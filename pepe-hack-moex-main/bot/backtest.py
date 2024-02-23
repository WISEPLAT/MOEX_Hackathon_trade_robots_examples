from datetime import datetime, timedelta, date
import pandas as pd
import time
import requests
from forecasts.forecast import start_forecast_backtest
import threading
from bot import TradingBot_backtest
from enum import Enum

import warnings
warnings.filterwarnings('ignore')


ticker_to_name = {'AFLT': 'Аэрофлот', 'BANE': 'Башнефть', 'DSKY': 'Детский Мир', 'FEES': 'ФСК Россети', 'GAZP': 'Газпром', 'PHOR': 'ФосАгро', 'POSI': 'Positive Technologies', 'SBER': 'Сбер Банк', 'YNDX': 'Яндекс', 'MTLR': 'Мечел'}

class User:
    def __init__(self, end_investment, risk_level, money, stocks):
        self.end_investment = end_investment
        self.risk_level = risk_level
        self.money = money
        self.stocks = stocks
        self.price_prev_buy = {}


class BackTest:
    def __init__(self, time_interval, user):
        self.time_interval = time_interval
        self.user = user

        self.tradestats_data = pd.read_csv('./backtest_data/backtest_tradestats.csv', index_col=0)
        self.tradestats_data['ts'] = self.tradestats_data['ts'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
        self.obstats_data = pd.read_csv('./backtest_data/backtest_obstats.csv', index_col=0)
        self.obstats_data['ts'] = self.obstats_data['ts'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
        self.orderbook_data = pd.read_csv('./backtest_data/backtest_orderbook.csv', index_col=0)
        self.orderbook_data['ts'] = self.orderbook_data['ts'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

        self.tradestats = pd.read_csv('./backtest_data/backtest_tradestats_2023-10-01_2023-10-31.csv', index_col=0)
        self.tradestats['ts'] = self.tradestats['ts'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
        self.obstats = pd.read_csv('./backtest_data/backtest_obstats_2023-10-01_2023-10-31.csv', index_col=0)
        self.obstats['ts'] = self.obstats['ts'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
        self.orderbook = pd.read_csv('./backtest_data/backtest_orderbook_2023-10-01_2023-10-31.csv', index_col=0)
        self.orderbook['ts'] = self.orderbook['ts'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

        self.lot_size = pd.read_csv('./backtest_data/lot_size.csv', index_col=0)
        self.forecast = pd.DataFrame()

        self.stop_losses = {}#{'ticker': prise}
        self.orders_buy = {}#{'ticker': (prise, num_lots)}
        self.orders_sell = {}#{'ticker': (prise, num_lots)}

        self.new_data_was_adedd = False
        self.forecast_was_adedd = False

        self.thread = threading.Thread(target=self.start_test)

    def start_thread(self):
        self.thread.start()

    def terminate_thread(self):
        self.thread.terminate()

    def start_test(self):
        datetime_stop = self.user.end_investment
        # datetime_stop = datetime.strptime('2023-11-14 18:40:00', "%Y-%m-%d %H:%M:%S")
        cur_datetime = datetime.strptime('2023-11-01 10:05:00', "%Y-%m-%d %H:%M:%S")
        print('ТЕСТ НАЧАЛСЯ\n')

        while True:
            new_tradestats = self.tradestats_data[self.tradestats_data.ts == cur_datetime]
            self.tradestats = pd.concat([self.tradestats, new_tradestats])

            new_obstats = self.obstats_data[self.obstats_data.ts == cur_datetime]
            self.obstats = pd.concat([self.obstats, new_obstats])

            new_orderbook = self.orderbook_data[self.orderbook_data.ts == cur_datetime]
            self.orderbook = pd.concat([self.orderbook, new_orderbook])

            print('\n', '#'*80)
            print('Дата: ', cur_datetime, '\n')
            print('@'*20)
            print(f'Портфель: {round(self.user.money, 2)} рублей')
            print('Акции:')
            m = 0
            for stock in self.user.stocks.keys():
                if self.user.stocks[stock] != 0:
                    lot_size = self.lot_size[self.lot_size.ticker == stock].lot_size.values[0]
                    cur_pr = new_tradestats[new_tradestats.secid == stock].pr_close.values[0]
                    m += self.user.stocks[stock] * cur_pr * lot_size
                    print(f'{stock}: {self.user.stocks[stock]} лотов')
            print(f'Общая ценность портфеля: {round(m + self.user.money, 2)} рублей')
            print('@' * 20, '\n')

            self.check_stop_losses()
            self.check_orders()

            self.set_new_data_was_adedd(True)

            if cur_datetime == datetime_stop:
                print('ТЕСТ ЗАКОНЧЕН')
                time.sleep(self.time_interval)
                break



            l = list(self.user.stocks.keys())
            for ticker in l:
                cur_pr = new_tradestats[new_tradestats.secid == ticker].pr_close.values[0]
                lot_size = self.lot_size[self.lot_size.ticker == stock].lot_size.values[0]
                if ticker in self.user.price_prev_buy.keys() and ticker in self.user.stocks.keys():
                    update_stock_info(0, ticker_to_name[ticker], lot_size*self.user.stocks[ticker], self.user.price_prev_buy[ticker], cur_pr)




            cur_datetime = self.set_cur_datetime(cur_datetime)

            time.sleep(self.time_interval)

    def set_cur_datetime(self, cur_datetime):
        cur_datetime += timedelta(minutes=5)

        if cur_datetime.time() == datetime.strptime('18:45:00', '%H:%M:%S').time():
            cur_datetime += timedelta(days=1)
            cur_datetime = cur_datetime.replace(minute=5, hour=10)

        if cur_datetime.weekday() == 5:
            cur_datetime += timedelta(days=2)

        return cur_datetime

    def get_new_data_was_adedd(self):
        return self.new_data_was_adedd

    def set_new_data_was_adedd(self, value):
        self.new_data_was_adedd = value

    def get_forecast_was_adedd(self):
        return self.forecast_was_adedd

    def set_forecast_was_adedd(self, value):
        self.forecast_was_adedd = value

    def set_forecast(self, value):
        self.forecast = value

    def get_tradestats(self):
        return self.tradestats

    def get_obstats(self):
        return self.obstats

    def get_orderbook(self):
        return self.orderbook

    def set_order_buy(self, ticker, offered_price, num_lots):
        print(f'Установлена заявка на покупку {num_lots}, {ticker}, Цена покупки: {offered_price}')
        self.orders_buy[ticker] = (offered_price, num_lots)

    def set_order_sell(self, ticker, offered_price, num_lots):
        print(f'Установлена заявка на продажу {num_lots}, {ticker}, Цена продажи: {offered_price}')
        self.orders_sell[ticker] = (offered_price, num_lots)

    def check_orders(self):
        for ticker in self.orders_sell.keys():
            pr_h = self.tradestats[self.tradestats.secid == ticker].pr_high.values[-1]

            if pr_h < self.orders_sell[ticker]:
                lot_size = self.lot_size[self.lot_size.ticker == ticker].lot_size.values[0]
                num_stocks = self.orders_sell[ticker][1] * lot_size
                order_size = self.orders_sell[ticker][0] * num_stocks

                if lot_size <= self.user.stocks[ticker]:
                    self.user.stocks[ticker] -= self.orders_sell[ticker][1]

                    self.user.money += order_size



                    mon_in_stoks = 0
                    cur_date = self.tradestats.ts.max()
                    cur_data = self.tradestats[self.tradestats.ts == cur_date]
                    for stock in self.user.stocks.keys():
                        if self.user.stocks[stock] != 0:
                            lot_size = self.lot_size[self.lot_size.ticker == stock].lot_size.values[0]
                            cur_pr = cur_data[cur_data.secid == stock].pr_close.values[0]
                            mon_in_stoks += self.user.stocks[stock] * cur_pr * lot_size

                    cur_bal = self.user.money + mon_in_stoks
                    update_balance(current_balance=cur_bal)


                    add_bot_action(0, ticker_to_name[ticker], num_stocks, BotActionType.SELL, BotActionColor.RED, order_size,
                                   '', cur_date)


                    print(f'Бумага {ticker} в кол-ве {num_stocks} лота продана по цене {self.orders_sell[ticker][0]}, покупалась по {self.user.price_prev_buy[ticker]}')
                    del self.orders_sell[ticker]
                    del self.user.price_prev_buy[ticker]

        ks = list(self.orders_buy.keys())
        for ticker in ks:
            pr_l = self.tradestats[self.tradestats.secid == ticker].pr_low.values[-1]

            if self.orders_buy[ticker] != () and pr_l > self.orders_buy[ticker][0]:
                lot_size = self.lot_size[self.lot_size.ticker == ticker].lot_size.values[0]
                num_stocks = self.orders_buy[ticker][1] * lot_size
                order_size = self.orders_buy[ticker][0] * num_stocks

                if order_size < self.user.money:
                    self.user.stocks[ticker] += self.orders_buy[ticker][1]
                    self.user.money -= order_size

                    mon_in_stoks = 0
                    cur_date = self.tradestats.ts.max()
                    cur_data = self.tradestats[self.tradestats.ts == cur_date]
                    for stock in self.user.stocks.keys():
                        if self.user.stocks[stock] != 0:
                            lot_size = self.lot_size[self.lot_size.ticker == stock].lot_size.values[0]
                            cur_pr = cur_data[cur_data.secid == stock].pr_close.values[0]
                            mon_in_stoks += self.user.stocks[stock] * cur_pr * lot_size

                    cur_bal = self.user.money + mon_in_stoks
                    update_balance(current_balance=cur_bal)


                    add_bot_action(0, ticker_to_name[ticker], num_stocks, BotActionType.PURCHASE, BotActionColor.GREEN, order_size,
                                   '', cur_date)


                    print(f'Бумага {ticker} в кол-ве {num_stocks} лота куплена по цене {self.orders_buy[ticker][0]}. Объем покупки = {order_size} рублей')
                    del self.orders_buy[ticker]

    def set_stop_loss(self, ticker, stop_loss):
        print(f'Установлен стоп-лосс {ticker}: {stop_loss}')
        self.stop_losses[ticker] = stop_loss

    def del_stop_loss(self, ticker):
        del self.stop_losses[ticker]

    def check_stop_losses(self):
        stop_losses = list(self.stop_losses.keys())
        for ticker in stop_losses:
            pr_low = self.tradestats[self.tradestats.secid == ticker].pr_low.values[-1]
            if pr_low <= self.stop_losses[ticker] and self.user.stocks[ticker] != 0:
                lot_size = self.lot_size[self.lot_size.ticker == ticker].lot_size.values[0]
                num_stocks = self.user.stocks[ticker] * lot_size
                order_size = self.stop_losses[ticker] * num_stocks

                self.user.stocks[ticker] = 0
                self.user.money += order_size


                mon_in_stoks = 0
                cur_date = self.tradestats.ts.max()
                cur_data = self.tradestats[self.tradestats.ts == cur_date]
                for stock in self.user.stocks.keys():
                    if self.user.stocks[stock] != 0:
                        lot_size = self.lot_size[self.lot_size.ticker == stock].lot_size.values[0]
                        cur_pr = cur_data[cur_data.secid == stock].pr_close.values[0]
                        mon_in_stoks += self.user.stocks[stock] * cur_pr * lot_size

                cur_bal = self.user.money + mon_in_stoks
                update_balance(current_balance=cur_bal)


                add_bot_action(0, ticker_to_name[ticker], num_stocks, BotActionType.SELL, BotActionColor.RED, order_size, 'По стоп-лозу', cur_date)



                print(f'Бумага {ticker} в кол-ве {num_stocks} лота продана по стоп-лосу по цене {order_size}')

                del self.user.price_prev_buy[ticker]
                del self.stop_losses[ticker]




#######################################################################################################################
#######################################################################################################################
#######################################################################################################################



def back_test_on_front_start(money, time_interval):
    while True:
        if is_bot_running():
            delete_bot_history()
            delete_stocks()

            end_investment, risk_level = get_bot_info()

            tickers = ['AFLT', 'BANE', 'DSKY', 'FEES', 'GAZP', 'PHOR', 'POSI', 'SBER', 'YNDX', 'MTLR']
            stocks = {ticker: 0 for ticker in tickers}
            user = User(end_investment=end_investment, risk_level=risk_level, money=money, stocks=stocks)
            update_balance(0, user.money, user.money)

            backtest = BackTest(time_interval, user)

            trading_bot = TradingBot_backtest(user, backtest)

            backtest.start_thread()
            trading_bot.start_thread()
            thread_forecast_backtest = threading.Thread(target=start_forecast_backtest, args=[backtest])
            thread_forecast_backtest.start()

            # СДЕЛАТЬ СТОП БОТА
            while True:
                if not is_bot_running():
                    backtest.terminate_thread()
                    trading_bot.terminate_thread()
                    thread_forecast_backtest.terminate()

                break

def is_bot_running(user_id: int = 0):
    return requests.get(f"http://127.0.0.1:8000/bot/?user_id={user_id}").json()["state"] == 1

def update_balance(user_id: int = 0, initial_balance: float = None, current_balance: float = None):
    request = f"http://127.0.0.1:8000/bot/balance?user_id={user_id}"

    if initial_balance:
        request += f"&initial_balance={initial_balance}"
    if current_balance:
        request += f"&current_balance={current_balance}"

    return requests.post(request).json()


def update_stock_info(user_id: int = 0, company_name: str = "Unspecified",
                      stocks_count: int = 0, purchase_price: float = 0, current_price: float = 0):
    return requests.post(f"http://127.0.0.1:8000/bot/stocks?user_id={user_id}&company_name={company_name}&stocks_count={stocks_count}&purchase_price={purchase_price}&current_price={current_price}").json()

def delete_stocks(user_id: int = 0, company_name: str = None):
    request = f"http://127.0.0.1:8000/bot/stocks?user_id={user_id}"

    if company_name:
        request += f"&company_name={company_name}"

    return f"Deleted {requests.delete(request).json()} position(s)"

def get_bot_info(user_id: int = 0):
    bot_info = requests.get("http://127.0.0.1:8000/bot/?user_id=0").json()

    return bot_info["dateTo"], bot_info["riskLevel"]


class BotActionType(Enum):
    PURCHASE = "Покупка"
    SELL = "Продажа"

class BotActionColor(Enum):
    GREEN = "#06AB03"
    RED = "#FF0000"


def add_bot_action(user_id: int = 0, company_name: str = "Unspecified",
                   stocks_count: int = 0,
                   action: BotActionType = BotActionType.PURCHASE,
                   action_color: BotActionColor = BotActionColor.GREEN,
                   profit: float = 0, comment: str = "Comment",
                   action_datetime=datetime.now().isoformat()):
    args = locals()

    request = f"http://127.0.0.1:8000/bot/history?user_id={user_id}"

    for arg_name, arg_value in args.items():
        if isinstance(arg_value, BotActionType) or isinstance(arg_value, BotActionColor):
            arg_value = arg_value.value.replace("#", "%23")

        request += f"&{arg_name}={arg_value}"

    return requests.post(request).json()


def delete_bot_history(user_id: int = 0):
    request = f"http://127.0.0.1:8000/bot/history?user_id={user_id}"

    return f"Deleted {requests.delete(request).json()} position(s)"



if __name__ == "__main__":
    money = 100000
    time_interval = 3
    back_test_on_front_start(money, time_interval)

    # процент брокера добавить
    # time_interval = 3
    # tickers = ['AFLT', 'BANE', 'DSKY', 'FEES', 'GAZP', 'PHOR', 'POSI', 'SBER', 'YNDX', 'MTLR']
    # stocks = {ticker: 0 for ticker in tickers}
    #
    # end_investment = datetime.strptime('2023-11-14 18:40:00', "%Y-%m-%d %H:%M:%S")
    # # datetime.strptime('30-11-2023 12:00:00', "%d-%m-%Y %H:%M:%S")
    #
    # user = User(end_investment=end_investment, risk_level=3, money=100000, stocks=stocks)
    #
    # backtest = BackTest(time_interval, user)
    # trading_bot = TradingBot_backtest(user, backtest)
    #
    # backtest.start_thread()
    # trading_bot.start_thread()
    # thread_forecast_backtest = threading.Thread(target=start_forecast_backtest, args=[backtest])
    # thread_forecast_backtest.start()

