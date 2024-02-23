import pandas as pd
import ast
import codecs
import datetime as dt
import pytz
#import streamlit as st
import moexalgo as sns
from moexalgo import Market, Ticker, metrics

#metrics.

#st.header('MOEX recommendation API for trading')

# obtaining data

stocks = Market('stocks')

stocks_tickers = pd.DataFrame(stocks.tickers())

stocks_tickers["PREVDATE"] = stocks_tickers["PREVDATE"].apply(lambda x: x.strftime("%Y-%m-%d"))
stocks_tickers["SETTLEDATE"] = stocks_tickers["SETTLEDATE"].apply(lambda x: x.strftime("%Y-%m-%d"))

#out = stocks_tickers.to_json(orient='records', force_ascii=False)
#out = out.replace('[{', '[{"model":"Trading.stock","pk":null,"fields":{')
#out = out.replace('},{', '}},{"model": "Trading.stock","pk":null,"fields":{')
#out = out.replace('}]','}}]')
#print(out)

# Акции SBER
sber = Ticker('SBER')

# Все акции
stocks = Market('stocks')

# Свечи по акциям SBER за период
#tradestat = sber.candles(date='2023-10-10', till_date='2023-10-18', period='10m').head()

#orderstat =  pd.DataFrame(sber.orderstats(date='2023-12-08'))
#print (orderstat)

end_date = dt.datetime.today()
timestamp_now = dt.datetime.timestamp(end_date)
timestamp_start=dt.datetime.fromtimestamp(timestamp_now-604800)
timestamp_start = timestamp_start.strftime("%Y-%m-%d")
tradestat = pd.DataFrame(sber.tradestats(date=timestamp_start, till_date='today'))

print (tradestat)
#print(tradestat)

#out = tradestat.to_json(orient='records', force_ascii=False)

tradestat.to_csv('trading.csv', sep='\t', encoding='utf-8')

