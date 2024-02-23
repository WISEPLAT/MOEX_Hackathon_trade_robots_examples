import streamlit as st
from moexalgo import Market, Ticker
import pandas as pd
import os
from update import update_data
from filters import *
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from utils import check_strategy


def page_strategies():
    st.title('Strategy backtesing')

    selected_strategy = st.selectbox(label='Select strategy:', options=['SMA Cross', 'Supertrend', 'Mean Reversion'])

    if selected_strategy == 'SMA Cross':
        st.caption("""
            [DESCRIPTION] Simple strategy: SMA crossover.

            Indicators:
            - SMA(period=50)
            - SMA(period=200)

            Conditions:
            - If SMA_50 crosses SMA_200 from bottom to top - BUY. 
            - Otherwise - close position, if exists. 
        """)
        st.table(check_strategy('strategies/SmaCross.csv'))

    elif selected_strategy == 'Supertrend':
        st.caption("""
            [DESCRIPTION] This strategy uses SMA with 200 period and Supertrend indicator to enter long
            when the price is above SMA and crosses the Supertrend from bottom to top. 
            Also this strategy uses Supertrend with `mult` parameter = 2 as Trailing stop.

            Indicators:
            - SMA (period=200)
            - Supertrend(period=21, mult=2)

            Conditions:
            - If close > SMA and close crosses Supertrend - Buy
            - exit by Trailing stop
        """)
        st.table(check_strategy('strategies/SmaTrendSupertrend.csv'))
    
    elif selected_strategy == 'Mean Reversion':
        st.caption("""
            [DESCRIPTION] Mean reversion strategy

            Indicators:
            - Bollinger Bands (period=50, mult=3)

            Conditions:
            - If close < Lower band - Buy
            - If close > Upper band - Sell
            - exit on SMA (from BB)
        """)
        st.table(check_strategy('strategies/MeanReversion.csv'))


