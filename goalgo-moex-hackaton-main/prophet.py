#!/usr/bin/env python
# coding: utf-8


from moexalgo import Market, Ticker
from prophet import Prophet
import pandas as pd


class StockPredictor:
    """
    A class used to predict stock prices using Prophet model.

    ...

    Attributes
    ----------
    ticker : str
        a formatted string to determine the stock to be predicted
    predictions : int
        an integer to determine the number of future predictions

    Methods
    -------
    get_data():
        Returns the stock data from the moexalgo API.
    train_model():
        Trains the Prophet model and returns the forecasted data.
    """

    def __init__(self, ticker, days_to_predicts=60):
        """
        Parameters
        ----------
        ticker : str
            The stock to be predicted
        predictions : int
            The number of future predictions
        """

        self.ticker = ticker
        self.predictions = None
        self.days_to_predicts = days_to_predicts
        self.m = None  # model

    def get_data(self, min_date='2021-10-10', max_date='2023-12-04'):
        """
        Get the stock data from the moexalgo API.

        Parameters
        ----------
        min_date : str
            The minimum date for the stock data
        max_date : str
            The maximum date for the stock data

        Returns
        -------
        df
            a pandas DataFrame with the stock data
        """

        sber = Ticker(self.ticker)
        df = sber.candles(date=min_date, till_date=max_date)
        df = df.set_index('begin').drop('end', axis=1)
        return df

    def train_model(self):
        """
        Train the Prophet model and return the forecasted data.

        Returns
        -------
        forecast
            a pandas DataFrame with the forecasted data
        """

        df = self.get_data()
        df = df.reset_index()
        df = df[['begin', 'close']]
        df.columns = ['ds', 'y']

        self.m = Prophet()
        self.m.fit(df)

        future = self.m.make_future_dataframe(periods=self.days_to_predicts)
        self.predictions = self.m.predict(future)
        return self.predictions

    def plot(self):
        """
        Plot the forecasted data.

        Returns
        -------
        None
        """
        self.m.plot(forecast, xlabel=self.ticker, ylabel='close', plot_cap=False);


if __name__ == "__main__":
    stock_predictor = StockPredictor("SBER")
    forecast = stock_predictor.train_model()
    stock_predictor.plot()
