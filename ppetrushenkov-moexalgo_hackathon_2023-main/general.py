import streamlit as st
from moexalgo import Market, Ticker
import datetime 
import pandas as pd
import os
from update import update_data
import plotly.express as px

market = Market("stocks")
stocks = pd.DataFrame(Market("stocks").marketdata())["SECID"].unique()


def page_general():
    st.title("Stock explorer")
    
    col_1, col_2= st.columns(2)
    with col_1:
        tf = st.radio(label='Select TimeFrame:', options=['Daily', 'Weekly', 'Monthly'])
    
    st.metric("Total stocks on market:", len(stocks))

    tickers = os.listdir('data/d1')
    stock_names = []
    pct_changes = []
    for ticker in tickers:
        data = pd.read_csv(f'data/d1/{ticker}')
        data['begin'] = pd.to_datetime(data['begin'])
        data.set_index('begin', inplace=True)
        data = data[['open', 'high', 'low', 'close']]
        if tf == 'Weekly':
            data = data.resample('1W').agg({'open': 'first', 
                                 'high': 'max', 
                                 'low': 'min', 
                                 'close': 'last'})
        elif tf == 'Monthly':
            data = data.resample('1M').agg({'open': 'first', 
                                 'high': 'max', 
                                 'low': 'min', 
                                 'close': 'last'})
        data = data.iloc[-2:, :]
        pct_change = data['close'].pct_change().values[-1] * 100
        pct_changes.append(pct_change)
        stock_names.append(ticker.split('.')[0])

    returns = pd.DataFrame({
        'SECID': stock_names,
        '%': pct_changes
    }).dropna()
    ticker_names = pd.DataFrame(market.tickers())[["SECID", "SHORTNAME", "PREVPRICE"]]
    returns = returns.merge(ticker_names, on="SECID", how="left")
    returns = returns[["SECID", "SHORTNAME", "PREVPRICE", "%"]]
    ticker_sector_cap = pd.read_csv("data/sector_cap/ticker_info.csv")
    ticker_sector_cap.replace("-", pd.NA, inplace=True)
    ticker_sector_cap.dropna(inplace=True)
    ticker_sector_cap["MarketCap"] = ticker_sector_cap["MarketCap"].astype(float)
    min_market_cap, max_market_cap = ticker_sector_cap["MarketCap"].min(), ticker_sector_cap["MarketCap"].max()

    with col_2:
        filter_sector = st.multiselect("Select market sector:", ticker_sector_cap["Sector"].unique(), ticker_sector_cap["Sector"].unique())

    returns = returns.merge(ticker_sector_cap, on="SECID", how="left")
    returns = returns[returns["Sector"].isin(filter_sector)]
    returns.sort_values(by='%', inplace=True, ascending=False)
    top5gainers = returns.head(5)
    top5losers = returns.tail(5)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Top gainers', divider='green')
        st.table(top5gainers)
    with col2:
        st.subheader('Top losers', divider='red')
        st.table(top5losers)
    st.button("Update data", on_click=lambda: update_data("data/d1"))

    treemap_ds = returns[["Sector", "%", "MarketCap"]].groupby("Sector").agg({'%': 'mean', 'MarketCap': 'sum'})
    c1, c2 = st.columns(2)
    with c1: st.dataframe(treemap_ds)
    #fig = px.treemap(treemap_ds, names=treemap_ds.index, values = "MarketCap")
    #fig.write_html("smth.html")
    piechart = px.pie(treemap_ds, names = treemap_ds.index, values="MarketCap", title="Total market capitalisation by sectors")
    with c2: st.plotly_chart(piechart)

    # treechart = px.treemap(returns, path = [px.Constant("market"), "Sector", "SECID"], values="MarketCap", color="%", range_color=[-.20, 0.20])
    treechart = px.treemap(returns, path = [px.Constant("market"), "Sector", "SECID"], values="MarketCap", color="%", range_color=[-10, 10])
    treechart.update_layout(autosize=False, width=1200, height=800)
    st.plotly_chart(treechart)

    

    