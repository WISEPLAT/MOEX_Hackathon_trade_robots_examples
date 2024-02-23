from FinamPy import FinamPy
from FinamPy.Config import Config

# Создайте массив для сохранения цен актива
asset_prices = []

# Флаг для отслеживания сохранения цен актива
asset_price_saved = False

print('start')
fp_provider = FinamPy(Config.AccessToken)

board = 'TQBR'
code = 'SBER'

def on_order_book(order_book):
    global asset_price_saved
    if not asset_price_saved:
        print('Saving asset price:', order_book.asks[0].price)
        asset_prices.append(order_book.asks[0].price)
        asset_price_saved = True

    print('ask:', order_book.asks[0].price)

# Установите обработчик события прихода подписки на стакан
fp_provider.on_order_book = on_order_book

# Подпишитесь на стакан
fp_provider.subscribe_order_book(code, board, 'orderbook1')

# Добавьте цикл ожидания для чтения данных
while not asset_price_saved:
    pass

# Выход
input('Enter - выход\n')

# Отпишитесь от стакана
fp_provider.unsubscribe_order_book('orderbook1', 'SBER', 'TQBR')
fp_provider.close_channel()

print(asset_prices)