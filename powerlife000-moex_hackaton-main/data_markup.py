#!/usr/bin/env python
# coding: utf-8
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import numpy as np
import requests
import datetime
import pytz
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from mpl_finance import candlestick_ohlc  #  pip install mpl-finance
import mplfinance as mpf
import yfinance as yf
from moexalgo import Market, Ticker
import plotly.graph_objects as go
import warnings
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
import sys
import json
import argparse
import io
from PIL import Image
import psycopg2
import base64

sys.path.insert(0, 'modules')


# # Загрузка параметров
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
    _ = parser.add_argument('--timeframe')
    _ = parser.add_argument('--start_date')
    _ = parser.add_argument('--end_date')
    _ = parser.add_argument('--count_points')
    _ = parser.add_argument('--extr_bar_count')
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
            with open('app/configs/10m/data_markup.json', 'r', encoding='utf_8') as cfg:
                temp_data=cfg.read()

    # parse file
    config = json.loads(temp_data)
    
    task_id = str(config['task_id'])
    ticker = str(config['ticker'])
    interval = str(config['timeframe'])
    start_date = str(config['start_date']) #Начальная дата датасета
    end_date = str(config['end_date']) #Конечная дата датасета
    count_points = int(config['count_points']) #Параметр разметки экстремумов
    extr_bar_count = int(config['extr_bar_count']) #Сколько баров размечаем для генерации сигналов
    if config['respos_url']:
        respos_url = config['respos_url']
    else:
        respos_url = '127.0.0.1:8080'
    
if load_params_from_command_line:
    task_id = str(args.task_id)
    ticker = str(args.ticker)
    interval = str(args.timeframe)
    start_date = str(args.start_date) #Начальная дата датасета
    end_date = str(args.end_date) #Конечная дата датасета
    count_points = int(args.count_points) #Параметр разметки экстремумов
    extr_bar_count = int(args.extr_bar_count) #Сколько баров размечаем для генерации сигналов
    if args.respos_url:
        respos_url = str(args.respos_url).replace(']',"").replace('[',"").replace('"',"").replace("'","")
    else:
        respos_url = '127.0.0.1:8080'

Y_shift = 0

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


# # Читаем и выбираем данные
# Акции
quotes_temp = Ticker(ticker)
# Свечи по акциям за период
quotes = quotes_temp.candles(date = start_date, till_date = end_date, period=interval)
quotes = pd.DataFrame(quotes)

quotes.rename(
    columns = {
        'begin' : 'Datetime',
        'open' : 'Open',
        'close' : 'Close',
        'high' : 'High',
        'low' : 'Low',
        'volume' : 'Volume'
    }, inplace = True
)
quotes.index = quotes['Datetime']
quotes.sort_index(ascending=True, inplace = True)


# # Смотрим исходные данные
try:
    if is_notebook():
        fig = go.Figure(data=[go.Candlestick(
                        #x=quotes.index,
                        open=quotes['Open'],
                        high=quotes['High'],
                        low=quotes['Low'],
                        close=quotes['Close'])])
        #fig.update_layout(xaxis_rangeslider_visible=False)
        fig.show()
except:
    pass


# # Ищем экстремумы
def get_extrems(dataset, count_points):
    
    dataset['extr'] = None
    
    #Инициализируем переменные
    new_min = 10000000;
    new_max = 0;

    find_first = False;

    count_extr = 0;
    current_top_number = 0;
    current_bot_number = 0;

    extrems = []
    last_extr = None;
    last_extr_i = 0;
    
    #Число точек, относительно по которым ищутся экстремумы
    #count_points = 10
    
    min = []
    max = []
    
    for i in range(count_points+1):
        min.append(0)
        max.append(0)   

    
    i_filter = 1; #Фильтр близости предыдущего экстремума. Он должен быть дальше чем 1 день
    
    print("Общее число данных графика для обработки: ", dataset.shape[0])
    
    quote_count = 0;
    
    for i, quote in dataset.iterrows():
        
        if quote_count+count_points >= dataset.shape[0]:
            break
            
        for j in range(count_points+1):
            
#             max[j] = quotes.iloc[quote_count+j].High;
#             min[j] = quotes.iloc[quote_count+j].Low;

            max[j] = quotes.iloc[quote_count+j].Close;
            min[j] = quotes.iloc[quote_count+j].Close;
            
        if find_first == False: #Ищем первую точку
            
            logic_max = True
            for j in range(1, count_points+1):
                logic_max = logic_max & (max[0] > max[j])
            
            if logic_max:
                find_first = True;#Первый максимум найден

                new_min = max[0];
                dataset.at[i, 'extr'] = 'max'
                extrems.append([quote,quote_count,'max'])
                last_extr = 'max'

            
            logic_min = True
            for j in range(1, count_points+1):
                logic_min = logic_min & (min[0] < min[j])
                
            if logic_min:
                find_first = True;#Первый минимум найден

                new_max = min[0];
                dataset.at[i, 'extr'] = 'min'
                extrems.append([quote,quote_count,'min'])
                last_extr = 'min'
        
        else: #Ищем остальные точки
            
            if last_extr == 'min':
                
                if quotes.iloc[quote_count].High > new_max:
                    new_max = max[0];
                    
                    logic_max = True
                    for j in range(1, count_points+1):
                        logic_max = logic_max & (max[0] > max[j])
                    
                    if logic_max:
                        find_first = True;#Максимум найден
                        
                        new_min = max[0]
                        dataset.at[i, 'extr'] = 'max'
                        extrems.append([quote,'max'])
                        last_extr = 'max'                        
            
            elif last_extr == 'max':
                
                if quotes.iloc[quote_count].Low < new_min:
                    new_min = min[0]
                    
                    logic_min = True
                    for j in range(1, count_points+1):
                        logic_min = logic_min & (min[0] < min[j])

                    if logic_min:
                        find_first = True;#Минимум найден

                        new_max = min[0];
                        dataset.at[i, 'extr'] = 'min'
                        extrems.append([quote,'min'])
                        last_extr = 'min'
        
        quote_count = quote_count+1

    return dataset

quotes_with_extrems = get_extrems(quotes, count_points)
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
    

# # Смотрим результаты разметки
quotes_with_extrems['x'] = quotes_with_extrems.index

y_max = quotes_with_extrems['High'].max()*1.05
y_min = quotes_with_extrems['Low'].min()*0.95

#%matplotlib qt

try:
    if is_notebook():

        feel_df = quotes_with_extrems

        try:
            feel_df.drop(columns = ['Datetime'], inplace = True)
        except:
            pass

        feel_df.reset_index(inplace = True)
        fig = go.Figure(data=[go.Candlestick(
                        x=feel_df.index,
                        open=feel_df['Open'],
                        high=feel_df['High'],
                        low=feel_df['Low'],
                        close=feel_df['Close'])])

        feel_df = quotes_with_extrems[quotes_with_extrems['extr'].notna()]

        feel_df['x'] = feel_df.index
        feel_df['x1'] = feel_df['x'].shift(-1)
        feel_df.dropna(subset = ['x1'], inplace = True)

        for i, row in feel_df.iterrows():    

            fig.add_shape(type="rect",
                                xref="x",
                                yref="paper",
                                x0=row['x'],
                                y0=0,
                                x1=row['x1'],
                                y1=row['High']*10,
                                line=dict(color="rgba(0,0,0,0)",width=3,),
                                fillcolor=row['Color'],
                                layer='below')

            #quote_count = quote_count + 1



        fig.show()
except:
    pass


# # Разметка сигналов
#Разметка Y
def quotes_with_Y(quotes_with_extrems, extr_bar_count, Y_shift, max_unmark = 0.3):
    quotes_with_extrems['Y'] = None
    
    last_extr = quotes_with_extrems.iloc[0]['extr']
    bar_count = 0
    
    max_bar_count = 0
    
    for i, quote in quotes_with_extrems.iterrows():
        if (quote['extr'] != last_extr) & ((quote['extr'] == 'min') | (quote['extr'] == 'max')):
            last_extr = quote['extr']
            bar_count = 0
            
            #Считаем сколько баров до следующей точки экстремума
            max_bar_count = 0
            if quotes_with_extrems[quotes_with_extrems.index > i]['extr'].isin(['min', 'max']).any():
                for j, row in quotes_with_extrems[quotes_with_extrems.index > i].iterrows():
                    if (row['extr'] == 'min') | (row['extr'] == 'max'):
                        break
                    else:
                        max_bar_count += 1
            else:
                max_bar_count = quotes_with_extrems[quotes_with_extrems.index > i].shape[0]

        if (bar_count < extr_bar_count) & (bar_count < max_bar_count*(1-max_unmark)):
            if last_extr == 'min':
                quotes_with_extrems.at[i, 'Y'] = 1 + Y_shift
                bar_count = bar_count + 1
            elif last_extr == 'max':
                quotes_with_extrems.at[i, 'Y'] = -1 + Y_shift
                bar_count = bar_count + 1
        else:
            quotes_with_extrems.at[i, 'Y'] = 0 + Y_shift

    return quotes_with_extrems

#Размечаем Y по дневному графику
quotes_1d_with_Y = quotes_with_Y(quotes_with_extrems, extr_bar_count, Y_shift, max_unmark = 0.2)    

try:
    if is_notebook():
        fig, ax = plt.subplots()
        ax.set_title('Сигналы')

        try:
            show = quotes_1d_with_Y.drop(columns = ['Datetime']).reset_index()#Делаем ресет индекса, чтобы не показывались даты
        except:
            try:
                show = quotes_1d_with_Y.reset_index()
            except:
                show = quotes_1d_with_Y

        plt.plot(show['Y'], label='Размеченые данные')
        plt.legend(loc="lower right")
        plt.show()
except:
    pass

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


# # Расчёт трейдов при торговле в лонг
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
        if (quote['Trend'] == 'sell') | (iter_count+1 == quotes_with_extrems.shape[0]):
            current_position = 'close'
            
            profit = quote['Close']/current_open_price
            
            trades_without_shift.append([current_open_price, quote['Close'], profit])
    
    iter_count = iter_count + 1

#Доходность без смещения

profit_without_shift = 1

for row in trades_without_shift:
    profit_without_shift = profit_without_shift * row[2]
    
print("Доходность без смещения: ", profit_without_shift)

#Трейды со смещением

trades_with_shift = []

current_position = 'close'
current_open_price = 0

iter_count = 0
for i, quote in quotes_with_extrems.iterrows():
    
    if current_position == 'close':
        if quote['Trend'] == 'buy':
            current_position = 'open'
            try:
                current_open_price = quotes_with_extrems.iloc[iter_count+1]['Close']
            except:
                current_open_price = quotes_with_extrems.iloc[iter_count]['Close']
            
    if current_position == 'open':
        if (quote['Trend'] == 'sell') | (iter_count+1 == quotes_with_extrems.shape[0]):
            current_position = 'close'
            
            try:
                profit = quotes_with_extrems.iloc[iter_count+1]['Close']/current_open_price 
                trades_with_shift.append([current_open_price, quotes_with_extrems.iloc[iter_count+1]['Close'], profit])
            except:
                profit = quotes_with_extrems.iloc[iter_count]['Close']/current_open_price 
                trades_with_shift.append([current_open_price, quotes_with_extrems.iloc[iter_count]['Close'], profit])
    
    iter_count = iter_count + 1

#Доходность со смещением

profit_with_shift = 1

for row in trades_with_shift:
    profit_with_shift = profit_with_shift * row[2]
    
print("Доходность со смещением: ", profit_with_shift)

# # Сохранение результатов
result_df = quotes_with_extrems.copy(deep = True)
result_df.drop(columns = ['value', 'end', 'Color', 'x'], inplace = True)

result_df.rename(columns = {
    'Y':'Singals',
    'extr': 'Extrems'
}, inplace = True)

result_df['Trend'] = np.where(result_df['Trend'] == 'sell', 0, result_df['Trend'])
result_df['Trend'] = np.where(result_df['Trend'] == 'buy', 1, result_df['Trend'])

result = {
    'task_id': task_id,
    'markup': {
       'description': '',
        'values': {
            'Datetime': result_df['Datetime'].values.tolist(),
            'Open': result_df['Open'].values.tolist(),
            'Close': result_df['Close'].values.tolist(),
            'High': result_df['High'].values.tolist(),
            'Low': result_df['Low'].values.tolist(),
            'Volume': result_df['Volume'].values.tolist(),
            'Extrems': result_df['Extrems'].values.tolist(),
            'Trend': result_df['Trend'].values.tolist(),
            'Singals': result_df['Singals'].values.tolist(),
        }
    },
    'profit_without_shift': {
        'description': 'Теоретическая доходность',
        'value': profit_without_shift
    },
    'profit_with_shift': {
        'description': 'Доходность при смещении точек покупки и продажи на 1 бар',
        'value': profit_with_shift
    }
}

#result_json = json.dumps(result)
# #
# with open('results/murkup_data.json', 'w') as f:
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

