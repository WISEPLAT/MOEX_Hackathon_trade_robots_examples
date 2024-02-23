#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Orders():
    
    def __init__(self,mt5):
        import time
        from moexalgo import Market, Ticker
        from datetime import datetime, timedelta
        import pandas as pd
        self.pd = pd
        self.time = time
        self.mt5 = mt5
        self.Ticker = Ticker
        
    def send_order(self, id, symbol, lot, type_, stop_loss):
        #Подписываемся на получение данных по тикеру
        if self.mt5.market_book_add(symbol):
            # сделаем паузу в 3 секунды для добавления тикера в терминал
            self.time.sleep(5)
        
            lot = float(lot)

            try:
                if type_ == 'buy':
                    ORDER_TYPE = self.mt5.ORDER_TYPE_BUY
                    price = self.mt5.symbol_info_tick(symbol).ask
                    sl = price*(1 - stop_loss/100)

                    deviation = 20
                    request = {
                        "action": self.mt5.TRADE_ACTION_DEAL,
                        "symbol": symbol,
                        "volume": lot,
                        "type": ORDER_TYPE,
                        "price": price,
                        "sl": sl,
                        #"deviation": deviation,
                        "magic": id,
                        "comment": "buy",
                        "type_time": self.mt5.ORDER_TIME_GTC,
                        "type_filling": self.mt5.ORDER_FILLING_FOK,
                    }
                elif type_ == 'sell':
                    ORDER_TYPE = self.mt5.ORDER_TYPE_SELL
                    price = self.mt5.symbol_info_tick(symbol).bid
                    deviation = 20
                    request = {
                        "action": self.mt5.TRADE_ACTION_DEAL,
                        "symbol": symbol,
                        "volume": lot,
                        "type": ORDER_TYPE,
                        "price": price,
                        #"deviation": deviation,
                        "magic": id,
                        "comment": "sell",
                        "type_time": self.mt5.ORDER_TIME_GTC,
                        "type_filling": self.mt5.ORDER_FILLING_FOK,
                    }

                # send a trading request
                result = self.mt5.order_send(request)
                self.mt5.market_book_release(symbol)
                return result
            except Exception as e:
                self.mt5.market_book_release(symbol)
                print(e)
        
        #Не удалось открыть подписку на тикер
        else:
            self.mt5.market_book_release(symbol)
            return False
            
    def send_order_limit(self, id, symbol, lot, type_, stop_loss):
            lot = float(lot)
            
            action = self.mt5.TRADE_ACTION_PENDING

            #Подписываемся на получение данных по тикеру
            if self.mt5.market_book_add(symbol):
                # сделаем паузу в 3 секунды для добавления тикера в терминал
                #self.time.sleep(5)
                pass
            else:
                #Не удалось открыть подписку на тикер
                self.mt5.market_book_release(symbol)
                return False

            try:

                # Акции
                import re
                from datetime import datetime, timedelta
                quotes_temp = self.Ticker(re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', symbol)[0])
                # Свечи по акциям за период
                quotes = quotes_temp.candles(
                    date = (datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d"), 
                    till_date = datetime.now().strftime("%Y-%m-%d"), 
                    period='1m')
                #quotes_1d.head()
                quotes = self.pd.DataFrame(quotes)

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

#                 import yfinance as yf
#                 quotes_temp=yf.Ticker(symbol)
#                 quotes=quotes_temp.history(
#                     interval = "1m",# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
#                     period="1d"
#                 ) #  1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
#                 quotes.sort_index(ascending=True, inplace = True)
#                 quotes = quotes[-1:]
#                 price = quotes['Close'].values[0]

                if type_ == 'buy':
                    ORDER_TYPE = self.mt5.ORDER_TYPE_BUY_LIMIT
                    sl = round(price*(1 - stop_loss/100), 3)
                    
                    print('Выставляем ордер покупки ', symbol, 'по цене ', price)

                    request = {
                        "action": action,
                        "symbol": symbol,
                        "volume": lot,
                        "type": ORDER_TYPE,
                        "price": price,
                        "sl": sl,
                        "order": id,
                        "magic": id,#Уникальный идентификатор советника для работы с ордерами
                        "comment": "buy_limit",
                        "type_time": self.mt5.ORDER_TIME_DAY,
                        "type_filling": self.mt5.ORDER_FILLING_FOK,
                    }
                elif type_ == 'sell':
                    ORDER_TYPE = self.mt5.ORDER_TYPE_SELL_LIMIT
                    sl = 0
                    
                    print('Выставляем ордер продажи ', symbol, 'по цене ', price)

                    request = {
                        "action": action,
                        "symbol": symbol,
                        "volume": lot,
                        "type": ORDER_TYPE,
                        "price": price+10,
                        "order": id,
                        "magic": id,#Уникальный идентификатор советника для работы с ордерами
                        "comment": "sell_limit",
                        "type_time": self.mt5.ORDER_TIME_DAY,
                        "type_filling": self.mt5.ORDER_FILLING_FOK,
                    }
                # send a trading request
                result = self.mt5.order_send(request)
                self.mt5.market_book_release(symbol)
                return result
            except Exception as e:
                self.mt5.market_book_release(symbol)
                print(e)
                
    def change_price_order_limit(self, id, symbol):
        
#         # Акции
        import re
        from datetime import datetime, timedelta
        quotes_temp = self.Ticker(re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', symbol)[0])
        # Свечи по акциям за период
        quotes = quotes_temp.candles(
            date = (datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d"), 
            till_date = datetime.now().strftime("%Y-%m-%d"), 
            period='1m')
        #quotes_1d.head()
        quotes = self.pd.DataFrame(quotes)

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

#         import yfinance as yf
#         quotes_temp=yf.Ticker(symbol)
#         quotes=quotes_temp.history(
#             interval = "1m",# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
#             period="1d"
#         ) #  1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
#         quotes.sort_index(ascending=True, inplace = True)
#         quotes = quotes[-1:]
#         price = quotes['Close'].values[0]
        
        print('Обновляем цену ордера № ', id, 'Тикер ', symbol, 'по цене ', price)
        
        action = self.mt5.TRADE_ACTION_MODIFY
        
        ORDER_TYPE = self.mt5.ORDER_TYPE_SELL_LIMIT
        sl = 0
        
        request = {
            "action": action,
            "price": price,
            "order": id,
            "type_time": self.mt5.ORDER_TIME_GTC,
        }
        # send a trading request
        result = self.mt5.order_send(request)
        return result
        
    def delete_order(self, TDClient, id):
        action = self.mt5.TRADE_ACTION_REMOVE
        request = {
            "action": action,
            "order": id
        }
        # send a trading request
        result = self.mt5.order_send(request)
        return result        

