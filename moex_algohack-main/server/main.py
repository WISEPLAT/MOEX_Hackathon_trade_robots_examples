from fastapi import FastAPI
from moexalgo import Market, Ticker
import datetime
import random

app = FastAPI()

@app.get('/ping')
def ping():
    return 'pong'

@app.get('/candle')
def get_candle(ticker: str, timestamp: int, period: str):
    if period not in ['1m', '10m', '1h', '1d']:
        raise "Invalid argument"


    dataGetter = Ticker(ticker)

    ts = datetime.datetime.fromtimestamp(timestamp)
    for day in range(10):
        search_ts = datetime.datetime.fromtimestamp(timestamp - day*24*3600)
        dateformat = f'{search_ts.year:04}-{search_ts.month:02}-{search_ts.day:02}'
    
        cur_candles = list(dataGetter.candles(date=dateformat, till_date=dateformat, period=period))
        if 0 < len(cur_candles):
            for candle in cur_candles[::-1]:
                if candle.begin <= ts:
                    return candle

@app.get('/predictions')
def get_predictions(ticker: str):
    if random.randint(0, 9) == 1:
        return {'text':'text of event))','prediction':random.uniform(-0.1, 0.1)}
    else:
        return None
    
    
    