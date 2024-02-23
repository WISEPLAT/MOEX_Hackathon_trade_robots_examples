import pandas as pd
import os
import datetime
from moexalgo import Ticker, Market
import streamlit as st
from tqdm import tqdm


def update_data(path2folder: str, period='D'):
    progress_text = "Updating in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    files = os.listdir(path2folder)
    for index in range(len(files)):
        file = files[index]
        n4bar = index/len(files)
        ticker_name = file[:-4]
        filepath = os.path.join("data/d1", file)
        data_ticker = pd.read_csv(filepath).reset_index(drop=False)
        data_ticker["begin"] = pd.to_datetime(data_ticker["begin"])
        last_date  = data_ticker["begin"].max()
        date_from = last_date + datetime.timedelta(days=1)
        ticker = Ticker(ticker_name)
        candles = ticker.candles(date=date_from, till_date="today", period=period)
        new_candles = pd.DataFrame(candles)
        new_candles.to_csv(filepath, mode="a", header=False)
        my_bar.progress(n4bar, text=f"Updating in progress. Please wait. Current_file: {ticker_name}")

if __name__=="__main__":
    update_data('data/d1', 'D')
