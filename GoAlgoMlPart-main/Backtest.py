from __future__ import annotations
from typing import Dict, List, Iterable
import math

import pandas as pd
import numpy as np

from .SimpleDataset import SimpleDataset

# import dill

from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from lightgbm import LGBMRegressor
import catboost
import lightgbm
from sklearn.metrics import mean_squared_error

# from fastai.tabular.all import *
import warnings
import lightgbm as lgb

warnings.filterwarnings("ignore")


class Backtest:
    @staticmethod
    def calculate_year_income(
        sum_before: int = None,
        sum_after: int = None,
        candle_period: int = None,
        candle_val: int = None,
    ):  # сколько свечей на валидации

        if sum_after == sum_before:
            return 0
        income = sum_after - sum_before
        time = candle_val * candle_period  # сколько минут прошло
        days = math.ceil(time / 785)
        n = int(365 / days)
        if sum_after > sum_before:
            return (income * n + sum_before) / sum_before * 100
        if sum_after < sum_before:
            return (income * n) / sum_before * 100

    def __init__(
        self,
        features,
        balance: float,
        max_balance_for_trading: float,
        min_balance_for_trading: float,
        period: str,
        part_of_balance_for_buy: float = None,
        sum_for_buy_rur: float = None,
        sum_for_buy_num: float = None,
        part_of_balance_for_sell: float = None,
        sum_for_sell_rur: float = None,
        sum_for_sell_num: float = None,
        sell_all: bool = False,
        notebook: bool = False,
    ):

        self.features = features
        self.balance = balance
        self.start_balance = balance
        self.max_balance = max_balance_for_trading
        self.min_balance = min_balance_for_trading
        self.cur_volume_rur = 0
        self.cur_volume_num = 0
        self.num_for_trade = 0

        self.part_of_balance_for_buy = part_of_balance_for_buy
        self.sum_for_buy_rur = sum_for_buy_rur
        self.sum_for_buy_num = sum_for_buy_num

        self.part_of_balance_for_sell = part_of_balance_for_sell
        self.sum_for_sell_rur = sum_for_sell_rur
        self.sum_for_sell_num = sum_for_sell_num
        self.sell_all = sell_all

        self.sum_volume = 0
        self.preds = []
        self.prices = []
        self.sygnals = []
        self.notebook = notebook

        if period == "1m":
            self.candle_period = 1
        if period == "10m":
            self.candle_period = 10
        if period == "60,":
            self.candle_period = 60

    def get_preds(
        self,
        ticker,
        timeframe,
        seed=42,
        candles=1000,
        date_col: str = "date",
        target_col: str = "target",
    ):

        model_path = f'{12345678}_{ticker}_{timeframe}_{self.features["model"]}.bin'
        test_data = SimpleDataset.create_dataset(
            features=self.features,
            ticker=ticker,
            timeframe=timeframe,
            candles=candles,
            notebook=self.notebook,
        )
        test_data = test_data.drop(columns=[date_col, target_col])
        self.prices = test_data["close"].values

        if self.features["model"] == "catboost":
            model = CatBoostRegressor(eval_metric="RMSE", random_seed=seed)
            model.load_model(model_path)
            self.preds = model.predict(test_data)

        if self.features["model"] == "lightgbm":
            model = lgb.Booster(model_file=model_path)
            self.preds = model.predict(test_data)

        # if self.features['model'] == 'tabular_learner':
        #     model = load_learner(model_path, cpu=True, pickle_module=dill)
        #     test_dl = model.dls.test_dl(test_data)
        #     self.preds, _ = model.get_preds(dl = test_dl)

        self.sygnals = (self.preds > np.quantile(self.preds, 0.95)) * 1

    def buy(self, price: float) -> str:

        if self.part_of_balance_for_buy:
            self.num_for_trade = self.balance * self.part_of_balance_for_buy // price
        elif self.sum_for_buy_rur:
            self.num_for_trade = self.sum_for_buy_rur // price
        elif self.sum_for_buy_num:
            self.num_for_trade = self.sum_for_buy_num
        else:
            return "error"

        if self.balance - self.num_for_trade * price > 0:

            self.cur_volume_num += self.num_for_trade
            self.cur_volume_rur = self.cur_volume_num * price
            self.balance -= self.num_for_trade * price
            self.sum_volume += self.cur_volume_num * price

        else:
            pass

        self.num_for_trade = 0

        return self.change_parameters()

    def sell(self, price: float) -> str:

        if self.cur_volume_num > 0:

            if self.part_of_balance_for_sell:
                self.num_for_trade = (
                    self.balance * self.part_of_balance_for_sell // price
                )
            elif self.sum_for_sell_rur:
                self.num_for_trade = self.sum_for_sell_rur // price
            elif self.sum_for_sell_num:
                self.num_for_trade = self.sum_for_sell_num
            elif self.sell_all:
                self.num_for_trade = self.cur_volume_num
            else:
                return "error"

            self.cur_volume_num -= self.num_for_trade
            self.cur_volume_rur = self.cur_volume_num * price
            self.balance += self.num_for_trade * price
            self.sum_volume += self.cur_volume_num * price
            self.num_for_trade = 0

        else:
            pass

        return self.change_parameters()

    def change_parameters(self) -> str:

        if self.balance < self.min_balance:
            return "min_balance"

        elif self.balance > self.max_balance:
            return "max_balance"

        else:
            return "done"

    def do_backtest(self, ticker, timeframe, candles=1000):

        self.num_candles = candles

        self.get_preds(ticker, timeframe, candles)

        for idx in range(len(self.sygnals)):
            status = ""
            if self.sygnals[idx]:
                status = self.buy(self.prices[idx])
            else:
                status = self.sell(self.prices[idx])

            if (status == "min_balance") or (status == "max_balance"):
                break

            # print(self.sygnals[idx], self.prices[idx])
            # print(status)
            # print(self.balance)
            # print(self.cur_volume_rur)
            # print(self.cur_volume_num)
            # print(self.num_for_trade)
            # print('\n')

        self.balance += self.cur_volume_rur

        year_income = Backtest.calculate_year_income(
            self.start_balance,
            self.balance,
            self.candle_period,
            self.num_candles,
        )
        return self.balance, year_income
