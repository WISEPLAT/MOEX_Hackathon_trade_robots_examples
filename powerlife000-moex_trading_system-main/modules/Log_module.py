#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def new_logs(config, db, mt5):
    import pandas as pd
    import requests
    from datetime import datetime
    
    #Получаем данные о последних записях лога из БД
    last_logs_data = db.execute("SELECT * FROM robot_logs WHERE robot_name='"+config.robot_name+"' ORDER BY time DESC LIMIT 5")
    if last_logs_data is not None:
        last_logs = last_logs_data

    #Получаем последнюю дату
    #...

    #Получаем логи ВКЛЮЧАЯ ПОСЛЕДНЮЮ ДАТУ
    from_date=datetime(2020,1,1)
    to_date=datetime.now()
    deals=mt5.history_deals_get(from_date, to_date)

    #Преобразовываем логи
    deals_df = pd.DataFrame(
        data = deals,
        columns = [
            'ticket',
            'order',
            'time',
            'time_msc',
            'type',
            'entry',
            'magic',
            'position_id',
            'reason',
            'volume',
            'price',
            'commission',
            'swap',
            'profit',
            'fee',
            'symbol',
            'comment',
            'external_id'        
        ]
    )
    deals_df['robot_name'] = config.robot_name
    
    #Исключаем те, которые мы уже записывали
    if (last_logs_data is not None) & (last_logs_data != []):
        if (last_logs[0][3] != None):
            new_deals_df = deals_df[deals_df['time'] > last_logs[0][3]]
        else:
            new_deals_df = pd.DataFrame([])
    else:
        new_deals_df = pd.DataFrame([])

    #Записываем логи в БД
    new_deals_np = new_deals_df.to_numpy()
    new_deals_list = new_deals_np.tolist()

    sql = "INSERT INTO robot_logs (`ticket`, `order_id`, `time`, `time_msc`, `type`, `entry`, `magic`, `position_id`, `reason`, `volume`, `price`, `commission`, `swap`, `profit`, `fee`, `symbol`, `comment`, `external_id`, `robot_name`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        #for insert_data in new_deals_list:
        #    insert_new_logs = db.execute(sql,insert_data)
        if len(new_deals_list) != 0:
            insert_new_logs = db.executemany(sql,new_deals_list)
    except Exception as e:
        print("Error with DB: ", e)

    #Выводим данные о новых логах в телеграм
    for i,new_deal in new_deals_df.iterrows():
        
        message = ''
        if new_deal['comment'] == 'buy':
            message = message + "Покупаем по рынку инструмент: "
        elif new_deal['comment'] == 'sell':
            message = message + "Продаём по рынку инструмент: "
        elif new_deal['comment'] == 'buy_limit':
            message = message + "Покупаем лимитированно инструмент: "
        elif new_deal['comment'] == 'sell_limit':
            message = message + "Покупаем лимитированно инструмент: "
            
        message = message + new_deal['symbol'] + ". "
        message = message + "Цена сделки: "+str(new_deal['price'])+". "
        message = message + "Объем лота: "+str(new_deal['volume'])+". "
        message = message + "Комиссия: "+str(new_deal['commission'])+". "
        
        if new_deal['profit'] != 0.0:
            message = message + "Прибыль: "+str(new_deal['profit'])+". "
    
        res = requests.get('https://api.telegram.org/bot'+config.token_tg_bot+'/sendMessage?chat_id='+config.chat_id+'&text='+message)
        #print(res.status_code)
        #print(res.text)
    
    return True

