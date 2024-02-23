from backtesting.lib import TrailingStrategy, resample_apply
from backtesting import Backtest, Strategy
from backtesting.test import SMA
from backtesting.lib import crossover
from indicators import *
import pandas as pd


class Supertrend(TrailingStrategy):
    nrtr_period = 21
    nrtr_mult = 2
    mfi_period = 21
    rsi_period = 12

    def init(self):
        super().init()
        super().set_trailing_sl(n_atr=self.nrtr_mult)

        self.nrtr = self.I(supertrend, self.data, period=self.nrtr_period, mult=self.nrtr_mult)
        self.mfi = self.I(mfi, self.data, period=self.mfi_period)
        self.weekly_rsi = resample_apply('1W', pta.rsi, self.data.Close, self.rsi_period)

    def next(self):
        super().next()

        if not self.position and self.weekly_rsi[-1] > 50:  # If long
            if (self.data.Close[-1] > self.nrtr[-1]) and (self.data.Close[-2] < self.nrtr[-2]):
                sl = self.nrtr[-1] * 0.98
                self.buy(sl=sl)

        if self.position:
            if self.mfi[-1] > 80 and self.mfi[-2] < 80:
                self.position.close()


class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 50)
        self.ma2 = self.I(SMA, price, 200)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            # self.sell()
            self.position.close()


class SmaTrendSupertrend(TrailingStrategy):
    nrtr_period = 21
    nrtr_mult = 2

    def init(self):
        super().init()
        super().set_trailing_sl(n_atr=self.nrtr_mult)

        price = self.data.Close
        self.nrtr = self.I(supertrend, self.data, period=self.nrtr_period, mult=self.nrtr_mult)
        self.ma_long = self.I(SMA, price, 200)

    def next(self):
        super().next()
        if self.data.Close.s[-1] > self.ma_long[-1]:
            if crossover(self.data.Close.s, self.nrtr):
                self.buy()
        # elif self.data.Close.s[-1] < self.ma_long[-1]:
        #     if crossover(self.nrtr, self.data.Close.s):
        #         self.sell()


def std_3(arr, n):
    return pd.Series(arr).rolling(n).std() * 3

class MeanReversion(Strategy):
    roll = 50

    def init(self):
        self.he = self.data.Close

        self.he_mean = self.I(SMA, self.he, self.roll)
        self.he_std = self.I(std_3, self.he, self.roll)
        self.he_upper = self.he_mean + self.he_std
        self.he_lower = self.he_mean - self.he_std

        self.he_close = self.I(SMA, self.he, 1)

    def next(self):
        if self.he_close < self.he_lower:
            self.buy(tp = self.he_mean)

        if self.he_close > self.he_upper:
            self.sell(tp = self.he_mean)