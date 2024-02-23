import streamlit as st
from moexalgo import Market, Ticker
import datetime 
import pandas as pd
import numpy as np
import os
from prophet import Prophet
import plotly.graph_objects as go

stocks = pd.DataFrame(Market("stocks").marketdata())["SECID"].unique()
def page_prophet():
    st.title("Stock price forecasting")
    
    ticker = st.selectbox("Stock:", stocks)
    start_date, end_date = st.date_input(label='Date Range:',
                            value=(datetime.datetime.now()-datetime.timedelta(days=365), 
                                    datetime.datetime.now()),
                            key='#date_range',
                            help="The start and end date time")
    timeframe = st.selectbox("TimeFrame:", ['1m', '10m', '1h', 'D', 'W', 'M', 'Q'], 4)
    ticker_time_data = Ticker(ticker).candles(date=start_date, till_date=end_date, period=timeframe)
    ticker_time_data = pd.DataFrame(ticker_time_data)
    if ticker_time_data.empty:
        st.text("Please select another datas. It seems like there were no market operations during those days.")

    st.subheader(f'{ticker} candle plot:', divider='green')

    '''fig = go.Figure(data=[go.Candlestick(x=tatn_data["TRADEDATE"],
open=tatn_data["OPEN"],
high=tatn_data["HIGH"],
low=tatn_data["LOW"],
close=tatn_data["CLOSE"],
increasing_line_color='orange',
decreasing_line_color = 'black',
name = "real data"
)])
fig.add_trace(go.Scatter(x = forecast.ds, y = forecast.trend, name = "predicted data"))
fig.show()'''

    fig = go.Figure(data=[go.Candlestick(
    x=ticker_time_data["begin"],
    open=ticker_time_data["open"],
    high=ticker_time_data["high"],
    low=ticker_time_data["low"],
    close=ticker_time_data["close"],
    increasing_line_color="green",
    decreasing_line_color="red"
    )])
    fig.update_layout({"width": 1050})
    fig.update_layout(xaxis_rangeslider_visible=False)

    st.plotly_chart(fig)

    periods2pred = st.number_input("Enter selected periods number to predict", 100, step=1)
    st.dataframe(make_prediction(ticker_time_data, periods2pred))

    if st.button("Make a forecast with Reccurent Neural Network"):
        candles_forecast = make_prediction(ticker_time_data, periods=periods2pred)
        lines_low_high = candles_forecast[candles_forecast.notna()][["ds", "yhat", "yhat_lower", "yhat_upper", "trend_lower", "trend_upper"]]
        candles_forecast_fig = go.Figure(data=[go.Candlestick(
            x=ticker_time_data["begin"], open=ticker_time_data["open"],
            high=ticker_time_data["high"], low=ticker_time_data["low"],
            close=ticker_time_data["close"], increasing_line_color="green", decreasing_line_color="red", name="Train data")])
        candles_forecast_fig.add_trace(go.Scatter(x=lines_low_high["ds"], y=lines_low_high["yhat"], name="Forecast"))
        candles_forecast_fig.add_trace(go.Scatter(x=lines_low_high["ds"], y=lines_low_high["yhat_lower"], name="Uncertainity lower border"))
        candles_forecast_fig.add_trace(go.Scatter(x=lines_low_high["ds"], y=lines_low_high["yhat_upper"], name="Uncertainity upper border"))

        st.subheader(f'{ticker} Forecasting:', divider='blue')
        candles_forecast_fig.update_layout({"width": 1100, "height": 900})
        st.plotly_chart(candles_forecast_fig)


def make_prediction(history_data: pd.DataFrame, periods: int):
    train_data = history_data[["begin", "close"]]
    train_data.columns = ['ds', 'y']
    model = Prophet()
    model.fit(train_data)
    future = model.make_future_dataframe(periods = periods)
    forecast = model.predict(future)[["ds", "yhat", "trend", "yhat_lower", "yhat_upper", "trend_lower", "trend_upper"]]
    return forecast