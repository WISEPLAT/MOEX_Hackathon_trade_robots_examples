import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
from math import floor
from termcolor import colored as cl

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20,10)

# Функция для получения данных TradeStats
def get_tradestats_data(dates):
    tradestats = pd.DataFrame()
    for date in dates:
        print(date)
        # Запрос возвращает не более 1000 записей, используем курсор для получения всех записей
        for cursor in range(25):
            url = f'https://iss.moex.com/iss/datashop/algopack/eq/tradestats.csv?date={date}&start={cursor*1000}&iss.only=data'
            df = pd.read_csv(url, sep=';', skiprows=2)
            tradestats = pd.concat([tradestats, df])
            if df.shape[0] < 1000:
                break
            time.sleep(0.5)
    tradestats.to_csv('tradestats.csv', index=None)
    return tradestats

# Получение данных TradeStats
tradestats_data = get_tradestats_data(['2023-11-20', '2023-11-21', '2023-11-22', '2023-11-23', '2023-11-24'])

# Функция для расчета скользящих средних
def sma(data, lookback):
    sma = data.rolling(lookback).mean()
    return sma

# Функция для расчета Bollinger Bands
def get_bb(data, lookback):
    std = data.rolling(lookback).std()
    upper_bb = sma(data, lookback) + std * 2
    lower_bb = sma(data, lookback) - std * 2
    middle_bb = sma(data, lookback)
    return upper_bb, middle_bb, lower_bb

# Расчет Bollinger Bands
aapl['upper_bb'], aapl['middle_bb'], aapl['lower_bb'] = get_bb(aapl['close'], 20)

# Функция для расчета Keltner Channel
def get_kc(high, low, close, kc_lookback, multiplier, atr_lookback):
    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift()))
    tr3 = pd.DataFrame(abs(low - close.shift()))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.ewm(alpha = 1/atr_lookback).mean()
    
    kc_middle = close.ewm(kc_lookback).mean()
    kc_upper = close.ewm(kc_lookback).mean() + multiplier * atr
    kc_lower = close.ewm(kc_lookback).mean() - multiplier * atr
    
    return kc_middle, kc_upper, kc_lower

# Расчет Keltner Channel
aapl['kc_middle'], aapl['kc_upper'], aapl['kc_lower'] = get_kc(aapl['high'], aapl['low'], aapl['close'], 20, 2, 10)

# Функция для расчета RSI
def get_rsi(close, lookback):
    ret = close.diff()
    up = []
    down = []
    for i in range(len(ret)):
        if ret[i] < 0:
            up.append(0)
            down.append(ret[i])
        else:
            up.append(ret[i])
            down.append(0)
    up_series = pd.Series(up)
    down_series = pd.Series(down).abs()
    up_ewm = up_series.ewm(com = lookback - 1, adjust = False).mean()
    down_ewm = down_series.ewm(com = lookback - 1, adjust = False).mean()
    rs = up_ewm/down_ewm
    rsi = 100 - (100 / (1 + rs))
    rsi_df = pd.DataFrame(rsi).rename(columns = {0:'rsi'}).set_index(close.index)
    rsi_df = rsi_df.dropna()
    return rsi_df[3:]

# Расчет RSI
aapl['rsi_14'] = get_rsi(aapl['close'], 14)

# Функция для стратегии Bollinger Bands, Keltner Channel и RSI
def bb_kc_rsi_strategy(prices, upper_bb, lower_bb, kc_upper, kc_lower, rsi):
    buy_price = []
    sell_price = []
    bb_kc_rsi_signal = []
    signal = 0
    
    for i in range(len(prices)):
        if lower_bb[i] < kc_lower[i] and upper_bb[i] > kc_upper[i] and rsi[i] < 30:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                bb_kc_rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_kc_rsi_signal.append(0)
                
        elif lower_bb[i] < kc_lower[i] and upper_bb[i] > kc_upper[i] and rsi[i] > 70:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                bb_kc_rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_kc_rsi_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_kc_rsi_signal.append(0)
                        
    return buy_price, sell_price, bb_kc_rsi_signal

# Применение стратегии Bollinger Bands, Keltner Channel и RSI
buy_price, sell_price, bb_kc_rsi_signal = bb_kc_rsi_strategy(aapl['close'], aapl['upper_bb'], aapl['lower_bb'],
                                                           aapl['kc_upper'], aapl['kc_lower'], aapl['rsi_14'])

# Построение графиков
ax1 = plt.subplot2grid((11,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((11,1), (6,0), rowspan = 5, colspan = 1)
ax1.plot(aapl['close'])
ax1.plot(aapl.index, buy_price, marker = '^', markersize = 10, linewidth = 0, color = 'green', label = 'BUY SIGNAL')
ax1.plot(aapl.index, sell_price, marker = 'v', markersize = 10, linewidth = 0, color = 'r', label = 'SELL SIGNAL')
ax1.set_title('AAPL STOCK PRICE')
ax2.plot(aapl['rsi_14'], color = 'purple', linewidth = 2)
ax2.axhline(30, color = 'grey', linestyle = '--', linewidth = 1.5)
ax2.axhline(70, color = 'grey', linestyle = '--', linewidth = 1.5)
ax2.set_title('AAPL RSI 10')
plt.show()

# Позиция
position = []
for i in range(len(bb_kc_rsi_signal)):
    if bb_kc_rsi_signal[i] > 1:
        position.append(0)
    else:
        position.append(1)
        
for i in range(len(aapl['close'])):
    if bb_kc_rsi_signal[i] == 1:
        position[i] = 1
    elif bb_kc_rsi_signal[i] == -1:
        position[i] = 0
    else:
        position[i] = position[i-1]
        
kc_upper = aapl['kc_upper']
kc_lower = aapl['kc_lower']
upper_bb = aapl['upper_bb'] 
lower_bb = aapl['lower_bb']
rsi = aapl['rsi_14']
close_price = aapl['close']
bb_kc_rsi_signal = pd.DataFrame(bb_kc_rsi_signal).rename(columns = {0:'bb_kc_rsi_signal'}).set_index(aapl.index)
position = pd.DataFrame(position).rename(columns = {0:'bb_kc_rsi_position'}).set_index(aapl.index)

frames = [close_price, kc_upper, kc_lower, upper_bb, lower_bb, rsi, bb_kc_rsi_signal, position]
strategy = pd.concat(frames, join = 'inner', axis = 1)

# Вывод JSON данных
json_data = strategy.to_json(orient='records')
print(json_data)