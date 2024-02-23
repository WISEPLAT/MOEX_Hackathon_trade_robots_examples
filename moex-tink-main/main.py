import json
import time
import emoji
from FinamPy import FinamPy
from FinamPy.Config import Config

MAX_ATTEMPTS = 10
WAIT_INTERVAL_SECONDS = 10


def subscribe_and_save_price(asset, result_prices_arr):
    fp_provider = FinamPy(Config.AccessToken)
    print(asset)

    def on_order_book(order_book):
        if asset['code'] not in result_prices_arr:
            result_prices_arr[asset['code']] = order_book.asks[0].price

    fp_provider.on_order_book = on_order_book
    fp_provider.subscribe_order_book(asset['code'], asset['board'], 'orderbook1')

    # Добавьте цикл ожидания с ограничением по попыткам
    attempts = 0
    while asset['code'] not in result_prices_arr and attempts < MAX_ATTEMPTS:
        time.sleep(WAIT_INTERVAL_SECONDS)
        attempts += 1

    if asset['code'] not in result_prices_arr:
        print(f"Котировки для {asset['code']} не пришли после {MAX_ATTEMPTS} попыток.")
        return False

    fp_provider.unsubscribe_order_book('orderbook1', asset['code'], asset['board'])
    fp_provider.close_channel()

def calculate_difference(currience, basket_price):
    if currience == usd:
        quarterly = 'Si'
        perpetual = 'USDRUBF'
        x = 1000

    if currience == eur:
        quarterly = 'Eu'
        perpetual = 'EURRUBF'
        x = 1000

    if currience == cny:
        quarterly = 'Cny'
        perpetual = 'CNYRUBF'
        x = 1

    # Проверка, что в списке есть как минимум три элемента
    if len(basket_price) >= 3:
        # Получаем второй и третий элементы
        values = list(basket_price.values())
        first_element = values[0]
        second_element = values[1]
        third_element = values[2]

        # Извлекаем значения из элементов
        value_first = float(first_element)
        value_second = float(second_element)
        value_third = float(third_element) / x

        # Вычисляем разницу
        difference = "{:.3f}".format(value_third - value_second)
        result = f"Спред {quarterly} - {perpetual}: {difference}\n"

        if float(second_element) > float(first_element):
            difference1 = f"{perpetual}: {'{:.3f}'.format(value_second)} > cпот: {'{:.3f}'.format(value_first)}\n"
        if float(second_element) < float(first_element):
            difference1 = f"Cпот: {'{:.3f}'.format(value_first)} > {perpetual}: {'{:.3f}'.format(value_second)}\n"
        if '{:.3f}'.format(float(second_element)) == '{:.3f}'.format(float(first_element)):
            difference1 = f"Cпот: {'{:.3f}'.format(value_first)} = {perpetual}: {'{:.3f}'.format(value_second)}\n"

        result = result + difference1
        print(result)

        return result

def write_spread(currience, diff):
    txt = 'usd.txt'
    if currience == eur:
        txt = 'eur.txt'
    if currience == cny:
        txt = 'cny.txt'

    with open(txt, 'w', encoding='utf-8') as file:
        pass
        file.write(diff)

def write_connection_error(currience, diff):
    txt = 'usd.txt'
    if currience == eur:
        txt = 'eur.txt'
    if currience == cny:
        txt = 'cny.txt'

    with open(txt, 'w', encoding='utf-8') as file:
        pass
        file.write(diff)


def write_signal_to_file(signal, signal_txt):
    with open('sig_proc.txt', 'a', encoding='utf-8') as file:
        file.write(signal + '\n')
    with open(signal_txt, 'w') as file:
        pass


# Чтение значения x из файла usd_tvh.txt
def read_x_from_file(tvh_txt):
    try:
        with open(tvh_txt, 'r') as file:
            x = float(file.read())
        return x
    except FileNotFoundError:
        # Обработка случая, когда файл не найден
        return None
    except ValueError:
        # Обработка случая, когда содержимое файла не является числом
        return None


def read_firstspread_and_signal_from_file(tvh_txt):
    try:
        with open(tvh_txt, 'r') as file:
            data = file.read().split(', ')
            values = [float(value) for value in data]
            return values
    except FileNotFoundError:
        # Обработка случая, когда файл не найден
        return None
    except ValueError:
        # Обработка случая, когда содержимое файла не является числом или не может быть разделено запятой и пробелом
        return None



# Чтение значения y из файла usd_signal.txt
def read_y_from_file(signal_txt):
    try:
        with open(signal_txt, 'r') as file:
            y = float(file.read())
        return y
    except FileNotFoundError:
        # Обработка случая, когда файл не найден
        return None
    except ValueError:
        # Обработка случая, когда содержимое файла не является числом
        return None

def check_signal(curr, spread_txt, tvh_txt, signal_txt):
    with open(spread_txt, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        if "Спред" in line:
            parts = line.split()
            x_index = parts.index('Спред') + 4
            spread = parts[x_index]
    z = float(spread)  # Замените это на получение текущего значения z
    if read_x_from_file(tvh_txt) is not None and read_y_from_file(signal_txt) is not None:
        x = float(read_x_from_file(tvh_txt))  # Замените это на получение текущего значения x
        y = float(read_y_from_file(signal_txt))  # Замените это на получение текущего значения y

    # Проверяем условия и записываем сигнал, если они выполняются
        if z >= x + x / 100 * y:
            bell_emoji = "🔔"
            signal = f"{bell_emoji}{curr}: спред вырос на {y}%"
            write_signal_to_file(signal, signal_txt)
        elif z <= x - x / 100 * y:
            bell_emoji = "🔔"
            signal = f"{bell_emoji}{curr}: спред снизился на {y}%"
            write_signal_to_file(signal, signal_txt)


def check_only_signal(curr, spread_txt, signal_txt):
    with open(spread_txt, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        if "Спред" in line:
            parts = line.split()
            x_index = parts.index('Спред') + 4
            spread = parts[x_index]
    z = float(spread)  # Замените это на получение текущего значения z
    if read_firstspread_and_signal_from_file(signal_txt) is not None:
        x = read_firstspread_and_signal_from_file(signal_txt) # Замените это на получение текущего значения y


    # Проверяем условия и записываем сигнал, если они выполняются
        if float(x[0]) < float(x[1]):
            if z >= float(x[1]):
                bell_emoji = "🔔"
                signal = f"{bell_emoji}{curr}: спред вырос до {x[1]}"
                write_signal_to_file(signal, signal_txt)
        elif  float(x[0]) > float(x[1]):
            if z <= float(x[1]):
                bell_emoji = "🔔"
                signal = f"{bell_emoji}{curr}: спред снизился до {x[1]}"
                write_signal_to_file(signal, signal_txt)

# Создаем файлы под запрос пользователя о позах-----------------------------------------------------------------------------
def createTxtFile(txt_file):
    try:
        f = open(txt_file, 'r')
    except FileNotFoundError as err:
        with open(txt_file, 'w') as fw:
            pass

usd = (

    {'board': 'CETS', 'code': 'USD000UTSTOM'},  # USDRUB
    {'board': 'FUT', 'code': 'USDRUBF'},
    {'board': 'FUT', 'code': 'SiZ3'}  # SIZ3
)

eur = (

    {'board': 'CETS', 'code': 'EUR_RUB__TOM'},  # USDRUB
    {'board': 'FUT', 'code': 'EURRUBF'},
    {'board': 'FUT', 'code': 'EuZ3'}  # SIZ3
)

cny = (

    {'board': 'CETS', 'code': 'CNYRUB_TOM'},  # USDRUB
    {'board': 'FUT', 'code': 'CNYRUBF'},
    {'board': 'FUT', 'code': 'CRZ3'}  # SIZ3
)

# Создаем файлы для оповещения по сигналу
createTxtFile('usd_firstspread_and_signal.txt')
createTxtFile('eur_firstspread_and_signal.txt')
createTxtFile('cny_firstspread_and_signal.txt')

while True:


    try:
        f = open('sig_proc.txt', 'r')
    except FileNotFoundError as err:
        with open('sig_proc.txt', 'w') as fw:
            pass

    # Создайте словарь для сохранения цен активов
    usd_prices = {}
    eur_prices = {}
    cny_prices = {}

    # Подпишитесь на стакан для каждого актива
    for asset in usd:
        subscribe_and_save_price(asset, usd_prices)
        if not subscribe_and_save_price(asset, usd_prices):
            write_connection_error(usd, "Котировки отсутствуют")
            # Если subscribe_and_save_price вернуло False, перезапустите цикл
            continue

    # В asset_prices будут сохранены цены активов
    print(usd_prices)
    diff = calculate_difference(usd, usd_prices)
    if diff is not None:
        write_spread(usd, diff)


    # Подпишитесь на стакан для каждого актива
    for asset in eur:
        subscribe_and_save_price(asset, eur_prices)
        if not subscribe_and_save_price(asset, eur_prices):
            write_connection_error(eur, "Котировки отсутствуют")
            # Если subscribe_and_save_price вернуло False, перезапустите цикл
            continue

    # В asset_prices будут сохранены цены активов
    print(eur_prices)
    diff = calculate_difference(eur, eur_prices)
    if diff is not None:
        write_spread(eur, diff)


    # Подпишитесь на стакан для каждого актива
    for asset in cny:
        subscribe_and_save_price(asset, cny_prices)
        if not subscribe_and_save_price(asset, cny_prices):
            write_connection_error(cny, "Котировки отсутствуют")
            # Если subscribe_and_save_price вернуло False, перезапустите цикл
            continue

    # В asset_prices будут сохранены цены активов
    print(cny_prices)
    diff = calculate_difference(cny, cny_prices)
    if diff is not None:
        write_spread(cny, diff)



    # Для примера, я задам их статически________________________________________________________________________________

    check_signal('USD', 'usd.txt', 'usd_tvh.txt', 'usd_signal.txt')
    check_signal('EUR', 'eur.txt', 'eur_tvh.txt', 'eur_signal.txt')
    check_signal('CNY', 'cny.txt', 'cny_tvh.txt', 'cny_signal.txt')
    check_signal('USD', 'usd.txt', 'usd_spread_only.txt', 'usd_signal_only.txt')
    check_signal('EUR', 'eur.txt', 'eur_spread_only.txt', 'eur_signal_only.txt')
    check_signal('CNY', 'cny.txt', 'cny_spread_only.txt', 'cny_signal_only.txt')
    check_only_signal('USD', 'usd.txt', 'usd_firstspread_and_signal.txt')
    check_only_signal('EUR', 'eur.txt', 'eur_firstspread_and_signal.txt')
    check_only_signal('CNY', 'cny.txt', 'cny_firstspread_and_signal.txt')


    time.sleep(5)

