from __future__ import annotations
import typing as tp
from .SimpleDataset import SimpleDataset

import pandas as pd
import numpy as np

import warnings

warnings.filterwarnings("ignore")


class IfInference:
    @staticmethod
    def anomaly(
        features: tp.Dict[str, tp.Any],
        ticker: str,
        timestamp: str,
        df: pd.DataFrame,
        condition: tp.Literal["high", "low"],
        param: tp.Literal["value", "price_changing"],
        notebook: bool = False,
    ) -> pd.DataFrame:

        count_df = SimpleDataset.create_dataset(
            features, ticker, timestamp, candles=10_000, notebook=notebook
        )
        col = "target" if param == "price_changing" else "value"
        signal_col = f"anomal_{param}_{condition}"
        m = count_df[col].mean()
        s = count_df[col].std()
        anomal_l = m - (3 * s)
        anomal_r = m + (3 * s)
        tmp_anomaly_df = pd.DataFrame({signal_col: [0] * len(df)})

        if condition == "high":
            anomal_mask = np.array(df[col] > anomal_r)
            tmp_anomaly_df.loc[anomal_mask, signal_col] = 1
        elif condition == "low":
            anomal_mask = np.array(df[col] < anomal_l)
            tmp_anomaly_df.loc[anomal_mask, signal_col] = 1

        return tmp_anomaly_df

    @staticmethod
    def anomal_rsi(
        df: pd.DataFrame,
        period: tp.Literal[2, 5, 10, 15, 20, 30, 50],
        value: tp.Literal[50, 55, 60, 65, 70, 75, 80, 85, 90],
    ) -> pd.DataFrame:

        col = f"rsi_{period}"
        signal_col = f"anomal_rsi_{period}"
        tmp_anomaly_df = pd.DataFrame({signal_col: [0] * len(df)})

        anomaly_mask = np.array(df[col] > value)
        tmp_anomaly_df.loc[anomaly_mask, signal_col] = 1
        return tmp_anomaly_df

    @staticmethod
    def out_of_limits(
        df: pd.DataFrame,
        condition: tp.Literal["high", "low"],
        feature_name: tp.Literal[
            "close",
            "high",
            "low",
            "open",
            "value",
            "volume",
            "green_candles_ratio",
            "red_candles_ratio",
            "price_changing",
        ],
        limit: float,
        period: int | None = None,
    ) -> pd.DataFrame:

        col = feature_name
        if feature_name == "green_candles_ratio":
            col = f"green_{period}"
        elif feature_name == "red_candles_ratio":
            col = f"red_{period}"
        elif feature_name == "price_changing":
            col = "target"

        signal_col = f"out_of_limit_{feature_name}_{condition}"
        tmp_anomaly_df = pd.DataFrame({signal_col: [0] * len(df)})
        if condition == "high":
            anomaly_mask = np.array(df[col] > limit)
        elif condition == "low":
            anomaly_mask = np.array(df[col] < limit)

        tmp_anomaly_df.loc[anomaly_mask, signal_col] = 1
        return tmp_anomaly_df

    @staticmethod
    def average_cross(
        df: pd.DataFrame,
        average_type: tp.Literal["ema", "sma"],
        feature_name: tp.Literal["close", "high", "low", "open", "value", "volume"],
        n_fast: tp.Literal[2, 5, 10, 15, 50, 100],
        n_slow: tp.Literal[2, 5, 10, 15, 50, 100],
    ) -> pd.DataFrame:

        col_fast = f"{feature_name}_{average_type}_{n_fast}"
        col_slow = f"{feature_name}_{average_type}_{n_slow}"
        signal_col = f"{average_type}_{feature_name}_cross_{n_fast}_{n_slow}"
        delta = df[col_fast] - df[col_slow]
        tmp_anomaly_df = pd.DataFrame({signal_col: [0] * len(df)})

        tmp_anomaly_df[signal_col] = delta.rolling(2).apply(
            lambda x: ((x.iloc[0] > 0) and (x.iloc[1] < 0)) * 1
        )
        tmp_anomaly_df.fillna(0, inplace=True)
        return tmp_anomaly_df

    @staticmethod
    def macd_cross(
        df: pd.DataFrame,
        feature_name: tp.Literal["close", "high", "low", "open", "value", "volume"],
        n_fast: tp.Literal[2, 5, 10, 15, 50, 100],
        n_slow: tp.Literal[2, 5, 10, 15, 50, 100],
    ) -> pd.DataFrame:

        tmp_anomaly_df = IfInference.average_cross(
            df=df,
            average_type="ema",
            feature_name=feature_name,
            n_fast=n_fast,
            n_slow=n_slow,
        )

        return tmp_anomaly_df

    def process_if_block(
        self,
        df: pd.DataFrame,
        block: tp.Dict[str, tp.Any],
    ) -> pd.DataFrame:

        if block["feature"] == "anomaly":

            tmp_features = self.features

            signal_df = IfInference.anomaly(
                df=df,
                features=tmp_features,
                ticker=self.ticker,
                timestamp=self.timestamp,
                condition=block["condition"],
                param=block["param"],
                notebook=self.notebook,
            )

        if block["feature"] == "anomal_rsi":

            period = block["param"]["period"]
            value = block["param"]["value"]

            signal_df = IfInference.anomal_rsi(
                df=df,
                period=period,
                value=value,
            )

        if block["feature"] == "out_of_limits":

            condition = block["condition"]
            feature_name = block["param"]["feature_name"]
            limit = block["param"]["limit"]

            period = None
            if feature_name in ["green_candles_ratio", "red_candles_ratio"]:
                period = block["param"]["period"]

            signal_df = IfInference.out_of_limits(
                df=df,
                condition=condition,
                feature_name=feature_name,
                limit=limit,
                period=period,
            )

        if block["feature"] == "average_cross":

            average_type = block["param"]["average_type"]
            feature_name = block["param"]["feature_name"]
            n_fast = block["param"]["n_fast"]
            n_slow = block["param"]["n_slow"]

            signal_df = IfInference.average_cross(
                df=df,
                average_type=average_type,
                feature_name=feature_name,
                n_fast=n_fast,
                n_slow=n_slow,
            )

        if block["feature"] == "macd_cross":

            feature_name = block["param"]["feature_name"]
            n_fast = block["param"]["n_fast"]
            n_slow = block["param"]["n_slow"]

            signal_df = IfInference.macd_cross(
                df=df,
                feature_name=feature_name,
                n_fast=n_fast,
                n_slow=n_slow,
            )

        return signal_df

    def __init__(
        self,
        IF_features: tp.Iterable[tp.Dict[tp.Literal["and", "if"], tp.Any]],
        ticker: str,
        timestamp: tp.Literal["1m", "10m", "60m"],
        notebook: bool = False,
    ) -> None:

        self.IF_features = IF_features
        self.ticker = ticker
        self.timestamp = timestamp
        self.notebook = notebook

        rsi_periods = [2, 5, 10, 15, 20, 30, 50]

        candles_periods = [2, 5, 7, 10, 14, 21, 30, 100]

        average_periods = [2, 5, 10, 15, 50, 100]

        average_features = ["close", "high", "low", "open", "value", "volume"]

        self.features = {
            "lags": False,
            "cma": {"features": average_features},
            "sma": {"features": average_features, "period": average_periods},
            "ema": {"features": average_features, "period": average_periods},
            "green_candles_ratio": {"period": candles_periods},
            "red_candles_ratio": {"period": candles_periods},
            "rsi": {"period": rsi_periods},
            "macd": False,
            "bollinger": False,
            "time_features": False,
        }

    def predict_candles_dataframe(self, candles_df: pd.DataFrame) -> np.ndarray:
        df = candles_df.copy()
        signals = pd.DataFrame({"signal": [0] * len(df)})
        signals.reset_index(drop=True, inplace=True)

        for feat in self.IF_features:

            if feat["type"] == "and":
                and_signal = pd.DataFrame({"signal": [1] * len(df)})
                for and_feat in feat["blocks"]:
                    tmp_signal = self.process_if_block(
                        df=df,
                        block=and_feat,
                    )
                    and_signal["signal"] = and_signal["signal"].astype(
                        "int"
                    ) & tmp_signal.iloc[:, 0].astype("int")
                signals["signal"] = signals["signal"].astype("int") | and_signal[
                    "signal"
                ].astype("int")

            if feat["type"] == "if":
                tmp_signal = self.process_if_block(
                    df=df,
                    block=feat,
                )
                signals["signal"] = signals["signal"].astype("int") | tmp_signal.iloc[
                    :, 0
                ].astype("int")

        return signals.signal.values

    def predict_n_last_candles(
        self, candles: int = 1_000
    ) -> tp.Tuple[pd.DataFrame, np.ndarray]:

        df = SimpleDataset.create_dataset(
            self.features,
            self.ticker,
            self.timestamp,
            candles + 300,
            self.notebook,
        )
        df.reset_index(drop=True, inplace=True)

        signals = pd.DataFrame({"signal": [0] * len(df)})
        signals.reset_index(drop=True, inplace=True)

        for feat in self.IF_features:

            if feat["type"] == "and":
                and_signal = pd.DataFrame({"signal": [1] * len(df)})
                for and_feat in feat["blocks"]:
                    tmp_signal = self.process_if_block(
                        df=df,
                        block=and_feat,
                    )
                    and_signal["signal"] = and_signal["signal"].astype(
                        "int"
                    ) & tmp_signal.iloc[:, 0].astype("int")
                signals["signal"] = signals["signal"].astype("int") | and_signal[
                    "signal"
                ].astype("int")

            if feat["type"] == "if":
                tmp_signal = self.process_if_block(
                    df=df,
                    block=feat,
                )
                signals["signal"] = signals["signal"].astype("int") | tmp_signal.iloc[
                    :, 0
                ].astype("int")

        return df.tail(candles), signals.tail(candles).signal.values

    def predict_one_last_candle(self) -> tp.Tuple[pd.DataFrame, int]:

        candle, signal = self.predict_n_last_candles(candles=1)
        signal = signal[0]
        return candle, signal
