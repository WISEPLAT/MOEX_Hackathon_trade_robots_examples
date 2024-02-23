import streamlit as st
from moexalgo import Market, Ticker
import datetime 
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


def page_portfolio():
    st.title("Portfolio")
    st.header('Under consideration')
    favourite_tickers = pd.read_csv("data/considerations.csv").iloc[:, 0].tolist()

    market = Market("stocks")
    md = pd.DataFrame(market.marketdata())
    md = md[md['SECID'].isin(favourite_tickers)]

    sector_info = pd.read_csv('data/sector_cap/ticker_info.csv')

    md = md.merge(sector_info, on='SECID', how='left')
    md = md[['SECID', 'Sector', 'LAST', 'WAPRICE', 'NUMTRADES', 'VOLTODAY', 'ISSUECAPITALIZATION']]
    
    md.columns = ['Ticker', 'Sector', 'Close', 'Weighted Price', '№ trades', 'Volume today', 'Market Cap.']
    md.reset_index(inplace=True, drop=True)

    gd = GridOptionsBuilder.from_dataframe(md)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(md, gridOptions=gridoptions,
                        update_mode=GridUpdateMode.SELECTION_CHANGED)

    col1, col2, col3= st.columns((1, 1, 1, 4))[:3]

    with col1:
        if st.button(label='Buy'):
            selected = grid_table['selected_rows']
            selected_tickers = pd.DataFrame(selected)['Ticker']
            portfolio = add_to_bought(selected_tickers)
            st.write('Done')

    with col2:
        if st.button(label='Sell'):
            selected = grid_table['selected_rows']
            selected_tickers = pd.DataFrame(selected)['Ticker']
            portfolio = remove_from_bought(selected_tickers)
            st.write('Done')

    with col3:
        if st.button(label='Remove'):
            selected = grid_table['selected_rows']
            selected_tickers = pd.DataFrame(selected)['Ticker']
            portfolio = remove_from_considerations(selected_tickers)
            st.rerun()
            st.write('Done')

    st.header('Bought stocks')
    bought_tickers = pd.read_csv('data/bought.csv')
    bought_tickers = bought_tickers.merge(md, on='Ticker', how='left')
    st.table(bought_tickers)

    if st.button(label = "Check correlation for selected stocks"):
        selected = grid_table['selected_rows']
        selected_tickers = pd.DataFrame(selected)['Ticker']
        plot_heatmap(selected_tickers.tolist())


def remove_from_considerations(tickers: pd.Series):
    tickers2drop = tickers.tolist()
    file_path = 'data/considerations.csv'
    try:
        considered = pd.read_csv(file_path)
        stocks_considered = considered['Ticker'].tolist()
        for td in tickers2drop:
            stocks_considered.remove(td)
        stocks_considered = list(set(stocks_considered))
        stocks_considered = pd.Series(stocks_considered, name='Ticker')
        stocks_considered.to_csv(file_path, index=False)
    except Exception as e:
        st.markdown(":red[ERROR:] You don't have this stock in your portfolio")
        print(e)


def add_to_bought(tickers: pd.Series):
    # Check if the portfolio file already exists
    tickers = tickers.tolist()
    file_path = 'data/bought.csv'
    if os.path.exists(file_path):
        bought = pd.read_csv(file_path)
        stocks_bought = bought['Ticker'].tolist()
        stocks_bought = stocks_bought + tickers
        stocks_bought = list(set(stocks_bought))
        stocks_bought = pd.Series(stocks_bought, name='Ticker')
        stocks_bought.to_csv(file_path, index=False)

    else:
        tickers = pd.Series(tickers, name="Ticker")
        tickers.to_csv(file_path, index=False)

def remove_from_bought(tickers2drop: pd.Series):
    tickers2drop = tickers2drop.tolist()
    file_path = 'data/bought.csv'
    try:
        bought = pd.read_csv(file_path)
        stocks_bought = bought['Ticker'].tolist()
        for td in tickers2drop:
            stocks_bought.remove(td)
        stocks_bought = list(set(stocks_bought))
        stocks_bought = pd.Series(stocks_bought, name='Ticker')
        stocks_bought.to_csv(file_path, index=False)
    except Exception as e:
        st.markdown(":red[ERROR:] You don't have this stock in your portfolio")

def plot_heatmap(selected_tickers: pd.Series):

    start_date = datetime.datetime.now()-datetime.timedelta(days=30)
    end_date = datetime.datetime.now()

    ticker_ds = [pd.DataFrame(Ticker(ticker).candles(date=start_date, till_date=end_date, period="10m"))[["open", "close"]].mean(axis=1) for ticker in selected_tickers]
    ticker_stock_mean_oc = pd.concat(ticker_ds, axis=1)
    ticker_stock_mean_oc.columns = selected_tickers

    st.subheader('Correlation between stocks:', divider='red')
    heatmap = px.imshow(ticker_stock_mean_oc.corr(method='kendall'), x=selected_tickers, y=selected_tickers, color_continuous_scale='Reds', aspect="auto")
    heatmap.update_traces(text=ticker_stock_mean_oc.corr(method='kendall').round(2), texttemplate="%{text}")
    heatmap.update_layout({"height": 600, "width": 1050})
    st.plotly_chart(heatmap)