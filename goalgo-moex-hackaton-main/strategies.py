import pandas as pd

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG


def std_3(arr, n):
    """
    Calculate 3 standard deviations for a rolling window on the data.

    Parameters:
    arr (array-like): Input data
    n (int): Size of the rolling window

    Returns:
    pd.Series: Resulting data with rolling standard deviation
    """
    return pd.Series(arr).rolling(n).std() * 3


class SmaCross(Strategy):
    """
    Implements the SMA Cross strategy.
    """
    def init(self):
        """
        Initialize the strategy. Calculate the SMA for two different periods.
        """
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        """
        Define the strategy's step. Buy when the first SMA crosses above the second, sell when it crosses below.
        """
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


class MeanReversion(Strategy):
    """
    Implements the Mean Reversion strategy.
    """
    roll = 50

    def init(self):
        """
        Initialize the strategy. Calculate the mean and standard deviation for a rolling window on the data.
        """
        self.he = self.data.Close

        self.he_mean = self.I(SMA, self.he, self.roll)
        self.he_std = self.I(std_3, self.he, self.roll)
        self.he_upper = self.he_mean + self.he_std
        self.he_lower = self.he_mean - self.he_std

        self.he_close = self.I(SMA, self.he, 1)
        
    def next(self):
        """
        Define the strategy's step. Buy when the price is below the lower bound, sell when it's above the upper bound.
        """

        if self.he_close < self.he_lower:
            self.buy(
                tp = self.he_mean,
            )

        if self.he_close > self.he_upper:
            self.sell(
                tp = self.he_mean,
            )


def run_sma_cross_strategy_stats(df):
    """
    Run the SMA Cross strategy on the data and return the statistics.

    Parameters:
    df (pd.DataFrame): Input data

    Returns:
    dict: Statistics of the strategy
    """
    sma_cross_strategy = Backtest(df, SmaCross, commission=.002,
                                  exclusive_orders=True)
    stats = sma_cross_strategy.run()
    return stats


def run_sma_cross_strategy_plot(df):
    """
    Run the SMA Cross strategy on the data and plot the results.

    Parameters:
    df (pd.DataFrame): Input data

    Returns:
    matplotlib.figure.Figure: Plot of the strategy
    """
    sma_cross_strategy = Backtest(df, SmaCross, commission=.002,
                                  exclusive_orders=True)
    sma_cross_strategy.run()
    return sma_cross_strategy.plot(filename='Оценка стратегии', plot_width=None,
             plot_equity=True, plot_return=True, plot_pl=True,
             plot_volume=True, plot_drawdown=True,
             smooth_equity=False, relative_equity=True,
             resample=True, reverse_indicators=False,
             show_legend=True, open_browser=True)


def run_mean_reversion_stats(df):
    """
    Run the Mean Reversion strategy on the data and return the statistics.

    Parameters:
    df (pd.DataFrame): Input data

    Returns:
    dict: Statistics of the strategy
    """
    mean_reversion_strategy = Backtest(df, MeanReversion, commission=.002,
                                       exclusive_orders=True)
    stats = mean_reversion_strategy.run()
    return stats


def run_mean_reversion_plot(df):
    """
    Run the Mean Reversion strategy on the data and plot the results.

    Parameters:
    df (pd.DataFrame): Input data

    Returns:
    matplotlib.figure.Figure: Plot of the strategy
    """
    mean_reversion_strategy = Backtest(df, MeanReversion, commission=.002,
                                       exclusive_orders=True)
    mean_reversion_strategy.run()
    return mean_reversion_strategy.plot()
