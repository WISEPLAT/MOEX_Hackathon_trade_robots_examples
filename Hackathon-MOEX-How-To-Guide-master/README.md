# 🏅Номинация «How to guide» - Как сделать торгового робота за 15 минут с нуля
## Пошаговое руководство Hackathon-MOEX-How-To-Guide

```
Перед прочтением этой статьи — ВАЖНО следующее: основная цель данной статьи заключается в том, чтобы показать 
как просто можно создать торгового робота, который может торговать российскими акциями или зарубежными акциями. 
Важно понимать, что создавая бота, вы лично несете ответственность за принимаемые им решения, инвестиционные 
операции и связанные с ними риски. Я не несу ответственности за решения, которые вы можете принять после 
прочтения этого материала. И я не даю никаких инвестиционных рекомендаций или советов. 
Не забывайте, что боты способны принести большие убытки, поэтому используйте их с осторожностью.

Пошаговое руководство по созданию торгового робота в рамках соревнования Хакатон [GO ALGO] организатором которого выступает биржа MOEX.
```

## Выбор брокера и библиотек
Как вы знаете, брокеров много))) но нам нужны те, у которых есть API — программный интерфейс через который наш торговый робот сможет отправлять заявки на покупку и продажу акций.

В этой статье будем рассматривать Российских брокеров для торговли Российскими акциями, если вы захотите торговать иностранными акциями — то это тоже можно сделать через них же — через СПБ биржу. (код торгового робота не поменяется — поменяется только название тикера — торговой бумаги, которой вы будете торговать).

Чтобы вас долго не мучать с выбором хорошего брокера для торгового бота, я приведу мои решения, которые сформировались после длительной практики по написанию торговых ботов, работающих в live режиме — прямо сейчас торгующих российскими акциями.

![alt text](https://raw.githubusercontent.com/WISEPLAT/imgs_for_repos/master/list01.jpg)
список сделок за сегодня, таймфрейм H1

Нужный и важный компонент в разработке торгового бота — это возможность тестирования вашей стратегии на истории, например используя простую библиотеку [Backtrader](https://github.com/WISEPLAT/backtrader ).

Итак приступим! )))

**1й вариант** — если очень сильно хочется иметь робота, который может торговать практически через любого брокера — то есть очень хорошее решение использовать библиотеку [QuikPy](https://github.com/cia76/QuikPy ) в связке с библиотекой [BackTraderQuik](https://github.com/cia76/BackTraderQuik ) — использование этих двух библиотек позволит вашему торговому роботу работать с любым брокером, у которого есть возможность предоставить вам торговый терминал **Quik**. А этот торговый терминал есть у большинства брокеров.

Множество примеров по этой связке специально для вас выложил [вот здесь](https://github.com/WISEPLAT/Learn-BackTrader ).

**2й вариант** — он немного ограничивает в выборе брокеров, но даёт прекрасную возможность общаться с разработчиками API брокеров, и они!!! заметьте быстро и эффективно исправляют косяки) и добавляют функционал — это большой плюс!

Для брокера Финам — библиотеки [FinamPy](https://github.com/cia76/FinamPy ) + [BackTraderFinam](https://github.com/cia76/BackTraderFinam )

Для брокера Тинькофф — библиотеки [TinkoffPy](https://github.com/cia76/TinkoffPy ) + [BackTraderTinkoff](https://github.com/cia76/BackTraderTinkoff )
* Несколько примеров кода опубликовал в их репозитории — [пример стратегии](https://github.com/Tinkoff/invest-python/blob/main/examples/wiseplat_live_strategy_print_ohlcv.py ) которая использует только API Тинькофф

Для брокера Алор — библиотеки [AlorPy](https://github.com/cia76/AlorPy ) и [BackTraderAlor](https://github.com/cia76/BackTraderAlor )

ОФФТОПИК: Если кому интересно подключение к криптобирже — то я написал свою библиотеку [backtrader_binance](https://github.com/WISEPLAT/backtrader_binance ), она работает так же, т. е. один и тот же код, можно использовать для разных активов, вот про [нее статья](https://habr.com/ru/articles/729036/ ).

Итак, выбираем последнего брокера — Алор. ))

## Приступаем к написанию торгового бота


Устанавливаем последнюю версию [Python 3.12.1](https://www.python.org/downloads/ );

Устанавливаем среду разработки [PyCharm Community 2023.1](https://www.jetbrains.com/pycharm/download/#section=windows );

Запускаем PyCharm Community;

В нём создаем новый проект, давайте его назовём **trade_robot_moex** и укажем что создаем виртуальное окружение Virtualenv => нажимаем «Create»;
![alt text](https://raw.githubusercontent.com/WISEPLAT/imgs_for_repos/master/list02.jpg)
 
Теперь нам нужна библиотека, которая поможет брать данные с биржи MOEX, выполняем команду:
```shell
git clone https://github.com/WISEPLAT/backtrader_moexalgo
```
она создает копию **backtrader_moexalgo** в нашем проекте

![alt text](https://raw.githubusercontent.com/WISEPLAT/imgs_for_repos/master/list03.jpg)

копируем уже готовый файл **01 - Live Trade - broker Alor.py** с примером торгового робота в корень нашего проекта

![alt text](https://raw.githubusercontent.com/WISEPLAT/imgs_for_repos/master/list04.jpg)

теперь клонируем дополнительные библиотеки

```shell
git clone https://github.com/cia76/AlorPy
```

```shell
git clone https://github.com/cia76/BackTraderAlor
```

они нужны, для live торговли, делают связку между API брокера и Backtrader

Теперь наш проект выглядит так:

![alt text](https://raw.githubusercontent.com/WISEPLAT/imgs_for_repos/master/list05.jpg)

Пришло время установить необходимые библиотеки

```shell
py -m ensurepip --upgrade
```


```shell
pip install numpy pandas backtrader moexalgo requests websockets
```

Теперь меняем путь к библиотеке backtrader_moexalgo (строка 8)

![alt text](https://raw.githubusercontent.com/WISEPLAT/imgs_for_repos/master/list06.jpg)

Создаем в корне проекта папку **my_config** и настраиваем файл **Config_Alor.py** для подключения к брокеру Алор через API.

Это нужно для возможности отправлять в рынок заявки на покупку и продажу акций.

Где взять пример файла с конфигурацией, показано на картинке ниже:

![alt text](https://raw.githubusercontent.com/WISEPLAT/imgs_for_repos/master/list07.jpg)

Теперь мы готовы запустить нашего первого торгового робота в жизнь! В live режиме он будет покупать и продавать акции!

## Запускаем!

![alt text](https://raw.githubusercontent.com/WISEPLAT/imgs_for_repos/master/list08.jpg)

На картинке выше 1 - это получение исторических данных с MOEX, после завершения их приема, мы переходим в Live режим - 2.

**Обучающее видео по работе с библиотекой backtrader_moexalgo можно посмотреть [на YouTube](https://youtu.be/SmcQF2jPxsQ ) и [на RuTube](https://rutube.ru/video/private/ba9e19f36c98d45ac9caf5b399dda6ca/?p=2T_4kwuwMz9aQAY3kFxYfQ )**


## Торговый робот создан и работает на рынке))

Вот выставилась заявка на покупку.

![alt text](https://raw.githubusercontent.com/WISEPLAT/imgs_for_repos/master/list09.jpg)

Весь код хорошо документирован, поэтому всё становится очевидным, когда на него посмотришь поближе:

```python
# git clone https://github.com/cia76/AlorPy
# git clone https://github.com/cia76/BackTraderAlor
# py -m ensurepip --upgrade
# pip install numpy pandas backtrader moexalgo requests websockets

import datetime as dt
import backtrader as bt
from backtrader_moexalgo.backtrader_moexalgo.moexalgo_store import MoexAlgoStore  # Хранилище AlgoPack

# пример live торговли для Алор
from BackTraderAlor.ALStore import ALStore  # Хранилище Alor
from AlorPy import AlorPy  # Работа с Alor OpenAPI V2
from my_config.Config_Alor import Config  # Файл конфигурации подключения к Alor


# Торговая система
class RSIStrategy(bt.Strategy):
    """
    Демонстрация live стратегии - однократно покупаем по рынку 1 лот и однократно продаем его по рынку через 3 бара
    """
    params = (  # Параметры торговой системы
        ('timeframe', ''),
        ('live_prefix', ''),  # префикс для выставления заявок в live
        ('info_tickers', []),  # информация по тикерам
    )

    def __init__(self):
        """Инициализация, добавление индикаторов для каждого тикера"""
        self.orders = {}  # Организовываем заявки в виде справочника, конкретно для этой стратегии один тикер - одна активная заявка
        for d in self.datas:  # Пробегаемся по всем тикерам
            self.orders[d._name] = None  # Заявки по тикеру пока нет

        # создаем индикаторы для каждого тикера
        self.sma1 = {}
        self.sma2 = {}
        self.rsi = {}
        for i in range(len(self.datas)):
            ticker = list(self.dnames.keys())[i]    # key name is ticker name
            self.sma1[ticker] = bt.indicators.SMA(self.datas[i], period=8)  # SMA indicator
            self.sma2[ticker] = bt.indicators.SMA(self.datas[i], period=16)  # SMA indicator
            self.rsi[ticker] = bt.indicators.RSI(self.datas[i], period=14)  # RSI indicator

        self.buy_once = {}
        self.sell_once = {}

    def start(self):
        for d in self.datas:  # Running through all the tickers
            self.buy_once[d._name] = False
            self.sell_once[d._name] = False

    def next(self):
        """Приход нового бара тикера"""
        for data in self.datas:  # Пробегаемся по всем запрошенным барам всех тикеров
            ticker = data._name
            status = data._state  # 0 - Live data, 1 - History data, 2 - None
            _interval = self.p.timeframe
            _date = bt.num2date(data.datetime[0])

            try:
                if data.p.supercandles[ticker][data.p.metric_name]:
                    print("\tSuper Candle:", data.p.supercandles[ticker][data.p.metric_name][0])
                    _data = data.p.supercandles[ticker][data.p.metric_name][0]
                    _data['datetime'] = _date
                    self.supercandles[ticker][data.p.metric_name].append(_data)
            except:
                pass

            if status in [0, 1]:
                if status: _state = "False - History data"
                else: _state = "True - Live data"

                print('{} / {} [{}] - Open: {}, High: {}, Low: {}, Close: {}, Volume: {} - Live: {}'.format(
                    bt.num2date(data.datetime[0]),
                    data._name,
                    _interval,  # таймфрейм тикера
                    data.open[0],
                    data.high[0],
                    data.low[0],
                    data.close[0],
                    data.volume[0],
                    _state,
                ))
                print(f'\t - {ticker} RSI : {self.rsi[ticker][0]}')

                if status != 0: continue  # если не live - то не входим в позицию!

                print(f"\t - Free balance: {self.broker.getcash()}")

                order = self.orders[data._name]  # Заявка тикера
                if order and order.status == bt.Order.Submitted:  # Если заявка не на бирже (отправлена брокеру)
                    return  # то ждем постановки заявки на бирже, выходим, дальше не продолжаем
                if not self.getposition(data):  # Если позиции нет
                    # if order and order.status == bt.Order.Accepted:  # Если заявка на бирже (принята брокером)
                    #     print(f"\t - Снимаем заявку на покупку {data._name}")
                    #     self.cancel(order)  # то снимаем ее

                    if not self.buy_once[ticker]:  # Enter long
                        free_money = self.broker.getcash()
                        print(f" - free_money: {free_money}")

                        lot = self.p.info_tickers[ticker]['securities']['LOTSIZE']
                        size = 1 * lot  # купим 1 лот - проверку на наличие денег не будем делать, считаем что они есть)
                        price = self.format_price(ticker, data.close[0] * 0.995)  # buy at close price -0.005% - to prevent buy
                        # price = 273.65

                        print(f" - buy {ticker} size = {size} at price = {price}")
                        self.orders[data._name] = self.buy(data=data, exectype=bt.Order.Limit, price=price, size=size)
                        print(f"\t - Выставлена заявка {self.orders[data._name]} на покупку {data._name}")

                        self.buy_once[ticker] = len(self)  # для однократной покупки + записываем номер бара

                else:  # Если есть позиция
                    print(self.sell_once[ticker], self.buy_once[ticker], len(self), len(self) > self.buy_once[ticker] + 3)
                    if not self.sell_once[ticker]:  # если мы еще не продаём
                        if self.buy_once[ticker] and len(self) > self.buy_once[ticker] + 3:  # если у нас есть позиция на 3-м баре после покупки
                            print("sell")
                            print(f"\t - Продаём по рынку {data._name}...")
                            self.orders[data._name] = self.close()  # закрываем позицию по рынку

                            self.sell_once[ticker] = True  # для предотвращения повторной продажи

    def notify_order(self, order):
        """Изменение статуса заявки"""
        order_data_name = order.data._name  # Имя тикера из заявки
        print("*"*50)
        self.log(f'Заявка номер {order.ref} {order.info["order_number"]} {order.getstatusname()} {"Покупка" if order.isbuy() else "Продажа"} {order_data_name} {order.size} @ {order.price}')
        if order.status == bt.Order.Completed:  # Если заявка полностью исполнена
            if order.isbuy():  # Заявка на покупку
                self.log(f'Покупка {order_data_name} Цена: {order.executed.price:.2f}, Объём: {order.executed.value:.2f}, Комиссия: {order.executed.comm:.2f}')
            else:  # Заявка на продажу
                self.log(f'Продажа {order_data_name} Цена: {order.executed.price:.2f}, Объём: {order.executed.value:.2f}, Комиссия: {order.executed.comm:.2f}')
                self.orders[order_data_name] = None  # Сбрасываем заявку на вход в позицию
        print("*" * 50)

    def notify_trade(self, trade):
        """Изменение статуса позиции"""
        if trade.isclosed:  # Если позиция закрыта
            self.log(f'Прибыль по закрытой позиции {trade.getdataname()} Общая={trade.pnl:.2f}, Без комиссии={trade.pnlcomm:.2f}')

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[0].datetime[0]) if not dt else dt  # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def format_price(self, ticker, price):
        """
        Функция округления до шага цены step, сохраняя signs знаков после запятой
        print(round_custom_f(0.022636, 0.000005, 6)) --> 0.022635
        """
        step = self.p.info_tickers[ticker]['securities']['MINSTEP']  # сохраняем минимальный Шаг цены
        signs = self.p.info_tickers[ticker]['securities']['DECIMALS']  # сохраняем Кол-во десятичных знаков

        val = round(price / step) * step
        return float(("{0:." + str(signs) + "f}").format(val))


def get_some_info_for_tickers(tickers, live_prefix):
    """Функция для получения информации по тикерам"""
    info = {}
    for ticker in tickers:
        i = store.get_symbol_info(ticker)
        info[f"{live_prefix}{ticker}"] = i
    return info


if __name__ == '__main__':

    # брокер Финам[FinamPy]: git clone https://github.com/cia76/FinamPy
    # брокер Алор[AlorPy]: git clone https://github.com/cia76/AlorPy
    # брокер Тинькофф[TinkoffPy]: git clone https://github.com/cia76/TinkoffPy
    # ЛЮБОЙ брокер у которого есть терминал Quik[QuikPy]: git clone https://github.com/cia76/QuikPy

    # пример для Алора
    exchange = 'MOEX'  # Биржа
    portfolio = Config.PortfolioStocks  # Портфель фондового рынка
    apProvider = AlorPy(Config.UserName, Config.RefreshToken)  # Подключаемся к торговому счету. Логин и Refresh Token берутся из файла Config.py
    live_prefix = 'MOEX.'  # префикс для выставления заявок в live
    store_alor = ALStore(providers=[dict(provider_name='alor_trade', username=Config.UserName, demo=False, refresh_token=Config.RefreshToken)])  # Хранилище Alor - Подключаемся к торговому счету. Логин и Refresh Token берутся из файла Config.py
    # - Подключение к брокеру с нашими учетными данными к выбранной бирже
    broker = store_alor.getbroker(use_positions=False, boards=Config.Boards, accounts=Config.Accounts)  # Брокер Alor

    symbol = 'SBER'  # Тикер в формате <Код тикера>
    # symbol2 = 'LKOH'  # Тикер в формате <Код тикера>
    store = MoexAlgoStore()  # Хранилище AlgoPack
    cerebro = bt.Cerebro(quicknotify=True)  # Инициируем "движок" BackTrader

    # live подключение к брокеру - для Offline закомментировать эти две строки
    cerebro.setbroker(broker)  # Устанавливаем live брокера

    # ----------------------------------------------------
    # Внимание! - Теперь это Live режим работы стратегии #
    # ----------------------------------------------------

    info_tickers = get_some_info_for_tickers([symbol, ], live_prefix)  # берем информацию о тикере (минимальный шаг цены, кол-во знаков после запятой)

    # live 1-минутные бары / таймфрейм M1
    timeframe = "M1"
    fromdate = dt.datetime.utcnow()
    data = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=1, dataname=symbol, fromdate=fromdate,
                         live_bars=True, name=f"{live_prefix}{symbol}")  # поставьте здесь True - если нужно получать live бары # name - нужен для выставления в live заявок
    # data2 = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=1, dataname=symbol2, fromdate=fromdate, live_bars=True)  # поставьте здесь True - если нужно получать live бары

    cerebro.adddata(data)  # Добавляем данные
    # cerebro.adddata(data2)  # Добавляем данные

    cerebro.addstrategy(RSIStrategy, timeframe=timeframe, live_prefix=live_prefix, info_tickers=info_tickers)  # Добавляем торговую систему

    cerebro.run()  # Запуск торговой системы
    # cerebro.plot()  # Рисуем график - в live режиме не нужно

```

Вся торговая система вынесена в отдельный класс, а торговая логика находится в методе **next**.

Получается очень удобно. 

Теперь у вас появился код первого рабочего торгового робота, который вы можете менять под свои условия стратегий.

## Важно
Исправление ошибок, доработка и развитие кода осуществляется автором и сообществом!

**Пушьте ваши коммиты!** 

## Условия использования
Программный код выложенный по адресу https://github.com/WISEPLAT/Hackathon-MOEX-How-To-Guide в сети интернет, реализующий торговую стратегию по акциям на фондовом рынке - это **Программа** созданная исключительно для удобства работы и изучения принципов - как сделать своего торгового робота.
При использовании **Программы** Пользователь обязан соблюдать положения действующего законодательства Российской Федерации или своей страны.
Использование **Программы** предлагается по принципу «Как есть» («AS IS»). Никаких гарантий, как устных, так и письменных не прилагается и не предусматривается.
Автор и сообщество не дает гарантии, что все ошибки **Программы** были устранены, соответственно автор и сообщество не несет никакой ответственности за
последствия использования **Программы**, включая, но, не ограничиваясь любым ущербом оборудованию, компьютерам, мобильным устройствам, 
программному обеспечению Пользователя вызванным или связанным с использованием **Программы**, а также за любые финансовые потери,
понесенные Пользователем в результате использования **Программы**.
Никто не ответственен за потерю данных, убытки, ущерб, включаю случайный или косвенный, упущенную выгоду, потерю доходов или любые другие потери,
связанные с использованием **Программы**.

**Программа** распространяется на условиях лицензии [MIT](https://choosealicense.com/licenses/mit).

==========================================================================
