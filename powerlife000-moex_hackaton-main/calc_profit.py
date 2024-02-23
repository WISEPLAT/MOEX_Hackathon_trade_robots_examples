#!/usr/bin/env python
# coding: utf-8

# # Импортируем библиотеки
import datetime
import pytz
import os
from pathlib import Path
import time
import requests
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator

from mpl_finance import candlestick_ohlc  #  pip install mpl-finance
import mplfinance as mpf
import pandas_ta as ta
import numpy as np
from sklearn.model_selection import train_test_split
import talib
import pickle
import yfinance as yf
import math
import json
from moexalgo import Market, Ticker
from sklearn.preprocessing import MinMaxScaler 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.regularizers import l2
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from tensorflow.keras import regularizers
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import LSTM, Dense, Dropout, Masking, Embedding
from tensorflow.keras.models import load_model
from array import *
import os.path
import joblib
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, auc, accuracy_score, roc_auc_score,f1_score,log_loss,\
classification_report, roc_curve
from math import sqrt
from sys import argv #Module for receiving parameters from the command line
import io
from PIL import Image
import base64
import argparse
import psycopg2
from sqlalchemy import create_engine

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

pd.options.mode.chained_assignment = None  # default='warn'

#%matplotlib qt
# # Импортируем модули
import sys, signal
sys.path.insert(0, 'modules')

def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#Модули генерации датасета
from date_filter import date_filter #Фильтрация данных по датам date_filter(quotes, filter_data_timezone, filter_data_start, filter_data_end)
from show_quotes import show_quotes #Смотрим исходные данные show_quotes(quotes)
from get_extrems import get_extrems #Получаем экстремумы get_extrems(dataset, delete_not_marking_data, count_points = 6)
from show_quotes_with_trends import show_quotes_with_trends #Просмотр результатов разметки show_quotes_with_trends(quotes_with_extrems, show = False)
from quotes_with_Y import quotes_with_Y#Разметка Y quotes_with_Y(quotes_with_extrems, extr_bar_count, Y_shift)
from get_indicators import get_indicators #Получение индикаторов для котировок get_indicators(df, prefix = ':1d')
from get_stoch_indicators import get_stoch_indicators#Обработка стохастика над индикаторами get_stoch_indicators(df, prefix = ':1d')
from get_stoch_logic_data import get_stoch_logic_data#Генерация логического датасета над датасетом стохастика get_stoch_logic_data(df, prefix = ':1d')
from norm_num_df import norm_num_df# Генерация нормализованного числового датасета norm_num_df(df, prefix = ':1d')
from waves_dataset import waves_dataset#Генерация датасета по экстремумам waves_dataset(df, prefix = ':1d')
from logic_dataset import logic_dataset#Генерация датасета на основании логических конструкций logic_dataset(df, prefix = ':1d')


# # Параметры генерируемого датасета
load_params_from_config_file = True #Загрузка параметров из файла
load_params_from_command_line = False #Загрузка параметров из командной строки
args = None

try:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument('--config_file', dest='config_file', action='store_true', help='Load config from file')
    _ = parser.add_argument('--config_path', help='Path to config file: /app/cfg.json')
    _ = parser.add_argument('--cmd_config', dest='cmd_config', action='store_true', help='Load config from cmd line')
    _ = parser.add_argument('--task_id')
    _ = parser.add_argument('--scaler_path')
    _ = parser.add_argument('--neural_path')
    _ = parser.add_argument('--ticker')
    _ = parser.add_argument('--timeframe')
    _ = parser.add_argument('--start_date')
    _ = parser.add_argument('--end_date')
    _ = parser.add_argument('--count_points')
    _ = parser.add_argument('--extr_bar_count')
    _ = parser.add_argument('--max_unmark')
    _ = parser.add_argument('--respos_url')
    args, unknown = parser.parse_known_args()
    
    if args.config_file:
        load_params_from_config_file = True
        load_params_from_command_line = False
    
    if args.cmd_config:
            load_params_from_config_file = False
            load_params_from_command_line = True
except:
    print("Ошибка парсинга параметров из командной строки")

if load_params_from_config_file:
    #Если есть параметры командной строки
    if args:
        #Если указан путь к конфигу
        if args.config_path:
            with open(config_path, 'r', encoding='utf_8') as cfg:
                temp_data=cfg.read()
        else:
            with open('app/configs/1D/calc_profit.json', 'r', encoding='utf_8') as cfg:
                temp_data=cfg.read()

    # parse file`
    config = json.loads(temp_data)
    
    task_id = str(config['task_id'])
    #Путь для сохранения скалера
    scaler_path = config['scaler_path'] #Путь должен быть без чёрточки в конце
    #Путь для сохранения нейронных сетей
    neural_path = config['neural_path'] #Путь должен быть без чёрточки в конце
    ticker = config['ticker']
    interval = config['timeframe']
    start_date = config['start_date'] #Начальная дата датасета
    end_date = config['end_date'] #Конечная дата датасета
    count_points = config['count_points'] #Параметр разметки экстремумов
    extr_bar_count = config['extr_bar_count'] #Сколько баров размечаем для генерации сигналов
    #Максимальное количество конечных баров волны в %, которые не размечаем
    max_unmark = config['max_unmark']
    if config['respos_url']:
        respos_url = config['respos_url']
    else:
        respos_url = '127.0.0.1:8080'
    
if load_params_from_command_line:
    task_id = str(args.task_id)
    scaler_path = str(args.scaler_path)
    neural_path = str(args.neural_path)
    ticker = str(args.ticker) 
    interval = str(args.timeframe)
    start_date = str(args.start_date) 
    end_date = str(args.end_date) 
    count_points = int(args.count_points) 
    extr_bar_count = int(args.extr_bar_count) 
    max_unmark = float(args.max_unmark) 
    if args.respos_url:
        respos_url = str(args.respos_url).replace(']',"").replace('[',"").replace('"',"").replace("'","")
    else:
        respos_url = '127.0.0.1:8080'

Y_shift = 0

#Смещение категориальных признаков разметки
Y_shift = 1

#Флаг необходимости формирования трендовых признаков
lag_flag = True

#Число баров, которые мы кладём в датасет для формирования признаков трендовости
#Число включает начальный бар без лага, то есть из 6: 1 - начальный + 5 лаговые
lag_count = 0

#Флаг необходимости масштабирования данных
scale_flag = True

#Флаг необходимости генерации сигналов по последним открытым позициям
open_positions_flag = True

#По какому количеству открытых позиций нужно проходить?
open_positions_count = 5

#Флаг необходимости удаления не размеченных данных
delete_not_marking_data = False

#Флаг необходимости генерации признаков индекса S&P500
get_index_features = False

#Стоп лосс
stop_loss_flag = False
stop_loss = -0.1 # в %

def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

def plt_to_png(graph):
    buffer = io.BytesIO()
    graph.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    graph.close()

    return graphic

#Смотрим результаты разметки
def show(quotes_with_extrems):
    quotes_with_extrems['Color'] = None
    quotes_with_extrems['Trend'] = None
    
    #Раскрашиваем тренды
    last_extr = None

    for i, quote in quotes_with_extrems.iterrows():

        if quote['extr'] == 'max':
            last_extr = 'max'
        elif quote['extr'] == 'min':
            last_extr = 'min'

        if last_extr == 'min':
            quotes_with_extrems.at[i, 'Color'] = '#AFE1AF'#green
            quotes_with_extrems.at[i, 'Trend'] = 'buy'
        elif last_extr == 'max':
            quotes_with_extrems.at[i, 'Color'] = '#880808'#red
            quotes_with_extrems.at[i, 'Trend'] = 'sell'

    quotes_with_extrems['x'] = quotes_with_extrems.index
    
    y_max = quotes_with_extrems['High'].max()*1.05
    y_min = quotes_with_extrems['Low'].min()*0.95
    
    return quotes_with_extrems

def get_ideal_profit(quotes_with_extrems):
    #Трейды без смещения

    trades_without_shift = []

    current_position = 'close'
    current_open_price = 0

    iter_count = 0
    for i, quote in quotes_with_extrems.iterrows():

        if current_position == 'close':
            if quote['Trend'] == 'buy':
                current_position = 'open'
                current_open_price = quote['Close']

        if current_position == 'open':
            
            if (stop_loss_flag) & (current_open_price != quote['Close']):
                profit_num = ((quote['Close']/current_open_price) - 1)*100
                #print(profit_num)
                
                if profit_num <= stop_loss:
                    current_position = 'close'
                    profit = quote['Close']/current_open_price
                    trades_without_shift.append([current_open_price, quote['Close'], profit])
            
            if (quote['Trend'] == 'sell') | (iter_count+1 == quotes_with_extrems.shape[0]):
                current_position = 'close'

                profit = quote['Close']/current_open_price

                trades_without_shift.append([current_open_price, quote['Close'], profit])

        iter_count = iter_count + 1
        
    #Доходность без смещения

    profit_without_shift = 1

    for row in trades_without_shift:
        profit_without_shift = profit_without_shift * row[2]

    #print("Доходность без смещения: ", profit_without_shift)
    
    return profit_without_shift, trades_without_shift

def get_profit_with_shift(df):    
    quotes_with_extrems = df.copy(deep = True)
    
    
    #Трейды со смещением

    trades_with_shift = []

    current_position = 'close'
    current_open_price = 0
    
    last_trend = None

    iter_count = 0
    for i, quote in quotes_with_extrems.iterrows():

        if current_position == 'close':
            if (quote['Trend'] == 'buy') & (last_trend == 'buy'):
                current_position = 'open'
                try:
                    #current_open_price = quotes_with_extrems.iloc[iter_count+1]['Close']
                    current_open_price = quotes_with_extrems.iloc[iter_count]['Close']
                except:
                    current_open_price = quotes_with_extrems.iloc[iter_count]['Close']

        if current_position == 'open':
            
            if (stop_loss_flag) & (current_open_price != quote['Close']):
                profit_num = ((quote['Close']/current_open_price) - 1)*100
                #print(profit_num)
                
                if profit_num <= stop_loss:
                    current_position = 'close'
                    profit = quote['Close']/current_open_price
                    trades_with_shift.append([current_open_price, quote['Close'], profit])
            
            
            if ((quote['Trend'] == 'sell') & (last_trend == 'sell')) | (iter_count+1 == quotes_with_extrems.shape[0]):
                current_position = 'close'

                try:
                    profit = quotes_with_extrems.iloc[iter_count]['Close']/current_open_price 
                    trades_with_shift.append([current_open_price, quotes_with_extrems.iloc[iter_count]['Close'], profit])
                except:
                    profit = quotes_with_extrems.iloc[iter_count]['Close']/current_open_price 
                    trades_with_shift.append([current_open_price, quotes_with_extrems.iloc[iter_count]['Close'], profit])

        iter_count = iter_count + 1
        last_trend = quote['Trend']
        
    #Доходность со смещением

    profit_with_shift = 1

    for row in trades_with_shift:
        profit_with_shift = profit_with_shift * row[2]
    
    return profit_with_shift, trades_with_shift

def get_strategy_inf(dataset, ref):

    results = {}
    
    dataset = dataset.dropna(subset = ['Close'])

    #Волатильность актива
    volat = dataset.ta.stdev(length=20).max()
    #print("Максимальная волатильность по стандартному отклонению на периоде = 20 дней: ", volat)

    std = dataset['Close'].std()
    print("Волатильность по стандартному отклонению по всей выборке: ", std)
    results['std'] = std

    #Анализ инвестиционной доходности
    start = dataset.head(1)['Close'].values[0]
    end = dataset.tail(1)['Close'].values[0]

    invest_profit = 100*(end-start)/start
    print("Доходность по стратегии buy&hold: ", invest_profit, '%')

    min_price = dataset['Close'].min()
    print("Максимальная просадка по стратегии buy&hold: ", 100*(min_price-start)/start, '%')
    results['max_risk'] = 100*(min_price-start)/start

    dataset['dyn_invest_profit'] = 100*(dataset['Close']-start)/start

    std_invest_profit = dataset['dyn_invest_profit'].std()

    print("Волатильность доходности стратегии buy&hold по стандартному отклонению: ", std_invest_profit)
    results['buy_hold_std'] = std_invest_profit

    sharp_invest = (invest_profit-ref)/std_invest_profit
    print("Коэффициент Шарпа стратегии buy&hold: ", sharp_invest)
    results['buy_hold_sharp'] = sharp_invest


    ideal_profit = 100*get_ideal_profit(dataset)[0]-100
    profit_with_shift = 100*get_profit_with_shift(dataset)[0]-100
    print("Доходность стратегии по разметке (без смещения): ", ideal_profit, '%')
    results['strategy_profit_without_shift'] = ideal_profit
    print("Доходность стратегии по разметке (со смещением): ", profit_with_shift, '%')
    results['strategy_profit_with_shift'] = profit_with_shift
    
    dataset['buy_ideal_price'] = np.where(dataset['extr'] == 'min', dataset['Close'], None)
    dataset['buy_shift_price'] = np.where(dataset['extr'].shift(1) == 'min', dataset['Close'], None)
    
    dataset['buy_ideal_price'] = dataset['buy_ideal_price'].fillna(method = 'ffill')
    dataset['buy_shift_price'] = dataset['buy_shift_price'].fillna(method = 'ffill')
    
    dataset['dyn_current_trade_ideal_profit'] = 100*(dataset['Close']-dataset['buy_ideal_price'])/dataset['buy_ideal_price']
    dataset['dyn_current_trade_shift_profit'] = 100*(dataset['Close']-dataset['buy_shift_price'])/dataset['buy_shift_price']
    
    dataset['dyn_previous_trade_ideal_profit']=0
    dataset['dyn_previous_trade_shift_profit']=0
    
    dyn_previous_trade_ideal_profit_arr = []
    count = 0
    last_profit = 0
    for i, row in dataset.iterrows():
        if (row['extr'] == 'max'):
            if not math.isnan(row['dyn_current_trade_ideal_profit']):
                if len(dyn_previous_trade_ideal_profit_arr) == 0:
                    last_profit = 1+row['dyn_current_trade_ideal_profit']/100
                    dyn_previous_trade_ideal_profit_arr.append(last_profit)
                else:
                    last_profit = (1+row['dyn_current_trade_ideal_profit']/100)*last_profit
                    dyn_previous_trade_ideal_profit_arr.append(last_profit)
        dataset.at[i, 'dyn_previous_trade_ideal_profit'] = last_profit
        count = count+1


    dyn_previous_trade_shift_profit_arr = []
    last_row = ''
    count = 0
    last_profit = 0
    for i, row in dataset.iterrows():
        if (last_row == 'max') :
            if not math.isnan(row['dyn_current_trade_shift_profit']):
                if len(dyn_previous_trade_shift_profit_arr) == 0:
                    last_profit = 1+row['dyn_current_trade_ideal_profit']/100
                    dyn_previous_trade_shift_profit_arr.append(last_profit)
                else:
                    last_profit = (1+row['dyn_current_trade_shift_profit']/100)*last_profit
                    dyn_previous_trade_shift_profit_arr.append(last_profit)
        last_row = row['extr']
        dataset.at[i, 'dyn_previous_trade_shift_profit'] = last_profit
        count = count+1
            
    dataset['dyn_trade_ideal_profit'] = np.where(dataset['dyn_previous_trade_ideal_profit'] != 0, ((1+dataset['dyn_current_trade_ideal_profit']/100)*dataset['dyn_previous_trade_ideal_profit']-1)*100,0)
    
    dataset['dyn_trade_shift_profit'] = np.where(dataset['dyn_previous_trade_shift_profit'] != 0, ((1+dataset['dyn_current_trade_shift_profit']/100)*dataset['dyn_previous_trade_shift_profit']-1)*100,0)
    
    
    std_ideal_trade_profit = dataset['dyn_trade_ideal_profit'].std()

    print("Волатильность доходности идеальной trade стратегии по стандартному отклонению: ", std_ideal_trade_profit)
    results['strategy_std_without_shift'] = std_ideal_trade_profit

    std_shift_trade_profit = dataset['dyn_trade_shift_profit'].std()

    print("Волатильность доходности shift trade стратегии по стандартному отклонению: ", std_shift_trade_profit)
    results['strategy_std_with_shift'] = std_shift_trade_profit

    sharp_ideal_trade = (ideal_profit-ref)/std_ideal_trade_profit
    print("Коэффициент Шарпа trade идеальной стратегии: ", sharp_ideal_trade)
    results['strategy_sharp_without_shift'] = sharp_ideal_trade

    sharp_shift_trade = (profit_with_shift-ref)/std_shift_trade_profit
    print("Коэффициент Шарпа trade shift стратегии: ", sharp_shift_trade)
    results['strategy_sharp_with_shift'] = sharp_shift_trade

    print("Максимальной просадка trade идеальной стратегии: ", dataset[
        (dataset['Trend'] == 'buy')
        | (dataset['extr'] == 'max')
    ]['dyn_current_trade_ideal_profit'].min())

    print("Максимальной просадка trade shift стратегии: ", dataset[
        ((dataset['Trend'] == 'buy')
        | (dataset['extr'] == 'max'))
        & (dataset['extr'] != 'min')
    ]['dyn_current_trade_shift_profit'].min())

    print("Количество сделок идеальной торговли: ", len(get_ideal_profit(dataset)[1]))
    results['strategy_trade_count_without_shift'] = len(get_ideal_profit(dataset)[1])
    print("Количество сделок торговли со смещением: ", len(get_profit_with_shift(dataset)[1]))
    results['strategy_trade_count_with_shift'] = len(get_profit_with_shift(dataset)[1])
    
    return dataset, results


#ticker = 'SBER'
quotes_temp = Ticker(ticker)
# Свечи по акциям за период
quotes_1d = quotes_temp.candles(date = start_date, till_date = end_date, period=interval)

def main (ticker):
    
    #КОТИРОВКИ!
    quotes_temp = Ticker(ticker)
    # Свечи по акциям за период
    quotes_1d = quotes_temp.candles(date = start_date, till_date = end_date, period=interval)
    #quotes_1d.head()
    quotes_1d = pd.DataFrame(quotes_1d)
    
    quotes_1d.rename(
        columns = {
            'begin' : 'Datetime',
            'open' : 'Open',
            'close' : 'Close',
            'high' : 'High',
            'low' : 'Low',
            'volume' : 'Volume'
        }, inplace = True
    )
    quotes_1d.index = quotes_1d['Datetime']
    quotes_1d.sort_index(ascending=True, inplace = True)

    #Получаем экстремумы по дневному графику
    print('Получаем экстремумы по дневному графику')
    quotes_1d_with_extrems = get_extrems(quotes_1d, delete_not_marking_data, count_points = count_points)

    #Размечаем Y по дневному графику
    quotes_1d_with_Y = quotes_with_Y(quotes_1d_with_extrems, extr_bar_count, Y_shift, max_unmark = max_unmark)

    #Очищаем не размеченные данные
    quotes_1d_with_Y = quotes_1d_with_Y.dropna(subset = ['Y'])

    #Получаем данные индикаторов котировок дневного датафрейма
    quotes_1d_indicators = get_indicators(quotes_1d_with_Y, prefix = ':5m')

    #Получаем stoch датасет для котировок дневного таймфрейма
    stoch_quotes_1d_dataset = get_stoch_indicators(quotes_1d_indicators, prefix = ':5m')

    #Получаем датасет логики над стохастиком для котировок дневного таймфрейма
    stoch_logic_quotes_1d_dataset = get_stoch_logic_data(stoch_quotes_1d_dataset, prefix = ':5m')
    
    #Получаем нормализованный числовой датасет для котировок дневного таймфрейма
    norm_num_dataset_quotes_1d = norm_num_df(quotes_1d_indicators, prefix = ':5m')

    #Свечной анализ
    cdl_dataset_quotes_1d = quotes_1d.ta.cdl_pattern(name="all")

    #Датасет волн
    waves_dataset_quotes_1d =  waves_dataset(quotes_1d_indicators, prefix = ':5m')

    #Логический датасет
    logic_dataset_quotes_1d =  logic_dataset(quotes_1d_indicators, prefix = ':5m')
    
    #Собираем датасеты
    num_logic_df = pd.DataFrame()
    
    #Формируем индекс по древным котировкам
    num_logic_df.index = quotes_1d.index
    
    #Инициализируем поля
    num_logic_df['Close'] = quotes_1d_with_Y['Close']
    num_logic_df['Y'] = quotes_1d_with_Y['Y']
    
    
    #Джойним датасеты
    num_logic_df = num_logic_df.join(norm_num_dataset_quotes_1d, lsuffix='_left_num_qout_5m', rsuffix='_right_num_qout_5m')#Нормализованные дневные котировки
    
    num_logic_df = num_logic_df.join(waves_dataset_quotes_1d, lsuffix='_left_num_qout_5m', rsuffix='_right_num_qout_5m')
    
    num_logic_df = num_logic_df.join(cdl_dataset_quotes_1d, lsuffix='_left_num_qout_5m', rsuffix='_right_num_qout_5m')
    
    num_logic_df = num_logic_df.join(stoch_quotes_1d_dataset, lsuffix='_left_stoch_qout_5m', rsuffix='_right_stoch_qout_5m')
    
    num_logic_df = num_logic_df.join(stoch_logic_quotes_1d_dataset, lsuffix='_left_stoch_qout_5m', rsuffix='_right_stoch_qout_5m')
    
    num_logic_df = num_logic_df.join(logic_dataset_quotes_1d, lsuffix='_left_logic_qout_5m', rsuffix='_right_logic_qout_5m')
    
    
    #Заполняем пустые ячейки предыдущими значениями
    num_logic_df = num_logic_df.fillna(method="ffill")
     
    #Добавляем лаги
    #num_df
    columns = num_logic_df.columns.values   
    for col in columns:
        if col not in ['Close', 'Y']:
            try:
                for i in range(1,lag_count):
                    num_logic_df[col+'shift_'+str(i)] = num_logic_df[col].copy(deep = True).shift(i)
            except:
                #print("Ошибка добавления лага в колонке: ", col)
                pass
    
    
    #Чистим от пустых значений
    num_logic_df = num_logic_df.dropna()
    
    #Конвертируем индексы
    num_logic_df.index = num_logic_df.index.astype(int)
    
    return num_logic_df

def date_filter_1(quotes, filter_data_timezone, filter_data_start, filter_data_end):
    import datetime
    import pytz
    
    tz_ny= pytz.timezone(filter_data_timezone)

    date1 = datetime.datetime.strptime(filter_data_start, '%Y-%m-%d %H:%M:%S')
    date1 = tz_ny.localize(date1)
    date2 = datetime.datetime.strptime(filter_data_end, '%Y-%m-%d %H:%M:%S')
    date2 = tz_ny.localize(date2)

    # select desired range of dates
    try:
        quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]
    except:
        try:
            date1 = np.datetime64(date1)
            date2 = np.datetime64(date2)
            quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]
        except:
            pass
    
    return quotes

#Подготовка данных
def prepade_df(df, dataset):
    
    init_data_train = df

    # Устанавливаем размерность датасетов
    n_train = init_data_train.shape[0]
    p_train = init_data_train.shape[1]
    print("Число факторов: ", p_train)
    # Формируем данные в numpy-массив
    init_data_train = init_data_train.values
    # Подготовка данных для обучения и тестирования (проверки)
    print("Подготавливаем выборки")
    train_start = 0
    train_end = n_train
    data_train = init_data_train[np.arange(train_start, train_end), :]
    #Выбор данных
    print("Выбираем данные")
    trainX = data_train[:, 2:]
    trainY = data_train[:, 1]
    train_quotes_close = data_train[:, 0]

    #Изменяем размерность массива, для обеспечения возможности масштабирования Y
    trainY = trainY.reshape(-1, 1)
    train_quotes_close = train_quotes_close.reshape(-1, 1)
    
    if scale_flag:
        #Загружаем скалер
        x_scaler = joblib.load('./'+scaler_path+'/scaler_'+dataset+'.save')
        
        trainX = x_scaler.transform(trainX)
        
    #Изменяем размерность массива Х, для рекурентной нейросети
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        
    return trainX, trainY, train_quotes_close

#Расчёт на основании модели
def calc_signals(model, trainX, trainY, train_quotes_close):
    
    print("Предсказываем результат")
    predict_trainY = model.predict(trainX, verbose = 1)

    #Преобразовываем выходные сигналы тренировочной выборки

    result_predict_trainY = []

    for predict in predict_trainY:
        result_predict_trainY.append(np.argmax(predict))

    result_predict_trainY = np.array(result_predict_trainY)
    
    np_result_Y = np.rint(result_predict_trainY)

        #Расчёт трендов по разметке
    last_train_signal = 2
    trends_origin = array('f', []) #Массив ожидаемых данных по тренду
    for i in range(trainY.shape[0]):
        if trainY[i] != last_train_signal and (trainY[i] == 2 or trainY[i] == 0):
            last_train_signal = trainY[i]
        trends_origin.insert(i,last_train_signal)
    
    #Расчёт трендов для расчётных значений
    last_test_signal = 2
    trends_predict = array('f', []) #Массив ожидаемых данных по тренду
    for i in range(len(np_result_Y)):
        if np_result_Y[i] != last_test_signal and (np_result_Y[i] == 2 or np_result_Y[i] == 0):
            last_test_signal = np_result_Y[i]
        trends_predict.insert(i,last_test_signal)
    
    trends_origin = np.asarray(trends_origin).astype(int)
    trends_predict = np.asarray(trends_predict).astype(int)
        
    f1_metric = f1_score(trends_origin, trends_predict, pos_label=2)
    
    return np_result_Y, trends_predict, trends_origin, f1_metric


# # Загружаем нейронные сети

#загружаем инвестиционные нейронные сети "neurals_tech_for_investing_signals"
model_num_logic = load_model('./'+neural_path+'/ansamble_num_logic_1d_1w_v1.h5', compile=False)
model_num_logic.compile() #Paste it here


# # Загружаем новый тикер и обрабатываем его

print("Начинаем обработку нового тикера: ", ticker, datetime.datetime.now())
print("Получаем датасеты")
temp = main(ticker)

#Предобрабатываем датасеты
print("Предобрабатываем датасеты")
num_logic_for_neurals = prepade_df(temp, 'num_logic_1d_1w')

#Расчёт сигналов
ansamble_signals_temp = calc_signals(model_num_logic, num_logic_for_neurals[0], num_logic_for_neurals[1], num_logic_for_neurals[2])
ansamble_signals = ansamble_signals_temp[0]

f1_metric = ansamble_signals_temp[3]


# # Смотрим разметку

# Акции
quotes_temp = Ticker(ticker)
# Свечи по акциям за период
quotes_1d = quotes_temp.candles(date = start_date, till_date = end_date, period=interval)
quotes_1d = pd.DataFrame(quotes_1d)

quotes_1d.rename(
    columns = {
        'begin' : 'Datetime',
        'open' : 'Open',
        'close' : 'Close',
        'high' : 'High',
        'low' : 'Low',
        'volume' : 'Volume'
    }, inplace = True
)
quotes_1d.index = quotes_1d['Datetime']
quotes_1d.sort_index(ascending=True, inplace = True)

dataset_trade_quotes_with_extrems = get_extrems(quotes_1d, delete_not_marking_data, count_points).copy(deep = True)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#СМОТРИМ РЕЗУЛЬТАТЫ РАЗМЕТКИ!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
dataset_trade_quotes_with_extrems = show(dataset_trade_quotes_with_extrems)

len_dataset = dataset_trade_quotes_with_extrems.shape[0]
len_dataset


# # Смотрим сигналы по разметке и ансамблю

try:
    if is_notebook():
        fig, ax = plt.subplots()
        ax.set_title('Сигналы по разметке и расчётам ансамбля')


        y = ansamble_signals_temp[2][-len_dataset:]#Реальные значения
        y1 = ansamble_signals_temp[1][-len_dataset:]#Расчетные значения
        y1 = y1+3
        y2 = ansamble_signals_temp[0][-len_dataset:]
        y2 = y2+6

        plt.plot(y, label='Размеченые данные')
        plt.plot(y1, label='Тренды нейронной сети')
        plt.plot(y2, label='Сигналы нейронной сети')
        #plt.title('Тренировочная выборка')
        plt.legend(loc="lower right")
        #singals_example = plt_to_png(plt)
        plt.show()
        #plt.close()
except:
    pass

# # Смотрим показатели точности нейронной сети
def toFixed(numObj, digits=0):
    return f"{100*numObj:.{digits}f}"

def toFixed1(numObj, digits=0):
    return f"{numObj:.{digits}f}"

test_accuracy_score = toFixed(accuracy_score(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:]), 2)
test_roc_auc_score = toFixed1(roc_auc_score(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:]), 2)
test_precision_score = toFixed(precision_score(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:], pos_label=2), 2)
test_recall_score = toFixed(recall_score(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:], pos_label=2), 2)
test_f1_score = toFixed(f1_score(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:], pos_label=2), 2)
test_log_loss = toFixed1(log_loss(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:]), 2)

print('accuracy, %:', toFixed(accuracy_score(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:]), 2))
#print('roc-auc:', toFixed(roc_auc_score(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:]), 2))
print('roc-auc:', toFixed1(roc_auc_score(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:]), 2))
print('precision, %:', toFixed(precision_score(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:], pos_label=2), 2))
print('recall, %:', toFixed(recall_score(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:], pos_label=2), 2))
print('f1, %:', toFixed(f1_score(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:], pos_label=2), 2))
print('logloss:', toFixed1(log_loss(ansamble_signals_temp[2][-len_dataset:], ansamble_signals_temp[1][-len_dataset:]), 2))

# # Расчёт бизнес-метрик по разметке
#Ставка рефинансирования
ref = 4.5
temp = get_strategy_inf(dataset_trade_quotes_with_extrems, ref)
result_ideal_strategy = temp[0]

results_ideal_strategy = temp[1]
results_ideal_strategy

#Динамика доходности портфеля сложным процентом
result_ideal_strategy[result_ideal_strategy['Trend'] == 'buy'].tail(3)

result_ideal = result_ideal_strategy.copy(deep = True)
result_ideal['dyn_current_trade_ideal_profit'] = np.where(
    result_ideal['Trend'] == 'buy',
    result_ideal['dyn_current_trade_ideal_profit'],
    0
)
result_ideal['dyn_trade_ideal_profit'] = np.where(
    result_ideal['Trend'] == 'buy',
    result_ideal['dyn_trade_ideal_profit'],
    None
)
result_ideal['dyn_trade_ideal_profit'] = result_ideal['dyn_trade_ideal_profit'].fillna(method = 'ffill')

try:
    if is_notebook():
        #Смотрим динамику доходности идеальной торговли
        fig, ax = plt.subplots()
        ax.set_title('Динамика доходности идеальной торговли')

        y = result_ideal['dyn_current_trade_ideal_profit']

        plt.plot(y, label='Доходность')
        plt.legend(loc="lower right")
        dyn_ideal_trading = plt_to_png(plt)
        plt.show()
        #plt.close()
except:
    pass

try:
    if is_notebook():
        #Смотрим динамику доходности идеального портфеля
        fig, ax = plt.subplots()
        ax.set_title('Динамика доходности идеального портфеля')

        y = result_ideal['dyn_trade_ideal_profit']

        plt.plot(y, label='Доходность')
        plt.legend(loc="lower right")
        dyn_ideal_portfel = plt_to_png(plt)
        plt.show()
        #plt.close()
except:
    pass


# # Расчёт бизнес-метрик по расчётам нейронной сети
#делаем переразметку относительно засчётных данных
calc_dataset = dataset_trade_quotes_with_extrems.copy(deep = True)

#Добавляем поле с сигналами и трендами
try:
    calc_dataset['signals'] = ansamble_signals_temp[0][-len_dataset:]
    calc_dataset['trends'] = ansamble_signals_temp[1][-len_dataset:]
except:
    calc_dataset = calc_dataset[-ansamble_signals_temp[0].shape[0]:]
    calc_dataset['signals'] = ansamble_signals_temp[0]
    calc_dataset['trends'] = ansamble_signals_temp[1]

#Переопределяем поля разметки

calc_dataset['extr'] = None

last_signal = 1

for i, row in calc_dataset.iterrows():
    if (row['signals'] != last_signal) & (row['signals'] != 1):
        if row['signals'] == 2:
            calc_dataset.at[i, 'extr'] = 'min'
        elif row['signals'] == 0:
            calc_dataset.at[i, 'extr'] = 'max'
                                          
        last_signal = row['signals']

calc_dataset.tail(3)

calc_dataset['Trend'] = None
calc_dataset['Trend'] = np.where(calc_dataset['trends'] == 2, 'buy',calc_dataset['Trend'])
calc_dataset['Trend'] = np.where(calc_dataset['trends'] == 0, 'sell',calc_dataset['Trend'])
calc_dataset.tail(3)

temp = get_strategy_inf(calc_dataset, ref)

result_calc_strategy = temp[0]

results_calc_strategy = temp[1]

results_calc_strategy

result_calc = result_calc_strategy.copy(deep = True)
result_calc['dyn_current_trade_ideal_profit'] = np.where(
    result_calc['Trend'] == 'buy',
    result_calc['dyn_current_trade_ideal_profit'],
    0
)
result_calc['dyn_trade_ideal_profit'] = np.where(
    result_calc['Trend'] == 'buy',
    result_calc['dyn_trade_ideal_profit'],
    None
)
result_calc['dyn_trade_ideal_profit'] = result_calc['dyn_trade_ideal_profit'].fillna(method = 'ffill')

try:
    if is_notebook():
        #Смотрим динамику доходности торговли по нейронным сетям
        fig, ax = plt.subplots()
        ax.set_title('Динамика доходности торговли по нейронным сетям')

        y = result_calc['dyn_current_trade_ideal_profit']

        plt.plot(y, label='Доходность')
        plt.legend(loc="lower right")
        dyn_neural_trading = plt_to_png(plt)
        plt.show()
        #plt.close()
except:
    pass

try:
    if is_notebook():
        #Смотрим динамику доходности портфеля с нейронными сетями
        fig, ax = plt.subplots()
        ax.set_title('Динамика доходности портфеля с нейронными сетями')

        y = result_calc['dyn_trade_ideal_profit']

        plt.plot(y, label='Доходность')
        plt.legend(loc="lower right")
        dyn_neural_portfel = plt_to_png(plt)
        plt.show()
        #plt.close()
except:
    pass

np_signals = result_calc['signals'].values

#Расчёт трендов для тренировочной выборки на основе сигналов по разметке
last_signal = 2
np_neural_trends = array('f', []) #Массив ожидаемых данных по тренду
for i in range(np_signals.shape[0]):
    if np_signals[i] != last_signal and (np_signals[i] == 2 or np_signals[i] == 0):
        last_signal = np_signals[i]
    np_neural_trends.insert(i,last_signal)

result_calc['neural_trends'] = np_neural_trends


output_data = result_calc[['Open', 'Close', 'High', 'Low', 'value', 'Volume', 'Datetime',
       'extr', 'Trend', 'neural_trends']].rename(columns = {
    'Trend':'Разметка',
})


output_data['neural_trends'] = np.where(output_data['neural_trends'] == 2.0, 1.0, output_data['neural_trends'])

#output_data.to_csv('results/SBER_results.csv')


# # Сохранение результатов

result_ideal_df = result_ideal[['Datetime', 'dyn_current_trade_ideal_profit', 'dyn_trade_ideal_profit']]

result_calc_df = result_calc_strategy[['Datetime', 'dyn_current_trade_ideal_profit', 'dyn_trade_ideal_profit']]

result = {
    'task_id': task_id,
    'singals_example': {
        'markup_signals': {
            'description': 'Сигнлаы про разметке',
            'values': ansamble_signals_temp[2][-len_dataset:].tolist()
        },
        'neural_signals': {
            'description': 'Сигнлаы нейронной сети',
            'values': ansamble_signals_temp[0][-len_dataset:].tolist()
        },
        'neural_trends': {
            'description': 'Тренды нейронной сети',
            'values': ansamble_signals_temp[1][-len_dataset:].tolist()
        }
    },
    'test_accuracy_score': {
        'description': 'Показатели точности датасета по метрике accuracy',
        'value': float(test_accuracy_score)
    },
    'test_roc_auc_score': {
        'description': 'Показатели точности датасета по метрике roc_auc',
        'value': float(test_roc_auc_score)
    },
    'test_precision_score': {
        'description': 'Показатели точности датасета по метрике precision',
        'value': float(test_precision_score)
    },
    'test_recall_score': {
        'description': 'Показатели точности датасета по метрике recall',
        'value': float(test_recall_score)
    },
    'test_f1_score': {
        'description': 'Показатели точности датасета по метрике f1',
        'value': float(test_f1_score)
    },
    'test_log_loss': {
        'description': 'Показатели точности датасета по метрике log_loss',
        'value': float(test_log_loss)
    },

    'data_std': {
        'description': 'Стандартное отклонение по всей выборке',
        'value': results_ideal_strategy['std']
    },
    'max_risk': {
        'description': 'Максимальная просадка',
        'value': results_ideal_strategy['max_risk']
    },
    'buy_hold_std': {
        'description': 'Стандартное отклонение стратегии buy&hold',
        'value': results_ideal_strategy['buy_hold_std']
    },
    'buy_hold_sharp': {
        'description': 'Коэффициент шарпа стратегии buy&hold',
        'value': results_ideal_strategy['buy_hold_sharp']
    },
    'ideal_strategy_profit_without_shift': {
        'description': 'Доходность стратегии по разметке',
        'value': results_ideal_strategy['strategy_profit_without_shift']
    },
    'ideal_strategy_profit_with_shift': {
        'description': 'Доходность стратегии по разметке со мещением на 1 бар',
        'value': results_ideal_strategy['strategy_profit_with_shift']
    },
    'ideal_strategy_std_without_shift': {
        'description': 'Стандартное отклонение стратегии по разметке',
        'value': results_ideal_strategy['strategy_std_without_shift']
    },
    'ideal_strategy_std_with_shift': {
        'description': 'Стандартное отклонение стратегии по разметке со мещением на 1 бар',
        'value': results_ideal_strategy['strategy_std_with_shift']
    },
    'ideal_strategy_sharp_without_shift': {
        'description': 'Коэффициент Шарпа стратегии по разметке',
        'value': results_ideal_strategy['strategy_sharp_without_shift']
    },
    'ideal_strategy_sharp_with_shift': {
        'description': 'Коэффициент Шарпа стратегии по разметке со мещением на 1 бар',
        'value': results_ideal_strategy['strategy_sharp_with_shift']
    },
    'ideal_strategy_trade_count_without_shift': {
        'description': 'Число сделок стратегии по разметке',
        'value': results_ideal_strategy['strategy_trade_count_without_shift']
    },
    'ideal_strategy_trade_count_with_shift': {
        'description': 'Число сделок стратегии по разметке со мещением на 1 бар',
        'value': results_ideal_strategy['strategy_trade_count_with_shift']
    },

    'neural_strategy_profit_without_shift': {
        'description': 'Доходность стратегии нейронной сети',
        'value': results_calc_strategy['strategy_profit_without_shift']
    },
    'neural_strategy_profit_with_shift': {
        'description': 'Доходность стратегии нейронной сети при смещении на 1 бар',
        'value': results_calc_strategy['strategy_profit_with_shift']
    },
    'neural_strategy_std_without_shift': {
        'description': 'Стандартное отклонение стратегии нейронной сети',
        'value': results_calc_strategy['strategy_std_without_shift']
    },
    'neural_strategy_std_with_shift': {
        'description': 'Стандартное отклонение стратегии нейронной сети при смещении на 1 бар',
        'value': results_calc_strategy['strategy_std_with_shift']
    },
    'neural_strategy_sharp_without_shift': {
        'description': 'Коэффициент Шарпа стратегии нейронной сети',
        'value': results_calc_strategy['strategy_sharp_without_shift']
    },
    'neural_strategy_sharp_with_shift': {
        'description': 'Коэффициент Шарпа стратегии нейронной сети при смещении на 1 бар',
        'value': results_calc_strategy['strategy_sharp_with_shift']
    },
    'neural_strategy_trade_count_without_shift': {
        'description': 'Число сделок стратегии нейронной сети',
        'value': results_calc_strategy['strategy_trade_count_without_shift']
    },
    'neural_strategy_trade_count_with_shift': {
        'description': 'Число сделок стратегии нейронной сети при смещении на 1 бар',
        'value': results_calc_strategy['strategy_trade_count_with_shift']
    },

    'dyn_ideal_trading': {
        'description': 'Динамика доходности стратегии по разметке',
        'value': {
            'Datetime': result_ideal_df['Datetime'].values.tolist(),
            'dyn_trades_profit': result_ideal_df['dyn_current_trade_ideal_profit'].fillna(0).values.tolist(),
            'dyn_portfel_profit': result_ideal_df['dyn_current_trade_ideal_profit'].fillna(0).values.tolist(),
        }
    },
    'dyn_neural_trading': {
        'description': 'Динамика доходности нейронной сети',
        'value': {
            'Datetime': result_calc_df['Datetime'].values.tolist(),
            'dyn_trades_profit': result_calc_df['dyn_current_trade_ideal_profit'].fillna(0).values.tolist(),
            'dyn_portfel_profit': result_calc_df['dyn_current_trade_ideal_profit'].fillna(0).values.tolist(),
        }
    }
}

# with open('results/calc_profit.json', 'w') as f:
#     json.dump(result, f)

count = 0

while True:
    try:
        url = 'http://'+respos_url+'/api/v1/task/complied'
        response = requests.post(url, json = json.dumps(result), headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print("Запрос успешно отправлен:")
            break
    except Exception as err:
        print("Ошибка отправка запроса на API:", err)
    
    #Делаем повторные попытки в случае ошибки
    if count >= 5:
        break
        
    count += 1    

