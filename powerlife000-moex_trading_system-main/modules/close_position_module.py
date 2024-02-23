#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def close_position(ticker, mt5, db, config, currency, balance):
    from datetime import datetime
    import math
    
    #Получаем данными по позиции, которую нужно закрыть
    symbol_info=mt5.symbol_info(ticker)
    position=mt5.positions_get(symbol = ticker)
    if (symbol_info!=None) & (position != None):
        symbol_info_dict = mt5.symbol_info(ticker)._asdict()
        #Цена покупки
        ticker_ask = symbol_info_dict['ask']
        
        if ticker_ask == 0.0:
            from moexalgo import Market, Ticker
            import re
            #Пытаемся получить данные с Algopack
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

#             #Пытаемся получить данные с Яху
#             import requests
#             url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+ticker+'?modules=summaryDetail'
#             headers = {
#                 'User-Agent': 'Mozilla/5.0'
#             }
#             response = requests.get(url, headers=headers)

            if response.status_code==200:
                import json
                response_json = json.loads(response.text)
                ticker_bid = response_json['quoteSummary']['result'][0]['summaryDetail']['ask']['raw']
            else:
                print("Error get ticker price: ", ticker)
                #return False
        
        #Проверяем, есть ли открытая задача на открытие позиции с таким же тикерм. если есть, то закрываем задачу
        check_tasks = db.execute("SELECT id FROM robot_tasks WHERE ticker = '"+ticker+"' AND task_type = 'open' AND status = 'in_progress'")
        if (check_tasks != None) & (check_tasks != []):
            for i in range(len(check_tasks)):
                check_tasks = db.execute("UPDATE robot_tasks SET status='closed' WHERE id = '"+check_tasks[i][0]+"'")
                
                #`status`='closed' - задача принудительно закрыта
        
                #Если есть открытая задача, которую нужно удалить, проверяем открытые ордера по задаче и закрываем их
        
        close_num_position = position[0].volume
        task_type = 'close'
        limit_odrer_type = config.order_limit_flag
        status = 'in_progress'
        date_now = datetime.now()  
        max_order_volume = close_num_position

        #Формируем задачу на закрытие позиции
        task = [config.robot_name, task_type, ticker, close_num_position, max_order_volume, limit_odrer_type, config.stop_loss, status, date_now.strftime("%Y-%m-%d %H:%M:%S")]

        #Сохраняем задачу в БД
        sql="INSERT INTO robot_tasks(robot_name, task_type, ticker, volume, max_order_volume, limit_odrer_type, stop_loss, status, date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        add_task = db.execute(sql, task)

        return True 
            
    else:
        return False      

