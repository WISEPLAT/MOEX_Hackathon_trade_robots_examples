import streamlit as st
import pandas as pd
import numpy as np

from general import page_general
from screener import page_screener
from portfolio import page_portfolio
from prophet_forecast import page_prophet
from strategy_statistics import page_strategies

st.set_page_config(layout="wide")

# page = st

# Навигация между страницами
page = st.sidebar.radio("Select a page", ["General", "Screener", "Strategy statistics", "Prophet forecast", "Portfolio"])

if page == "General":
    page_general()

elif page == "Screener":
    page_screener()

elif page == "Portfolio":
    page_portfolio()

elif page == "Strategy statistics":
    page_strategies()

elif page == "Prophet forecast":
    page_prophet()