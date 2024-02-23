#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
import math
import ast
import requests
import os
import pickle
from datetime import date
import holidays
import re


# In[2]:


from moexalgo import Market, Ticker
import yfinance as yf


# # Подключаем модули

# In[3]:


import sys, signal
sys.path.insert(0, 'modules')

from DB_module import DB
from Config_module import Config
import Log_module as log_module
from Orders_module import Orders
import close_position_module
import open_position_module
import check_market_module #Функция проверки открытости рынка
import get_usd_rub_module #Функция получения данных валютной пары рубль-доллар
import get_opt_lot_volume_module #Функция определения оптимального объема лота


# In[4]:


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


# In[5]:


def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


# In[6]:


import time


# # НАСТРОЙКИ

# In[7]:


config = Config()


# # Подключение к базе

# In[85]:


db = DB(config)


# # Подключаемся к MetaTrader 5

# In[33]:


if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
    
    if is_notebook() != True:
        print("Ending script")
        #quit()


# # Авторизация в MT5

# In[10]:


authorized = mt5.login(login = config.login, password = config.password, server = config.server)


# In[11]:


#Инициализируем класс выставления ордеров
orders = Orders(mt5)


# # Получаем информацию по валютной паре рубль-доллар

# In[12]:


def get_usd_rub():
    quotes_temp=yf.Ticker('RUB=X')
    quotes=quotes_temp.history(
        interval = "1m",# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        period="1d"
    ) #  1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    quotes.sort_index(ascending=True, inplace = True)
    quotes = quotes[-1:]
    usd_rub = quotes['Close'].values[0]
    
    return usd_rub


# # Закрываем позиции

# In[13]:


def close_all_positions(currency, balance):
    try:
        global db
        if db.connection.closed == 1:
            db = DB(config)
        
        #Получаем данные по открытым позициям
        positions=mt5.positions_get()
        positions_arr = []
        for position in positions:
            positions_arr.append(position.symbol)

        positions_df = pd.DataFrame(
            data = positions_arr,
            columns = ['symbol']
        )
        
        #Получаем данные по текущим заданиям
        close_tasks  = db.execute("SELECT ticker FROM robot_tasks WHERE task_type = 'close' AND status = 'in_progress' AND robot_name = '"+config.robot_name+"'")
        close_tasks_arr = []
        for open_task in close_tasks:
            close_tasks_arr.append(open_task[0])

        #Получаем список, для которого нужно проверить, нужно ли закрывать позиции 
        #Исключаем из списка заданий те,по которым мы уже закрываем позици
        check_positions_to_close = positions_df[~positions_df['symbol'].isin(close_tasks_arr)]

        #Для каждой позиции генерируем задачу на закрытие
        for i, check_position in check_positions_to_close.iterrows():
            print("Пытаемся закрыть позицию: ", check_position['symbol'])
            close_position_module.close_position(check_position['symbol'], mt5, db, config, currency, balance)
    except:
        print("Error to close all positions")


# In[58]:


def close_positions(currency, balance):
    try:
        global db
        if db.connection.closed == 1:
            db = DB(config)
        
        #Получаем данные сигналов
        #Отменяем задание на открытие поизиций (при наличии таковых)
        #Формируем задание на закрытие позиций (уведомляем о формировании задания в телеграм)
        #Рассчитываем объемы лотов закрытия
        #Выставляем лоты закрытия позиций (уведомляем о формировании лота, указываем параметры)

        #Получаем данные по открытым позициям
        positions=mt5.positions_get()
        positions_arr = []
        for position in positions:
            positions_arr.append(position.symbol)

        positions_df = pd.DataFrame(
            data = positions_arr,
            columns = ['symbol']
        )

        #Получаем данные по текущим заданиям
        close_tasks  = db.execute("SELECT ticker FROM robot_tasks WHERE task_type = 'close' AND status = 'in_progress' AND robot_name = '"+config.robot_name+"'")
        close_tasks_arr = []
        for open_task in close_tasks:
            close_tasks_arr.append(open_task[0])

        #Получаем список, для которого нужно проверить, нужно ли закрывать позиции 
        #Исключаем из списка заданий те,по которым мы уже закрываем позици
        check_positions_to_close = positions_df[~positions_df['symbol'].isin(close_tasks_arr)]

        for i, check_position in check_positions_to_close.iterrows():
            print("Check nesessary to close the position: ", check_position['symbol'])
            
            check_symbol = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', check_position['symbol'])[0]
            #Проверяем сигнал, нужно ли закрывать позицию
            check_signal = db.execute("SELECT signal, signal_position FROM cals_signals_results WHERE ticker = '"+check_symbol+"' AND task_id = '"+str(config.signals_task_id)+"'")
            #print(check_signal)
            if (check_signal != None) & (check_signal != []):
                #if int(check_signal[0][0]) == 0:
                if (int(check_signal[0][0]) == 0) & (int(check_signal[0][1]) >= 0):#Если сигнал закрытия в предыдущий день и позже
                    print("Open the task to close the position: ", check_position['symbol'])
                    close_position_module.close_position(check_position['symbol'], mt5, db, config, currency, balance)
    except Exception as e:
        print("Error to close positions: ", e)


# # Открываем новые позиции

# In[15]:


def open_positions(all_positions, balance):
    try:
        global db
        if db.connection.closed == 1:
            db = DB(config)
        
        
            #Рассчитываем число свободных лотов, Определяем объем лота

        lots_count = config.lots_count

        #Определяем текущее количество занятых слотов
        #Получаем данные по открытым позициям
        positions=mt5.positions_get()
        positions_arr = []
        for position in positions:
            positions_arr.append([position.symbol, position.price_open, position.volume])

        positions_df = pd.DataFrame(
            data = positions_arr,
            columns = ['symbol', 'price_open', 'volume']
        )

        positions_df['total'] = positions_df['price_open'] * positions_df['volume']

        free_USD = balance - positions_df['total'].sum()
        
        max_lot_curr_volume = (balance - config.portfel_reserv) / lots_count

        #Получаем данные по текущим заданиям
        open_tasks =db.execute("SELECT ticker FROM robot_tasks WHERE task_type = 'open' AND status = 'in_progress' AND robot_name = '"+config.robot_name+"'")
        open_tasks_arr = []
        for open_task in open_tasks:
            open_tasks_arr.append(open_task[0])

        #Объединяем данные по открым позициям и заданиям, получаем итоговое количество занятых слотов
        all_positions = list(set(list(positions_df['symbol'].array)+open_tasks_arr))
        
        #Проверяем достаточность средств для открытия позиции!!!
        check_free_USD = free_USD > 0.8*max_lot_curr_volume

        #Получаем количество свободных слотов
        free_slots_count = lots_count - len(all_positions)
        
        if (free_slots_count > 0) & (check_free_USD):
            print('Число свободных лотов: ', free_slots_count)
            #Получаем данные сигналов, берем лучший
            #Берем сигналы день предыдущий день
            best_open_signals = db.execute("SELECT ticker, signal, signal_position FROM cals_signals_results WHERE signal = '2' AND signal_position = '0' AND task_id = '"+str(config.signals_task_id)+"' LIMIT 20")
            best_open_signals_df = pd.DataFrame(
                data = best_open_signals,
                columns = ['ticker', 'signal', 'signal_position']
            )
            best_open_signals_df['ticker'] = best_open_signals_df['ticker']+config.postfix

            #Исключаем тикеры сигналов открытых позиций
            best_open_signals_df = best_open_signals_df[~best_open_signals_df['ticker'].isin(all_positions)]

            #Перебираем сигналы начиная с первого и пытаемся сформировать задачу на открытие позиции
            for i, signal in best_open_signals_df.iterrows():
                print("Trying to open task", signal['ticker'])
                result = open_position_module.open_position(signal['ticker'], mt5, db, config, balance, lots_count)

                #Если задача поставлена успешно, то заканчиваем работу
                if result == True:
                    break
    except Exception as e:
        print("Error to open positions: ", e)


# # Выполнение задач, работа с ордерами

# # Контролируем задания по закрытию позиций

# In[82]:


def control_close_tasks():
    try:
        global db
        if db.connection.closed == 1:
            db = DB(config)
        
        #Получаем данные по задачам на закрытие позиций
        sql = "SELECT id,robot_name,task_type,ticker,volume,max_order_volume,limit_odrer_type,stop_loss,status,date FROM robot_tasks WHERE task_type = 'close' AND status = 'in_progress' AND robot_name = '"+config.robot_name+"'"
        close_tasks =db.execute(sql)
        close_tasks_df = pd.DataFrame(
            data = close_tasks,
            columns = [
                'id',
                'robot_name',
                'task_type',
                'ticker',
                'volume',
                'max_order_volume',
                'limit_odrer_type',
                'stop_loss',
                'status',
                'date'
            ]
        ) 

        for i, close_task in close_tasks_df.iterrows():
            #Проверяем, выполнена ли текущая задача
            #Проверяем, сколько продано на текущий момент
            current_volume = 0
            current_position = mt5.positions_get(symbol=close_task['ticker'])
            print("Control close task: ", current_position)
            if (current_position == None) | (len(current_position) == 0):
                sql = "UPDATE robot_tasks SET status='done' WHERE id = '"+str(close_task['id'])+"'"
                result = db.execute(sql)
                continue

            #ЗАДАЧА НЕ ВЫПОЛНЕНА

            #Проверяем наличие выставленных ордеров для задачи, если они отсутствуют, то выставляем ордера на закрытие
            current_orders = mt5.orders_get(symbol = close_task['ticker'])
            if (current_orders == None) | (len(current_orders) == 0):
                #Ордеров нет, выставляем ордер
                print("Open new order for close position")

                #Определяем объем ордера
                #Некоторые ордера могут быть ранее выполнены не полностью, поэтому определяем максимальный объем ордера может быть избыточным
                #Необходимо скорректировать объем лота

                #Определяем объем для закрытия позиции
                order_volume = 0

                if ((close_task['volume']-current_volume)/close_task['max_order_volume']) >= 1:
                    order_volume = close_task['max_order_volume']
                else:
                    order_volume = close_task['volume'] - current_volume

                #Записываем задачу по ордеру в базу
                date_now = datetime.now()
                result = db.execute("SELECT MAX(id) FROM robot_orders_tasks;")
                if result[0][0] is None:
                    id = 0
                else:
                    id = result[0][0]+1

                if config.order_limit_flag:
                    print("Open limit order in market to close position: ", close_task['ticker'])
                    result = orders.send_order_limit(id, close_task['ticker'], order_volume, 'sell', close_task['stop_loss'])
                else:
                    print("Open order in market to close position: ", close_task['ticker'])
                    print(close_task['ticker'])
                    result = orders.send_order(id, close_task['ticker'], order_volume, 'sell', close_task['stop_loss'])
                
                try:
                    if result.comment == 'Request executed':
                        #Записываем задачу по ордеру в базу
                        date_now = datetime.now()
                        sql = "INSERT INTO robot_orders_tasks (ticker, type, limit_order, stop_loss, time, status) VALUES (%s,%s,%s,%s,%s,%s);"    
                        order_task = [close_task['ticker'],'sell',config.order_limit_flag,config.stop_loss,date_now.strftime("%m/%d/%Y, %H:%M:%S"),'open']
                        result = db.execute(sql,order_task)
                except:
                    print('Ошибка создания ордера на закрытие позиции: ', close_task['ticker'])

    except Exception as e:
        print("Error to control close positions: ", e)


# # Контролируем задания по открытию позиций

# In[17]:


def control_open_tasks():
    try:
        global db
        if db.connection.closed == 1:
            db = DB(config)
        
        #Получаем данные по задачам на открытие позиций
        open_tasks = db.execute("SELECT id,robot_name,task_type,ticker,volume,max_order_volume,limit_odrer_type,stop_loss,status,date FROM robot_tasks WHERE task_type = 'open' AND status = 'in_progress' AND robot_name = '"+config.robot_name+"'")
        open_tasks_df = pd.DataFrame(
            data = open_tasks,
            columns = [
                'id',
                'robot_name',
                'task_type',
                'ticker',
                'volume',
                'max_order_volume',
                'limit_odrer_type',
                'stop_loss',
                'status',
                'date'
            ]
        )

        for i, open_task in open_tasks_df.iterrows():
            #Проверяем, выполнена ли текущая задача
            #Проверяем, сколько куплено на текущий момент
            current_volume = 0
            current_position = mt5.positions_get(symbol=open_task['ticker'])
            if (current_position != None) & (len(current_position) != 0):
                #Обходим позиции
                current_position_df=pd.DataFrame(list(current_position),columns=current_position[0]._asdict().keys())
                for position in current_position:
                    current_volume = current_volume + position.volume

                #Если требуемый объем достигнут, закрываем задачу
                if (open_task['volume'] <= current_volume) & (current_volume != 0):
                    sql = "UPDATE robot_tasks SET status='done' WHERE id = '"+str(open_task['id'])+"'"
                    result = db.execute(sql)
                    continue

            #ЗАДАЧА НЕ ВЫПОЛНЕНА
            #Проверяем наличие выставленных ордеров для задачи, если они отсутствуют, то выставляем ордера на открытие
            current_orders = mt5.orders_get(symbol = open_task['ticker'])
            if (current_orders == None) | (len(current_orders) == 0):
                #Ордеров нет, выставляем ордер
                print("Open new order for open position")

                #Определяем объем ордера
                #Некоторые ордера могут быть ранее выполнены не полностью, поэтому определяем максимальный объем ордера может быть избыточным
                #Необходимо скорректировать объем лота

                #Определяем объем для открытия позиции
                order_volume = 0

                if ((open_task['volume']-current_volume)/open_task['max_order_volume']) >= 1:
                    order_volume = open_task['max_order_volume']
                else:
                    order_volume = open_task['volume'] - current_volume

                result = db.execute('SELECT MAX(id) FROM robot_orders_tasks;')        
                if result[0][0] == None:
                    id = 0
                else:
                    id = result[0][0]+1

                if config.order_limit_flag:
                    print("Open limit order in market for open: ", open_task['ticker'])
                    result = orders.send_order_limit(id, open_task['ticker'], order_volume, 'buy', open_task['stop_loss'])
                    print(result)
                    
                else:
                    print("Open order in market for open: ", open_task['ticker'])
                    result = orders.send_order(id, open_task['ticker'], order_volume, 'buy', open_task['stop_loss'])
                    print(result)

                try:
                    if result.comment == 'Request executed':
                        #Ордер выставлен
                        #Записываем задачу по ордеру в базу
                        date_now = datetime.now()
                        sql = "INSERT INTO robot_orders_tasks (ticker, type, limit_order, stop_loss, time, status) VALUES (%s,%s,%s,%s,%s,%s);"
                        order_task = [open_task['ticker'],'buy',config.order_limit_flag,config.stop_loss,date_now.strftime("%m/%d/%Y, %H:%M:%S"),'open']
                        result = db.execute(sql,order_task)
                except:
                    print('Ошибка создания ордера на открытие позиции: ', open_task['ticker'])

    except Exception as e:
        print("Error to control open positions: ", e)


# In[36]:


def control_limit_orders():
    #Обход ордеров и обновление цены каждые 30 секунд
    current_orders = mt5.orders_get()

    for order in current_orders:

        #Получаем дату выставления ордера
        order_date = datetime.fromtimestamp(order.time_setup)
        #Получаем текущую дату
        now = datetime.now()

        delta = (now-order_date).seconds

        #Если прошло более 10 секунд с момента установки ордера, обновляем цену

        if delta > config.update_limit_orders_time:
            orders.change_price_order_limit(order.ticket, order.symbol)


# In[19]:


def close_all_open_tasks():
    global db
    if db.connection.closed == 1:
        db = DB(config)
    
    close_tasks =db.execute("UPDATE robot_tasks SET status='canceled' WHERE task_type = 'open' AND status = 'in_progress'")
    
    return close_tasks


# In[20]:


def close_all_open_orders():
    current_orders = mt5.orders_get()
    
    for order in current_orders:
        #Если лимитированный ордер на покупку, то удаляем его
        if order.type == 2:
            orders.delete_order(td, order.ticket)
    
    return


# # Обработка сигналов

# In[ ]:


while True:
    try:
        #Проверяем состояние рынка
        market_status_temp = check_market_module.check_market(config, is_notebook)
        market_status = market_status_temp[0]
        time_to_close = market_status_temp[1]
        if market_status == 'closed':
            print("Market is closed.", datetime.now())
            time.sleep(3)
            continue
            
        #Получаем данные о счёте
        if authorized:
            account_info = mt5.account_info()

            balance = account_info.balance
            print('balance: ', balance) 
            equity = account_info.equity
            print('equity: ', equity)
            currency = account_info.currency
            print('currency: ', currency)
        else:
            print("Error get account balance", datetime.now())
            continue
            
        #Получаем данные по валютной паре рубль доллар
        try:
            usd_rub = get_usd_rub()
        except Exception as e:
            print("Ошибка получения валютной пары рубль-доллар:", e)
            if currency == 'USD':
                continue
                
        config.balance = balance
        config.equity = equity
        config.currency = currency
        config.usd_rub = usd_rub
            
        #Получаем данные по откытым позициям
        all_positions=mt5.positions_get()
        if all_positions:
            print("Total positions=",all_positions, ' ', datetime.now())
        else:
            print("Positions not found", datetime.now())
            
            
        #Пытаемся закрыть позиции
        try:
            close_positions(currency, balance)
        except KeyboardInterrupt:
            print("Keyboard interrupt exception caught")
            break
        except Exception as e:
            print("Ошибка закрытия позиций: ", datetime.now())
            
        if (config.close_end_day_flag == False) | ((config.close_end_day_flag == True) & (time_to_close > 3600)):
            #Пытаемся открыть позиции
            try:
                open_positions(all_positions, balance)
            except KeyboardInterrupt:
                print("Keyboard interrupt exception caught")
                break
            except Exception as e:
                print("Ошибка открытия позиций: ", datetime.now(), ' : ', e)
            
            
        #Контролируем выполнение лимитных ордеров
        try:
            control_limit_orders()
        except KeyboardInterrupt:
            print("Keyboard interrupt exception caught")
            break
        except Exception as e:
            print("Ошибка контроля выполнения лимитных ордеров: ", datetime.now(), ' : ', e)
            
        #Контролируем задания по закрытию позиций       
        try:
            control_close_tasks()
        except KeyboardInterrupt:
            print("Keyboard interrupt exception caught")
            break
        except Exception as e:
            print("Ошибка контроля заданий по закрытию позиций: ", datetime.now(), ' : ', e)
        
        if (config.close_end_day_flag == False) | ((config.close_end_day_flag == True) & (time_to_close > config.close_end_day_time)):
            #Контролируем задания по открытию позиций
            try:
                control_open_tasks()
            except KeyboardInterrupt:
                print("Keyboard interrupt exception caught")
                break
            except Exception as e:
                print("Ошибка контроля заданий по открытию позиций: ", datetime.now(), ' : ', e)
            
        #Логируем изменения
#         try:
#             log_module.new_logs(config, db, mt5)
#         except Exception as e:
#             print("Error update logs", ' : ', e)
            
            
        #Отменяем все задачи на открытые позиции в последний час торгов
        if ((config.close_end_day_flag == True) & (time_to_close <= config.close_end_day_time)):
            close_all_open_tasks()

        #Закрываем все открытые позиции в последний час торгов
        if ((config.close_end_day_flag == True) & (time_to_close <= config.close_end_day_time)):    
            close_all_positions(currency, balance)
        
        #Удаялем все ордера на открытие
        if ((config.close_end_day_flag == True) & (time_to_close <= config.close_end_day_time)):
            close_all_open_orders()
        
    except KeyboardInterrupt:
        print("Keyboard interrupt exception caught")
        break


# In[ ]:




