#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Формируем задание на открытие позиций (уведомляем о формировании задания в телеграм)
def open_position(ticker, mt5, db, config, balance, lots_count):
    from datetime import datetime
    import time
    import math
    
    #Проверяем возможность покупки по тикеру, получаем данные по цене покупки
    if mt5.market_book_add(ticker):
        # сделаем паузу в 3 секунды для добавления тикера в терминал
        time.sleep(5)
        symbol_info=mt5.symbol_info(ticker)
        if symbol_info!=None:
            symbol_info_dict = mt5.symbol_info(ticker)._asdict()
            #Цена покупки
            ticker_bid = symbol_info_dict['bid']
            
            if ticker_bid == 0.0:
                from moexalgo import Market, Ticker
                import re

                quotes_temp = Ticker(re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', ticker))
                # Свечи по акциям за период
                quotes = quotes_temp.candles(
                    date = (datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d"), 
                    till_date = datetime.now().strftime("%Y-%m-%d"), 
                    period='1m')
                #quotes_1d.head()
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
                #quotes = quotes[-1:]
                price = quotes['Close'].values[0]

                ticker_bid = price
                
#                 #Пытаемся получить данные с Яху
#                 import requests
#                 url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+ticker+'?modules=summaryDetail'
#                 headers = {
#                     'User-Agent': 'Mozilla/5.0'
#                 }
#                 response = requests.get(url, headers=headers)

#                 if response.status_code==200:
#                     import json
#                     response_json = json.loads(response.text)
#                     ticker_bid = response_json['quoteSummary']['result'][0]['summaryDetail']['ask']['raw']
#                 else:
#                     print("Error get ticker price: ", ticker)
#                     #return False

            #Определяем максимальный объем лота
            #!!! УЧЕСТЬ НЕОБХОДИМОСТЬ РЕЗЕРВИРОВАНИЯ СРЕДСТВ ПОД ВЫВОД И УЧЕСТЬ КОМИССИЮ 
            # (то есть, баланс всегда должен быть всегда положительным)
            #Учесть то, что деньги просто могут быть выведены со счёта и будет дисбаланс объема лотов
            #Нужно проверить объем текущий свободных денежных средств. Их должно быть больше чем на 1 лот.
            #Если их меньше, то максимальный объем должен быть меньше текущего объема с учётом резерва и комиссии
            if config.currency == 'USD':
                max_lot_curr_volume = config.usd_rub * (balance - config.portfel_reserv) / lots_count
            else:
                max_lot_curr_volume = (balance - config.portfel_reserv) / lots_count
                
#             max_lot_curr_volume = (balance - config.portfel_reserv) / lots_count

            #Определяем число акций для покупки
            try:
                print(ticker_bid)
                open_num_position = math.floor(max_lot_curr_volume/ticker_bid)
            except:
                print("Error calc number of shares for open position: ", ticker)
                return False

            #!!!
            #Сравниваем с максимально допустимым числом покупаемых акций в слоте, в зависимости от часового объема??
            #Среднего часового объема??
            #!!!

            #Проверяем, есть ли открытая задача на открытие позиции с таким же тикерм. если есть, то закрываем задачу
            
            check_tasks = db.execute("SELECT id FROM robot_tasks WHERE ticker = '"+str(ticker)+"' AND task_type = 'close' AND status = 'in_progress'")
            if (check_tasks != None) & (check_tasks != []):
                for i in range(len(check_tasks)):
                    check_tasks = db.execute("UPDATE robot_tasks SET status='closed' WHERE id = '"+str(check_tasks[i][0])+"'")

                    #`status`='closed' - задача принудительно закрыта

                    #Если есть открытая задача, которую нужно удалить, проверяем открытые ордера по задаче и закрываем их

            if balance == 0:
                print("Balance = 0, or error getting balance for open position")
                return False
                    
            task_type = 'open'
            limit_odrer_type = config.order_limit_flag
            status = 'in_progress'
            date_now = datetime.now()
            max_order_volume = open_num_position
            
            if open_num_position == 0:
                print("Error count volume for open position: ", ticker)
                return False

            #Формируем задачу на открытие позиции
            task = [config.robot_name, task_type, ticker, open_num_position, max_order_volume, limit_odrer_type, config.stop_loss, status, date_now.strftime("%Y-%m-%d %H:%M:%S")]
            
            sql="INSERT INTO robot_tasks(robot_name, task_type, ticker, volume, max_order_volume, limit_odrer_type, stop_loss, status, date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            add_task = db.execute(sql, task)
            
            mt5.market_book_release(ticker)
            return True
        else:
            mt5.market_book_release(ticker)
            return False
    else:
        mt5.market_book_release(ticker)
        return False

