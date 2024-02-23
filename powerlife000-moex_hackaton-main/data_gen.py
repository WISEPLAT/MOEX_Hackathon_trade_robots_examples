#!/usr/bin/env python
# coding: utf-8

# # Импортируем библиотеки

import datetime
import pytz
import os
from pathlib import Path
import requests
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import base64
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
import pandas_ta as ta
import numpy as np
import yfinance as yf
import pickle
from sklearn.model_selection import train_test_split
import json
from moexalgo import Market, Ticker
import io
from PIL import Image
import psycopg2

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

pd.options.mode.chained_assignment = None  # default='warn'


# # Импортируем модули
import sys
import argparse

sys.path.insert(0, 'modules')

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
    _ = parser.add_argument('--timeframe')
    _ = parser.add_argument('--start_date')
    _ = parser.add_argument('--end_date')
    _ = parser.add_argument('--count_points')
    _ = parser.add_argument('--extr_bar_count')
    _ = parser.add_argument('--size_df')
    _ = parser.add_argument('--max_unmark')
    _ = parser.add_argument('--data_path')
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
            with open('app/configs/1D/data_gen.json', 'r', encoding='utf_8') as cfg:
                temp_data=cfg.read()

    # parse file
    config = json.loads(temp_data)
    
    task_id = str(config['task_id'])
    interval = config['timeframe']
    start_date = config['start_date'] #Начальная дата датасета
    end_date = config['end_date'] #Конечная дата датасета
    count_points = config['count_points'] #Параметр разметки экстремумов
    #Сколько размечаем баров начиная с точки экстремума
    extr_bar_count = config['extr_bar_count']
    #Ограничения размера файла в Гигабайтах
    size_df = config['size_df']
    #Максимальное количество конечных баров волны в %, которые не размечаем
    max_unmark = config['max_unmark']
    #Путь для сохранения генерируемых данных
    data_path = config['data_path'] #Путь должен быть без чёрточки в конце
    if config['respos_url']:
        respos_url = config['respos_url']
    else:
        respos_url = '127.0.0.1:8080'
    
if load_params_from_command_line:
    task_id = str(args.task_id)
    interval = str(args.timeframe)
    start_date = str(args.start_date)
    end_date = str(args.end_date) 
    count_points = int(args.count_points)
    extr_bar_count = int(args.extr_bar_count) 
    size_df = float(args.size_df) 
    max_unmark = float(args.max_unmark) 
    data_path = str(args.data_path) 
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
#lag_count = 6 #(default)
lag_count = 0

#Дописывать данные (False) или заново записать датасет (True)
new_df = False

#Флаг наличия ограничений генерируемых датасетов по размеру
size_flag = True

#Флаг необходимости удаления не размеченных данных
delete_not_marking_data = True

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
    
    #Разбиваем датасеты
    num_logic_df_train, num_logic_df_test = train_test_split(num_logic_df, test_size=0.1, shuffle=False)
    
    #Записываем датасеты
    print("Записываем датасеты: ", ticker)
    #Проверяем на существование Если не существуют то записываем первый раз с заголовком
    #Если существуют до дописываем без заголовка
    if not os.path.exists(data_path+"/num_logic_1d_1w_train.csv"):
        num_logic_df_train.to_csv(data_path+"/num_logic_1d_1w_train.csv")
    else:
        num_logic_df_train.to_csv(data_path+"/num_logic_1d_1w_train.csv", mode='a', header= False)
    
    if not os.path.exists("app/data/num_logic_1d_1w_test.csv"):
        num_logic_df_test.to_csv(data_path+"/num_logic_1d_1w_test.csv")
    else:
        num_logic_df_test.to_csv(data_path+"/num_logic_1d_1w_test.csv", mode='a', header= False)


# # Проверяем контрольную точку продолжения генерации датасетов

def check_size():
    #Проверяем наличие датасетов
    folder = Path(data_path)
    if os.path.exists(data_path):
        if sum(1 for x in folder.iterdir()) > 0:
            #Проверяем ограничения на размер файла
            if size_flag:
                size_arr = []
                try:
                    size_arr.append(os.path.getsize(data_path+"/num_logic_1d_1w_train.csv")/(1024*1024*1024))
                except:
                    size_arr.append(0)

                max_size_df = max(size_arr)

                if max_size_df > size_df:
                    print ("Достигнут предел по размеру датасетов")
                    return False
                else:
                    return True
                
        else:
            return True
            
    else:
        os.mkdir(data_path)
        return True

#Проверяем наличие датасетов
folder = Path(data_path)
if os.path.exists(data_path):
    if sum(1 for x in folder.iterdir()) > 0:
        #Проверяем ограничения на размер файла
        if size_flag:
            size_arr = []
            try:
                size_arr.append(os.path.getsize(data_path+"/num_logic_1d_1w_train.csv")/(1024*1024*1024))
            except:
                size_arr.append(0)
            
            max_size_df = max(size_arr)
            
            if max_size_df > size_df:
                list_flag = False
                print ("Достигнут предел по размеру датасетов")
        
        #Пытаемся загрузить последний тикер генерации датасета
        try:
            with open('save/last_ticker.pickle', 'rb') as f:
                last_ticker = pickle.load(f)
        except:
            print("Отсутствуют данные сохранения")
else:
    os.mkdir(data_path)


# # Загружаем список для генерации
stocks = Market('stocks')

tickers_list_temp = stocks.tradestats(date='2023-10-10')
tickers_list = pd.DataFrame(tickers_list_temp).rename(
    columns = {
        'secid': 'ticker'
    }
)
tickers_list = tickers_list.groupby('ticker').agg(
    {
        'val': 'sum'
    }
).sort_values(by = ['val'], ascending = False).reset_index()['ticker'].values


# # Генерируем датасеты
if len(tickers_list) > 0:
    for ticker in tickers_list:

        print(ticker)
        if check_size():

            #Генерируем датасет
            print("Начало обработки нового тикера: ", ticker)
            try:
                main(ticker)
            except:
                print("Ошибка генерации датасета: ", ticker)

        else:
            break

else:
    print("Список для обработки пуст")


# # Сохранение результатов
result = {
    'task_id': task_id,
    'status': 'done'
}

#Сохранение результатов в файл
# with open('results/data_gen.json', 'w') as f:
#     json.dump(result, f)

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

