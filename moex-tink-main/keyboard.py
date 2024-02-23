from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_spread = KeyboardButton("Спред")
button_set_proc_tvh = KeyboardButton("Сигнал изменения спреда от точки входа, %")
button_set_proc = KeyboardButton("Сигнал изменения спреда, %")
button_set = KeyboardButton("Сигнал изменения спреда, заданное значение")


greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).row(button_spread).row(button_set_proc_tvh).row(button_set_proc).row(button_set)
spread_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("USD"), KeyboardButton("EUR")).row(KeyboardButton("CNY"), KeyboardButton("MGNT")).row(KeyboardButton("Главное меню"))

usd_fiks_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущая ТВХ USD"), KeyboardButton("Новая ТВХ USD")).row(KeyboardButton("Сброс ТВХ USD"), KeyboardButton("Назад"))
eur_fiks_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущая ТВХ EUR"), KeyboardButton("Новая ТВХ EUR")).row(KeyboardButton("Сброс ТВХ EUR"), KeyboardButton("Назад"))
cny_fiks_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущая ТВХ CNY"), KeyboardButton("Новая ТВХ CNY")).row(KeyboardButton("Сброс ТВХ CNY"), KeyboardButton("Назад"))
mgnt_fiks_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущая ТВХ MGNT"), KeyboardButton("Новая ТВХ MGNT")).row(KeyboardButton("Сброс ТВХ MGNT"), KeyboardButton("Назад"))

usd_yes_no_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Новая точка входа USD по спреду")).row(KeyboardButton("Запись новой точки входа USD")).row(KeyboardButton("Назад"))
eur_yes_no_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Новая точка входа EUR по спреду")).row(KeyboardButton("Запись новой точки входа EUR")).row(KeyboardButton("Назад"))
cny_yes_no_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Новая точка входа CNY по спреду")).row(KeyboardButton("Запись новой точки входа CNY")).row(KeyboardButton("Назад"))
mgnt_yes_no_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Новая точка входа MGNT по спреду")).row(KeyboardButton("Запись новой точки входа MGNT")).row(KeyboardButton("Назад"))

usd_yes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Зафиксировать точку входа по USD")).row(KeyboardButton("Назад"))
eur_yes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Зафиксировать точку входа по EUR")).row(KeyboardButton("Назад"))
cny_yes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Зафиксировать точку входа по CNY")).row(KeyboardButton("Назад"))
mgnt_yes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Зафиксировать точку входа по MGNT")).row(KeyboardButton("Назад"))


usd_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить точку входа USD")).row(KeyboardButton("Назад"))
eur_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить точку входа EUR")).row(KeyboardButton("Назад"))
cny_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить точку входа CNY")).row(KeyboardButton("Назад"))
mgnt_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить точку входа MGNT")).row(KeyboardButton("Назад"))

signal_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("USD, %"), KeyboardButton("EUR, %")).row(KeyboardButton("CNY, %"), KeyboardButton("MGNT, %")).row(KeyboardButton("Главное меню"))

signal_only_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("USD. %"), KeyboardButton("EUR. %")).row(KeyboardButton("CNY. %"), KeyboardButton("MGNT. %")).row(KeyboardButton("Главное меню"))

usd_signal_only_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал в % по USD."), KeyboardButton("Новый сигнал в % по USD.")).row(KeyboardButton("Сброс сигнала в % по USD."), KeyboardButton("Отмена."))
eur_signal_only_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал в % по EUR."), KeyboardButton("Новый сигнал в % по EUR.")).row(KeyboardButton("Сброс сигнала в % по EUR."), KeyboardButton("Отмена."))
cny_signal_only_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал в % по CNY."), KeyboardButton("Новый сигнал в % по CNY.")).row(KeyboardButton("Сброс сигнала в % по CNY."), KeyboardButton("Отмена."))
mgnt_signal_only_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал в % по MGNT."), KeyboardButton("Новый сигнал в % по MGNT.")).row(KeyboardButton("Сброс сигнала в % по MGNT."), KeyboardButton("Отмена."))


usd_signal_only_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить сигнал USD.")).row(KeyboardButton("Отмена."))
eur_signal_only_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить сигнал EUR.")).row(KeyboardButton("Отмена."))
cny_signal_only_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить сигнал CNY.")).row(KeyboardButton("Отмена."))
mgnt_signal_only_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить сигнал MGNT.")).row(KeyboardButton("Отмена."))


usd_signal_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал в % по USD"), KeyboardButton("Новый сигнал в % по USD")).row(KeyboardButton("Сброс сигнала в % по USD"), KeyboardButton("Отмена"))
eur_signal_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал в % по EUR"), KeyboardButton("Новый сигнал в % по EUR")).row(KeyboardButton("Сброс сигнала в % по EUR"), KeyboardButton("Отмена"))
cny_signal_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал в % по CNY"), KeyboardButton("Новый сигнал в % по CNY")).row(KeyboardButton("Сброс сигнала в % по CNY"), KeyboardButton("Отмена"))
mgnt_signal_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал в % по MGNT"), KeyboardButton("Новый сигнал в % по MGNT")).row(KeyboardButton("Сброс сигнала в % по MGNT"), KeyboardButton("Отмена"))

usd_signal_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить сигнал USD")).row(KeyboardButton("Отмена"))
eur_signal_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить сигнал EUR")).row(KeyboardButton("Отмена"))
cny_signal_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить сигнал CNY")).row(KeyboardButton("Отмена"))
mgnt_signal_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Сбросить сигнал MGNT")).row(KeyboardButton("Отмена"))


signal_firstspread_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton(" USD, п "), KeyboardButton(" EUR, п ")).row(KeyboardButton(" CNY, п "), KeyboardButton("MGNT, п")).row(KeyboardButton("Главное меню"))

usd_signal_firstspread_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал по USD, п"), KeyboardButton("Новый сигнал по USD, п")).row(KeyboardButton("Сброс сигнала по USD, п"), KeyboardButton("-Отмена-"))
eur_signal_firstspread_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал по EUR, п"), KeyboardButton("Новый сигнал по EUR, п")).row(KeyboardButton("Сброс сигнала по EUR, п"), KeyboardButton("-Отмена-"))
cny_signal_firstspread_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал по CNY, п"), KeyboardButton("Новый сигнал по CNY, п")).row(KeyboardButton("Сброс сигнала по CNY, п"), KeyboardButton("-Отмена-"))
mgnt_signal_firstspread_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton("Текущий сигнал по MGNT, п"), KeyboardButton("Новый сигнал по MGNT, п")).row(KeyboardButton("Сброс сигнала по MGNT, п"), KeyboardButton("-Отмена-"))

usd_signal_firstspread_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton(" Сбросить сигнал USD, п ")).row(KeyboardButton("-Отмена-"))
eur_signal_firstspread_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton(" Сбросить сигнал EUR, п ")).row(KeyboardButton("-Отмена-"))
cny_signal_firstspread_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton(" Сбросить сигнал CNY, п ")).row(KeyboardButton("-Отмена-"))
mgnt_signal_firstspread_sbros_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(KeyboardButton(" Сбросить сигнал MGNT, п ")).row(KeyboardButton("-Отмена-"))