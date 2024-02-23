import pandas as pd
import ta
from ta.momentum import RSIIndicator
import matplotlib.dates as mdates
from ta.trend import adx_pos
from datetime import datetime
import numpy as np
from ipynb.fs.full import *
import talib
import matplotlib.pyplot as plt
from pandas.core.interchange import dataframe
from sklearn.datasets import load_iris

df = pd.read_csv('data.csv')

df.set_index('Время', inplace=True)


def calculate_stop_loss_and_take_profit(entry_price, stop_loss_percent=0.75, take_profit_percent=2):
    stop_loss = entry_price * (1 - stop_loss_percent / 100)
    take_profit = entry_price * (1 + take_profit_percent / 100)
    return stop_loss, take_profit


# Метод для имитации выполнения сделки
def execute_trade(symbol, side, quantity, price):
    """
    Имитация выполнения сделки.

    :param symbol: Символ торгуемого инструмента
    :param side: 'BUY' для покупки или 'SELL' для продажи
    :param quantity: Количество единиц для торговли
    :param price: Цена, по которой должна быть выполнена сделка
    :return: None
    """
    # Здесь может быть логика подключения к API биржи и исполнения сделки


# Функция для проверки условий выхода из сделки
def check_exit_conditions(current_price, entry_price, stop_loss, take_profit):
    if current_price <= stop_loss:
        return 'stop_loss'
    elif current_price >= take_profit:
        return 'take_profit'
    else:
        return None



def trading_bot(data, symbol, initial_capital=100000):
    in_position = False
    entry_price = None
    stop_loss = None
    take_profit = None
    capital = initial_capital
    index = 0
    count_stoploss = 0
    count_takeprofit = 0
    trade_entries = []
    trade_exits = []
    while index < len(data) - 1:
        current_price = data['Последняя цена за период'].iloc[index]  # Последняя известная цена закрытия
        quantity = int((capital * 0.02) / current_price)
        if not in_position:
            df['SMA_20'] = df['Последняя цена за период'].rolling(window=20, min_periods=1).mean()
            df['SMA_50'] = df['Последняя цена за период'].rolling(window=50, min_periods=1).mean()
            df['SMA_200'] = df['Последняя цена за период'].rolling(window=200, min_periods=1).mean()
            last_close = df['Последняя цена за период'].iloc[index]
            last_sma20 = df['SMA_20'].iloc[index]
            last_sma50 = df['SMA_50'].iloc[index]
            last_sma200 = df['SMA_200'].iloc[index]
            if( last_close > last_sma20 > last_sma50 > last_sma200):
                df['RSI'] = ta.momentum.RSIIndicator(df['Последняя цена за период'], window=30).rsi()
                last_rsi = df['RSI'].iloc[index]
                if( last_rsi < 70):
                    df['+DI'] = ta.trend.adx_pos(df['Максимальная цена за период'], df['Минимальная цена за период'],
                                                 df['Последняя цена за период'], window=30)
                    df['-DI'] = ta.trend.adx_neg(df['Максимальная цена за период'], df['Минимальная цена за период'],
                                                 df['Последняя цена за период'], window=30)
                    df['ADX'] = ta.trend.ADXIndicator(df['Максимальная цена за период'],
                                                      df['Минимальная цена за период'],
                                                      df['Последняя цена за период'], window=30).adx()
                    last_plus_di = df['+DI'].iloc[index]
                    last_minus_di = df['-DI'].iloc[index]
                    last_adx = df['ADX'].iloc[index]
                    if(last_plus_di > last_minus_di and last_adx > 25):
                        entry_price = current_price
                        stop_loss, take_profit = calculate_stop_loss_and_take_profit(entry_price)
                        execute_trade(symbol, 'BUY', quantity, price=entry_price)  # Пример: покупка 1 единицы инструмента
                        in_position = True
                        capital -= quantity * entry_price# Вычитаем использованный капитал
                        trade_entries.append((index, current_price))
        if in_position:
            exit_signal = check_exit_conditions(current_price, entry_price, stop_loss, take_profit)
            if exit_signal == 'stop_loss' or exit_signal == 'take_profit':
                execute_trade(symbol, 'SELL', quantity, price=current_price)
                capital += quantity * current_price
                in_position = False
                trade_exits.append((index, current_price))
                if exit_signal == 'stop_loss':
                    count_stoploss += 1
                elif exit_signal == 'take_profit':
                    count_takeprofit += 1
                # plot_trade(data, trade_entries[-1], trade_exits[-1])
        index += 1
        print(capital)
    print(count_takeprofit, count_stoploss)
    return capital



final_capital = trading_bot(df, "TCSG")
print(f"Итоговый капитал после симуляции: {final_capital}")
