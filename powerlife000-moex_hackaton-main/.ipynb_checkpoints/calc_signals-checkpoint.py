#!/usr/bin/env python
# coding: utf-8
# %%

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
import io
from PIL import Image
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
from sqlalchemy import create_engine
import argparse
import psycopg2
import base64
import json
from moexalgo import Market, Ticker
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
pd.options.mode.chained_assignment = None  # default='warn'

# %matplotlib qt


# # Импортируем модули
import sys, signal

def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

sys.path.insert(0, 'modules')

#Системные модули
from DB_module import DB
from Config_module import Config

global_config = Config()

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
    _ = parser.add_argument('--ticker')
    _ = parser.add_argument('--scaler_path')
    _ = parser.add_argument('--neural_path')
    _ = parser.add_argument('--timeframe')
    _ = parser.add_argument('--count_points')
    _ = parser.add_argument('--extr_bar_count')
    _ = parser.add_argument('--max_unmark')
    _ = parser.add_argument('--count_days')
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
            with open('app/configs/1D/calc_signals.json', 'r', encoding='utf_8') as cfg:
                temp_data=cfg.read()

    # parse file`
    config = json.loads(temp_data)
    
    task_id = str(config['task_id'])
    #Список тикеров для генерации сигналов
    tickers = config['tickers']
    #Путь для сохранения скалера
    scaler_path = config['scaler_path'] #Путь должен быть без чёрточки в конце
    #Путь для сохранения нейронных сетей
    neural_path = config['neural_path'] #Путь должен быть без чёрточки в конце
    interval = config['timeframe']
    count_points = config['count_points'] #Параметр разметки экстремумов
    extr_bar_count = config['extr_bar_count'] #Сколько баров размечаем для генерации сигналов
    #Максимальное количество конечных баров волны в %, которые не размечаем
    max_unmark = config['max_unmark']
    #Число дней в датасете
    count_days = config['count_days']
    if config['respos_url']:
        respos_url = config['respos_url']
    else:
        respos_url = '127.0.0.1:8080'
    
if load_params_from_command_line:
    task_id = str(args.task_id)
    tickers = args.ticker.replace(']',"").replace('[',"").replace('"',"").replace("'","").split(",")
    scaler_path = str(args.scaler_path)
    neural_path = str(args.neural_path) 
    interval = str(args.timeframe)
    count_points = int(args.count_points) 
    extr_bar_count = int(args.extr_bar_count) 
    max_unmark = float(args.max_unmark) 
    count_days = int(args.count_days)
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

#По какому количеству открытых позиций нужно проходить?
open_positions_count = 5

#Флаг необходимости удаления не размеченных данных
delete_not_marking_data = False

#Максимальное количество конечных баров волны в %, которые не размечаем
max_unmark = 0.33

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

def main (ticker, start_date, end_date):
    
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
    
    quotes_1d = quotes_1d[:-1]

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


# %%


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

ticker_count = 0
def get_new_ticker():
    global ticker_count
    ticker = tickers[ticker_count]
    
    ticker_count += 1
    
    if ticker_count >=  len(tickers):
        ticker_count = 0
    
    return ticker


# # Загружаем нейронные сети
#загружаем инвестиционные нейронные сети "neurals_tech_for_investing_signals"
model_num_logic = load_model('./'+neural_path+'/ansamble_num_logic_1d_1w_v1.h5', compile=False)
model_num_logic.compile() #Paste it here


# # Делаем запись о задаче по запуску сервиса
#Соединение с БД
def connect():
    return psycopg2.connect(
        host=global_config.db_host,
        database=global_config.db_database,
        user=global_config.db_user,
        password=global_config.db_password
    )
conn = connect()
conn.close()


# # Загружаем новый тикер и обрабатываем его
while True:
    try:
        #Получаем новый тикер для обработки
        try:
            ticker = get_new_ticker()
        except KeyboardInterrupt:
            print("Keyboard interrupt exception caught")
            break
        except Exception as e:
            print("Ошибка получения тикера из БД: ", datetime.datetime.now(), ' e: ', e)
            continue
            
        #Опеределяем начальную и конечную даты для фильтрации
        start_date = datetime.datetime.today() - datetime.timedelta(days=count_days)
        end_date = datetime.datetime.today() - datetime.timedelta(days=0)

        #Преобразовываем в стринги
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")
            
        if ticker != None:
            start_date_1 = datetime.datetime.now()
            print("Начинаем обработку нового тикера: ", ticker, start_date_1)
            
            #Получаем датасеты
            try:
                print("Получаем датасеты")
                temp = main(ticker, start_date, end_date)
            except KeyboardInterrupt:
                print("Keyboard interrupt exception caught")
                break
            except Exception as e:
                print("Ошибка получения датасетов: ", datetime.datetime.now(), ' e: ', e)
                continue
                
            try:
                #Предобрабатываем датасеты
                print("Предобрабатываем датасеты")
                num_logic_for_neurals = prepade_df(temp, 'num_logic_1d_1w')
            except KeyboardInterrupt:
                print("Keyboard interrupt exception caught")
                break
            except Exception as e:
                print("Ошибка предобработки датасетов: ", datetime.datetime.now(), ' e: ', e)
                continue
                
            
            try:
                #Расчёт сигналов
                ansamble_signals_temp = calc_signals(model_num_logic, num_logic_for_neurals[0], num_logic_for_neurals[1], num_logic_for_neurals[2])
                ansamble_signals = ansamble_signals_temp[0]

                f1_metric = ansamble_signals_temp[3]

                f1_metric = ansamble_signals_temp[3]
            except KeyboardInterrupt:
                print("Keyboard interrupt exception caught")
                break
            except Exception as e:
                print("Ошибка расчёта сигналов: ", datetime.datetime.now(), ' e: ', e)
                continue
                
                
                
            try:
                #Записываем сигнал в базу данных
                print("Записываем сигнал в базу данных")
                stoch_signal = None
                last_stoch_signal = None
                num_signal = None
                last_num_signal = None
                logic_signal = None
                last_logic_signal = None

                df_ansamble = pd.DataFrame(ansamble_signals)

                last_ansamble_signal = 1

                ansamble_signal_length = df_ansamble.shape[0]-1

                current_signal = None
                count_pos = 0

                for i,row in  df_ansamble.iterrows():

                    if ((row[0] == 0.0) | (row[0] == 2.0)) & (row[0] != current_signal):
                        current_signal = row[0]
                        count_pos = 0

                    count_pos += 1

                ansamble_signal_position = count_pos
                ansamble_signal = current_signal
                
                print(ansamble_signal_position, ansamble_signal)

                #Проверяем наличие записей в базе
                now = datetime.datetime.now() # current date and time
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                
                #Пытаемся записать результаты
                try:
                    if conn.closed == 1:
                        conn = connect()
                    #Проверяем наличие записи
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM public.cals_signals_results WHERE task_id = %s AND ticker = %s;", (task_id,ticker))
                    results = cur.fetchall()
                    cur.close()
                    
                    if conn.closed == 1:
                        conn = connect()
                    #Проверяем наличие записи
                    cur = conn.cursor()
                    
                    if len(results) == 0:
                        print("Записываем результаты")
                        #Записи о результатах в БД нет, записываем новый результат
                        cur.execute(
                            """
                            INSERT INTO public.cals_signals_results
                            (
                                task_id,
                                ticker,
                                signal,
                                signal_position
                            )
                            VALUES (%s, %s, %s, %s);
                            """,
                            (
                                task_id, 
                                ticker, 
                                ansamble_signal, 
                                ansamble_signal_position
                            )
                        )
                        conn.commit()
                    else:
                        #Обновляем запись
                        print("Обновляем результаты")
                        sql = """ UPDATE public.cals_signals_results
                                    SET 
                                    signal = %s,
                                    signal_position = %s
                                    WHERE task_id = %s AND ticker = %s """
                        cur.execute(sql, (
                                ansamble_signal, 
                                ansamble_signal_position,
                                task_id,
                                ticker
                            ))
                        conn.commit()
                    cur.close()
                    
                    #Отправляем результаты в API
                    result = {
                        'task_id': task_id,
                        'ticker': ticker,
                        'ansamble_signal': ansamble_signal, 
                        'ansamble_signal_position': ansamble_signal_position
                        
                    }
                    
                    count = 0
                    while True:
                        try:
                            url = 'http://'+respos_url+'/api/v1/task/complied'
                            response = requests.post(url, json = result)
                            if response.status_code == 200:
                                print("Запрос успешно отправлен:")
                                break
                        except Exception as err:
                            print("Ошибка отправка запроса на API:", err)

                        #Делаем повторные попытки в случае ошибки
                        if count >= 5:
                            break

                        count += 1 
                    
                except Exception as e:
                    print("Ошибка записи результатов в БД: ", e)
                    conn = connect()

                end_date = datetime.datetime.now()
                print("Тикер обработан и записан в базу: ", ticker, end_date)
                print("Время обработки: ", ticker, (end_date-start_date_1).total_seconds())
            except KeyboardInterrupt:
                print("Keyboard interrupt exception caught")
                break
            except Exception as e:
                print("Ошибка записи сигнала в БД: ", datetime.datetime.now(), ' e: ', e)
                continue
    except KeyboardInterrupt:
        print("Keyboard interrupt exception caught")
        break
    except Exception as e:
        print("Не учтённая ошибка: ", datetime.datetime.now(), ' e: ', e)
        continue

