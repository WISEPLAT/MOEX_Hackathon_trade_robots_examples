#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Config():
    
    def __init__(self):
        
        #Название торгового робота
        self.robot_name = "moex_robot_001"

        #МАРЖИНАЛЬНОЕ ПЛЕЧО: 1 - без маржинального плеча, 1.3 - плечо +30%
        self.leverage = 1

        #Определяем stop-loss (> 7-10%)
        self.stop_loss = 1
        
        #портфель
        self.portfel_reserv = 100 #Резерв портвеля (например под вывод среств)

        #Число лотов
        self.lots_count = 5

        #Параметры телеграм робота и чата
        self.token_tg_bot = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        self.chat_id = '-aaaaaaaaaaaaaaaaaaaaaaaaaa'

        #Ордера выставляются по рынку или лимированно?? False - по рынку; True - лимитирвоанно
        self.order_limit_flag = True
        
        #Раз в сколько секунд обновляется выставленная цена лимитных ордеров??
        self.update_limit_orders_time = 10 #Обновление лимитных ордеров 1 раз в 10 секунд
        
        #Флаг необходимости закрытия позиций в конце дня
        self.close_end_day_flag = False
        #Время в конце дня для закрытия позиций, в секундах
        self.close_end_day_time = 3600
        
        #DB_config
        self.db_host='127.0.0.1'
        self.db_database='aaaaaaaaa'
        self.db_user='aaaaaaaaa'
        self.db_password='aaaaaaaaaa'
        
        #Параметры авторизации в торговом терминале MT5
        self.login = 12345678
        self.password = '12345678'
        self.server = 'Just2Trade-MT5'
        
        #Постфикс тикеров SBER -> SBER.MM
        #self.postfix = '.MM'
        self.postfix = ''
        
        #id задачи по генерации сигналов
        self.signals_task_id = 123
        

