import json
import os
import time

from FinamPy import FinamPy  # Работа с сервером TRANSAQ
from FinamPy.Config import Config  # Файл конфигурации


def createTxtFile(txt_file):
    try:
        f = open(txt_file, 'r')
    except FileNotFoundError as err:
        with open(txt_file, 'w') as fw:
            pass


def get_price(tickers, fp_provider):
    # Проверяем работу подписок
    securities = fp_provider.symbols  # Получаем справочник всех тикеров из провайдера
    prices = []
    prices_spot = []
    prices_quarterly = []
    prices_perp = []
    for i, ticker in enumerate(tickers):
        board = ticker['board']
        code = ticker['code']
        order_book_name = f'orderbook{i + 1}'  # Генерируем имя стакана с использованием счетчика
        print(code)


        # Подписываемся на стакан тикера
        fp_provider.subscribe_order_book(code, board, order_book_name)
        time.sleep(5)
        if code == tickers[0]['code']:
            fp_provider.on_order_book = lambda order_book: prices_spot.append({code: order_book.asks[0].price}) # Обработчик события прихода подписки на стакан
            time.sleep(15)
            print(prices_spot)
            print("")
        if code == tickers[1]['code']:
            fp_provider.on_order_book = lambda order_book: prices_quarterly.append({code: order_book.asks[0].price}) # Обработчик события прихода подписки на стака
            time.sleep(3)
            print(prices_quarterly)
            print("")
        if code == tickers[2]['code']:
            fp_provider.on_order_book = lambda order_book: prices_perp.append({code: order_book.asks[0].price}) # Обработчик события прихода подписки на стакан
            time.sleep(3)
            print(prices_perp)
            print("")
            print("")


        # Отписываемся от стакана тикера
        fp_provider.unsubscribe_order_book(order_book_name, code, board)

    if len(prices_spot) > 0 and len(prices_quarterly) > 0 and len(prices_perp) > 0:
        prices.append(prices_spot[-1])
        prices.append(prices_quarterly[-1])
        prices.append(prices_perp[-1])
        print(prices)
        print("")
        print("")

    else:
        print("Недостаточно элементов в списке для выполнения операции.")
        print("")
        print("")

    unique_prices = {}
    # Фильтруем список и оставляем только уникальные элементы
    filtered_prices = []
    for price_dict in prices:
        for key, value in price_dict.items():
            if key not in unique_prices:
                unique_prices[key] = value
                filtered_prices.append({key: value})

    print(filtered_prices)
    return filtered_prices


def calculate_difference(currience, basket_price):
    if currience == usd:
        quarterly = 'Si'
        perpetual = 'USDRUBF'
        x = 1000

    if currience == eur:
        quarterly = 'Eu'
        perpetual = 'EURRUBF'
        x = 1

    if currience == cny:
        quarterly = 'Cny'
        perpetual = 'CNYRUBF'
        x = 1

    # Проверка, что в списке есть как минимум три элемента
    if len(basket_price) >= 3:
        # Получаем второй и третий элементы
        second_element = basket_price[1]
        third_element = basket_price[2]

        # Извлекаем значения из элементов
        value_second = float(list(second_element.values())[0])
        value_third = float(list(third_element.values())[0]) / x

        # Вычисляем разницу
        difference = "{:.2f}".format(value_third - value_second)
        result = f"Спред {quarterly} - {perpetual}: {difference}"
        print(result)

        return result



# Запрос состояния от пользователя при запросе и запись при необходимости в файлы-----------------------------------------------------------------------------
def write_spread(currience, fp_provider):
    txt = 'usd.txt'
    if currience == eur:
        txt = 'eur.txt'
    if currience == cny:
        txt = 'cny.txt'

    basket_price = get_price(currience, fp_provider)
    data = calculate_difference(currience, basket_price)
    with open(txt, 'w', encoding="utf-8") as fw:
        pass
        json.dump(data, fw)


# СТАРТ-----------------------------------------------------------------------------
if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    fp_provider = FinamPy(Config.AccessToken)  # Провайдер работает со всеми счетами по токену (из файла Config.py)
    with open("prices.txt", "w") as file:
        file.truncate(0)


    # Создаем файлы под запрос пользователя-----------------------------------------------------------------------------
    request_files = ['request_usd.txt', 'request_eur.txt', 'request_cny.txt']
    for r in request_files:
        createTxtFile(r)

    createTxtFile('usd.txt')
    createTxtFile('eur.txt')
    createTxtFile('cny.txt')


    usd = (

        {'board': 'CETS', 'code': 'USD000000TOD'},  # USDRUB
        {'board': 'FUT', 'code': 'USDRUBF'},
        {'board': 'FUT', 'code': 'SiZ3'}  # SIZ3
    )

    eur = (

        {'board': 'CETS', 'code': 'EUR_RUB__TOD'},  # USDRUB
        {'board': 'FUT', 'code': 'EURRUBF'},
        {'board': 'FUT', 'code': 'EuZ3'}  # SIZ3
    )

    cny = (

        {'board': 'CETS', 'code': 'CNY000000TOD'},  # USDRUB
        {'board': 'FUT', 'code': 'CNYRUBF'},
        {'board': 'FUT', 'code': 'CRZ3'}  # SIZ3
    )

    while True:
        write_spread(usd, fp_provider)
        write_spread(eur, fp_provider)
        write_spread(cny, fp_provider)
        # Подписываемся на стакан тикера


        time.sleep(100)
