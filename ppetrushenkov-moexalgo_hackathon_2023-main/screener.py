import streamlit as st
from moexalgo import Market, Ticker
# import datetime
import pandas as pd
import os
from update import update_data
from filters import *
# import plotly.express as px
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder


def page_screener():
    market = Market("stocks")
    md = market.marketdata()
    md = pd.DataFrame(md)

    st.title("Stock screener")
    
    col_1, col_2, col_3 = st.columns((2, 1, 3))
    
    # Select TimeFrame
    with col_2:
        tf = st.selectbox(label='Select TimeFrame:', options=['Daily', 'Weekly', 'Monthly'])
        condition = st.selectbox(label='Select filter condition:', options=['Low ADX', 'Squeezed', 'SMA Crosses', 'Supertrend', 'Mean Reversion'])    
    
    # Choose sector
    with col_3:
        ticker_sector_cap = pd.read_csv("data/sector_cap/ticker_info.csv")
        ticker_sector_cap.replace("-", pd.NA, inplace=True)
        ticker_sector_cap.dropna(inplace=True)
        ticker_sector_cap["MarketCap"] = ticker_sector_cap["MarketCap"].astype(float)
        filter_sector = st.multiselect("Select market sector:", ticker_sector_cap["Sector"].unique(), ticker_sector_cap["Sector"].unique())


    if condition == 'Low ADX':
        handler = no_trend
        params = dict(period=21)

    elif condition == 'SMA Crosses':
        handler = sma_crosses
        params = dict(short_period=50, long_period=200)
    
    elif condition == 'Squeezed':
        handler = squeeze
        params = dict(period=21)

    # elif condition == 'Supertrend':
    #     handler = supertrend_filter  # TODO
    #     params = dict(period=21, mult=2)

    elif condition == 'Supertrend':
        handler = supertrend_sma_breakout
        params = dict(ma_period = 200, atr_period = 21, mult = 2)

    elif condition == 'Mean Reversion':
        handler = mean_reversion
        params = dict(period = 21, mult = 3)

    # Screen stocks
    filtered_tickers = get_filtered_tickers_by_func(handler, params, tf)
    
    sector_info = pd.read_csv('data/sector_cap/ticker_info.csv')
    md = md.merge(sector_info, on='SECID', how='left')
    md = md[md['Sector'].isin(filter_sector)]
    md = md[['SECID', 'Sector', 'LAST', 'WAPRICE', 'NUMTRADES', 'VOLTODAY', 'ISSUECAPITALIZATION']]
    
    md.columns = ['Ticker', 'Sector', 'Close', 'Weighted Price', '№ trades', 'Volume today', 'Market Cap.']
    md = md[md['Ticker'].isin(filtered_tickers)]

    with col_1:
        use_top_from_each_sector = st.toggle(label='Pick TOP N from each chosen sector')
        top_n = st.slider('TOP N', min_value=1, max_value=5, value=2)    

    # SELECT TOP 2 FROM EACH SECTOR
    if use_top_from_each_sector:
        md = md.groupby('Sector').apply(lambda x: x.nlargest(top_n, 'Market Cap.'))
        
    md.reset_index(inplace=True, drop=True)

    st.subheader('Filtered stocks:', divider='orange')

    gd = GridOptionsBuilder.from_dataframe(md)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()

    grid_table = AgGrid(md, gridOptions=gridoptions,
                        update_mode=GridUpdateMode.SELECTION_CHANGED)

    if st.button(label='Add stocks to consideration list'):
        selected = grid_table['selected_rows']
        selected_tickers = pd.DataFrame(selected)['Ticker']
        portfolio = add_to_consider(selected_tickers)
        st.write('Done')


def get_filtered_tickers_by_func(handler, params, tf):
    filtered_tickers = []
    for ticker in os.listdir('data/d1'):
        ticker_name = ticker.split('.')[0]
        ticker_prices = pd.read_csv(f'data/d1/{ticker}')
        ticker_prices['begin'] = pd.to_datetime(ticker_prices['begin'])
        ticker_prices.set_index('begin', inplace=True)
        ticker_prices = ticker_prices[['open', 'high', 'low', 'close', 'volume']]

        if tf == 'Weekly':
            ticker_prices = ticker_prices.resample('1W').agg({'open': 'first', 
                                'high': 'max', 
                                'low': 'min', 
                                'close': 'last'})
        elif tf == 'Monthly':
            ticker_prices = ticker_prices.resample('1M').agg({'open': 'first', 
                                'high': 'max', 
                                'low': 'min', 
                                'close': 'last'})
                                    
        is_under_condition = handler(ticker_prices, **params)
        if is_under_condition:
            filtered_tickers.append(ticker_name)
    return filtered_tickers


def add_to_consider(tickers: pd.Series):
    tickers = tickers.tolist()
    file_path = 'data/considerations.csv'
    
    # Check if the portfolio file already exists
    if os.path.exists(file_path):
        portfolio = pd.read_csv(file_path)
        stocks_in_portfolio = portfolio['Ticker'].tolist()
        stocks_in_portfolio = stocks_in_portfolio + tickers
        stocks_in_portfolio = list(set(stocks_in_portfolio))
        stocks_in_portfolio = pd.Series(stocks_in_portfolio, name='Ticker')
        stocks_in_portfolio.to_csv(file_path, index=False)

    else:
        tickers.to_csv(file_path, index=False)