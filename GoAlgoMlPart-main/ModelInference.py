from __future__ import annotations
from typing import Dict, List, Iterable, Any

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


class ModelInference:
    def __init__(
        self,
        features: Dict[str, Any],
        ticker: str,
        model_id: str,
        timeframe: str,
        api_data: Any,  # Заглушка для api
        #  balance: float,
        #  max_balance_for_trading: float,
        #  min_balance_for_trading: float,
        #  part_of_balance_for_buy: float=None,
        #  sum_for_buy_rur: float=None,
        #  sum_for_buy_num: float=None,
        #  part_of_balance_for_sell: float=None,
        #  sum_for_sell_rur: float=None,
        #  sum_for_sell_num: float=None,
        #  sell_all: bool=False,
        notebook: bool = False,
    ):

        self.features = features

        self.ticker = ticker
        self.user_id = model_id
        self.timeframe = timeframe
        self.api_data = api_data

        # self.balance = balance
        # self.max_balance = max_balance_for_trading
        # self.min_balance = min_balance_for_trading
        # self.cur_volume_rur = 0
        # self.cur_volume_num = 0
        # self.num_for_trade = 0

        # self.part_of_balance_for_buy = part_of_balance_for_buy
        # self.sum_for_buy_rur = sum_for_buy_rur
        # self.sum_for_buy_num = sum_for_buy_num

        # self.part_of_balance_for_sell = part_of_balance_for_sell
        # self.sum_for_sell_rur = sum_for_sell_rur
        # self.sum_for_sell_num = sum_for_sell_num
        # self.sell_all = sell_all

        # self.sum_volume = 0
        # self.price = 0
        self.sygnals = []
        self.notebook = notebook

    def get_pred_one_candle(
        self, seed=42, candles=200, date_col: str = "date", target_col: str = "target"
    ):
        model_path = f'{self.user_id}_{self.ticker}_{self.timeframe}_{self.features["model"]}.bin'
        test_data = SimpleDataset.create_dataset(
            features=self.features,
            ticker=self.ticker,
            timeframe=self.timeframe,
            candles=candles,
            notebook=self.notebook,
        )
        test_data = test_data.drop(columns=[date_col, target_col]).tail(1)

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

        self.sygnals = (self.preds > self.features["threshold"]) * 1
        return test_data, self.sygnals[0]

    # def change_parameters(self) -> str:

    #     if (self.balance < self.min_balance):
    #         return "min_balance"

    #     elif (self.balance > self.max_balance):
    #         return "max_balance"

    #     else:
    #         return "done"

    # def buy(self, price: float) -> str:
    #     if (self.part_of_balance_for_buy):
    #         self.num_for_trade = self.balance * self.part_of_balance_for_buy // price
    #     elif (self.sum_for_buy_rur):
    #         self.num_for_trade = self.sum_for_buy_rur // price
    #     elif (self.sum_for_buy_num):
    #         self.num_for_trade = self.sum_for_buy_num
    #     else:
    #         return "error"

    #     if (self.balance - self.num_for_trade * price > 0):

    #         self.cur_volume_num += self.num_for_trade
    #         self.cur_volume_rur = self.cur_volume_num * price
    #         self.balance -= self.num_for_trade * price
    #         self.sum_volume += self.cur_volume_num * price

    #     else:
    #         pass

    #     self.num_for_trade = 0

    #     return self.change_parameters()

    # def sell(self, price: float) -> str:

    #     if (self.cur_volume_num > 0):

    #         if (self.part_of_balance_for_sell):
    #             self.num_for_trade = self.balance * self.part_of_balance_for_sell // price
    #         elif (self.sum_for_sell_rur):
    #             self.num_for_trade = self.sum_for_sell_rur // price
    #         elif (self.sum_for_sell_num):
    #             self.num_for_trade = self.sum_for_sell_num
    #         elif (self.sell_all):
    #             self.num_for_trade = self.cur_volume_num
    #         else:
    #             return "error"

    #         self.cur_volume_num -= self.num_for_trade
    #         self.cur_volume_rur = self.cur_volume_num * price
    #         self.balance += self.num_for_trade * price
    #         self.sum_volume += self.cur_volume_num * price
    #         self.num_for_trade = 0

    #     else:
    #         pass

    #     return self.change_parameters()

    # def change_parameters(self) -> str:

    #     if (self.balance < self.min_balance):
    #         return "min_balance"

    #     elif (self.balance > self.max_balance):
    #         return "max_balance"

    #     else:
    #         return "done"

    # def do_one_candle(self):

    #     candle, signal = self.get_pred_one_candle()
    #     self.price = candle['close']
