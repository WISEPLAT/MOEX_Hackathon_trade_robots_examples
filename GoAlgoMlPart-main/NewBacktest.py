from __future__ import annotations

import typing as tp

import numpy as np
import pandas as pd

from catboost import CatBoostRegressor
import lightgbm
from lightgbm import LGBMRegressor

from .SimpleDataset import SimpleDataset
from .IfInference import IfInference

from backtesting import Backtest

from backtesting.lib import SignalStrategy, TrailingStrategy


class NewBacktest:
    @staticmethod
    def to_backtest_format(tradestats: pd.DataFrame, timestamp: str) -> pd.DataFrame:
        df = pd.DataFrame(
            {'Open': tradestats['open'],
            'High': tradestats['high'],
            'Low': tradestats['low'],
            'Close': tradestats['close'],
            'Volume': tradestats['volume']})
        
        # WARNING! KILL THAT WITH FIRE!
        tradestats["date"] = tradestats["date"].dt.round("min")
        
        df.index = tradestats['date']

        return df

    @staticmethod
    def create_strategy_class(
        signals: np.ndarray,
        part_of_sum_for_buy: float,
        start_sum: float,
        perc_for_stop: float,
        percent_trailing: float = 6,
    ):
        class MyStrategy(SignalStrategy, TrailingStrategy):
            def init(self):
                super().init()
                self.signal = signals
                self.part_of_sum_for_buy = part_of_sum_for_buy
                self.percent = percent_trailing
                self.start_sum = start_sum
                self.perc_for_stop = perc_for_stop

                entry_size = self.signal * self.part_of_sum_for_buy

                self.set_signal(entry_size=entry_size)
                self.set_trailing_sl(self.percent)

            def next(self):
                if self.equity >= self.start_sum * self.perc_for_stop:
                    for trade in self.trades:
                        self.position.close()
                        self.buying_power = 0
                else:
                    super().next()

        return MyStrategy

    @staticmethod
    def get_preds_model(
        ticker: str,
        timestamp: str,
        model_features: tp.Dict[str, tp.Any],
        model_id: str,
        candles: int = 1_000,
        date_col: str = "date",
        target_col: str = "target",
        notebook: bool = False,
        seed: int = 42,
    ) -> tp.Tuple[pd.DataFrame, np.ndarray]:

        model_name = model_features["model"]
        model_path = f"{model_id}_{ticker}_{timestamp}_{model_name}.bin"

        test_data = SimpleDataset.create_dataset(
            model_features,
            ticker=ticker,
            timeframe=timestamp,
            candles=candles + 1_000,
            notebook=notebook,
        )

        test_data = test_data.tail(candles)
        df_return = test_data.copy()
        test_data = test_data.drop(columns=[date_col, target_col])

        if model_features["model"] == "catboost":
            model = CatBoostRegressor(
                eval_metric="RMSE",
                random_seed=seed,
            )
            model.load_model(model_path)
            preds = model.predict(test_data)

        if model_features["model"] == "lightgbm":
            model = lightgbm.Booster(model_file=model_path)
            preds = model.predict(test_data)

        signals = (preds > np.quantile(preds, 0.75)) * 1
        return df_return, signals

    def __init__(
        self,
        type: tp.Literal["if_model", "ml_model"],
        model_id: str | None,
        ticker: str,
        timestamp: tp.Literal["1m", "10m", "60m"],
        part_of_sum_for_buy: float,
        percent_trailing: float,
        start_sum: float,
        perc_for_stop: float,
        model_features: tp.Dict[str, tp.Any] | None = None,
        IF_features: dict[str, tp.Any] | None = None,
        notebook: bool = False,
    ) -> None:
        self.model_id = model_id
        self.ticker = ticker
        self.timestamp = timestamp
        self.PART_OF_SUM_FOR_BUY = part_of_sum_for_buy
        self.PERCENT_TRAILING = percent_trailing
        self.START_SUM = start_sum
        self.PERC_FOR_STOP = perc_for_stop
        self.notebook = notebook
        self.type = type
        self.model_features = model_features
        self.IF_features = IF_features

    def do_backtest(
        self,
        candles: int = 1_000,
        my_comission: float = 0.00003,
        html_save_path="graph.html",
    ):

        if self.type == "if_model":
            if_model = IfInference(
                IF_features=self.IF_features,
                ticker=self.ticker,
                timestamp=self.timestamp,
                notebook=self.notebook,
            )

            dataset, self.SIGNALS = if_model.predict_n_last_candles(candles=candles)
            self.SIGNALS[self.SIGNALS == 0] = -1

        elif self.type == "ml_model":
            dataset, self.SIGNALS = NewBacktest.get_preds_model(
                ticker=self.ticker,
                model_id=self.model_id,
                timestamp=self.timestamp,
                model_features=self.model_features,
                candles=candles,
                notebook=self.notebook,
            )
            self.SIGNALS[self.SIGNALS == 0] = -1

        dataset = NewBacktest.to_backtest_format(dataset, timestamp=self.timestamp)

        strategy = NewBacktest.create_strategy_class(
            self.SIGNALS,
            self.PART_OF_SUM_FOR_BUY,
            self.START_SUM,
            self.PERC_FOR_STOP,
            self.PERCENT_TRAILING,
        )

        bt = Backtest(
            dataset,
            strategy=strategy,
            cash=self.START_SUM,
            commission=my_comission,
        )

        stats = bt.run()

        bt.plot(filename=html_save_path, open_browser=False)
        return stats
