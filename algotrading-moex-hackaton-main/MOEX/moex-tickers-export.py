import pandas as pd
import ast
import codecs
import datetime as dt
import pytz
#import streamlit as st
import moexalgo as sns
from moexalgo import Market, Ticker

#st.header('MOEX recommendation API for trading')

# obtaining data

stocks = Market('stocks')

stocks_tickers = pd.DataFrame(stocks.tickers())

#stocks_tickers['PREVDATE'] = pd.to_datetime(stocks_tickers['PREVDATE']).strftime('"%Y-%m-%d %H:%M:%S %Z%z"')
#stocks_tickers['SETTLEDATE'] = pd.to_datetime(stocks_tickers['SETTLEDATE']).strftime('"%Y-%m-%d %H:%M:%S %Z%z"')

#tz = pytz.timezone('Europe/Moscow')
#stocks_tickers["PREVDATE"] = stocks_tickers["PREVDATE"].apply(lambda x: dt.datetime.utcfromtimestamp(x).replace(tzinfo=tz).strftime('"%Y-%m-%d %H:%M:%S %Z%z"'))
#stocks_tickers["PREVDATE"] = stocks_tickers["PREVDATE"].apply(lambda x: dt.datetime.fromtimestamp(x, pytz.timezone("UTC")))
#stocks_tickers["SETTLEDATE"] = stocks_tickers["SETTLEDATE"].apply(lambda x: pytz.timezone('Europe/Moscow').localize(x, is_dst=None).strftime('"%Y-%m-%d %H:%M:%S %Z%z"'))

#stocks_tickers["PREVDATE"] = stocks_tickers["PREVDATE"].apply(lambda x: datetime.datetime.fromtimestamp(x).isoformat())
#stocks_tickers["SETTLEDATE"] = stocks_tickers["SETTLEDATE"].apply(lambda x: datetime.datetime.fromtimestamp(x).isoformat())

#stocks_tickers["PREVDATE"] = stocks_tickers["PREVDATE"].apply(lambda x: x.date())
#stocks_tickers["SETTLEDATE"] = stocks_tickers["SETTLEDATE"].apply(lambda x: x.date())

stocks_tickers["PREVDATE"] = stocks_tickers["PREVDATE"].apply(lambda x: x.strftime("%Y-%m-%d"))
stocks_tickers["SETTLEDATE"] = stocks_tickers["SETTLEDATE"].apply(lambda x: x.strftime("%Y-%m-%d"))

out = stocks_tickers.to_json(orient='records', force_ascii=False)
out = out.replace('[{', '[{"model":"Trading.stock","pk":null,"fields":{')
out = out.replace('},{', '}},{"model": "Trading.stock","pk":null,"fields":{')
out = out.replace('}]','}}]')
print(out)

with codecs.open('tickers.json', 'w', 'utf-8') as f:
    f.write(out)

#print(unique_tickers)

#tradestat = pd.DataFrame(stocks.tradestats())
