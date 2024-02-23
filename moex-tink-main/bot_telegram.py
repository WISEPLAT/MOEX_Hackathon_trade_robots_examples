import json
import re
from datetime import datetime
import os
import emoji
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor

from keyboard import *

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext, storage


class YourState(StatesGroup):
    new_usd = State()
    new_usd_only = State()
    new_usd_tvh = State()
    new_usd_spread_first = State()

    new_eur = State()
    new_eur_only = State()
    new_eur_tvh = State()
    new_eur_spread_first = State()

    new_cny = State()
    new_cny_only = State()
    new_cny_tvh = State()
    new_cny_spread_first = State()

    new_mgnt = State()
    new_mgnt_only = State()
    new_mgnt_tvh = State()
    new_mgnt_spread_first = State()


checkmark = "✅"
token = '5814873337:AAFmEDxaPRXmg8w1HQ4FTiNB1U5l8pgtFgE'

bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())

current_datetime = datetime.now()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>'
    await bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=greet_kb1)

@dp.message_handler(Text(equals="Спред"))
async def with_puree(message: types.Message):
    with open('request_pos.txt', 'w') as fw:
        status = 'request'
        json.dump(status, fw)
    mess = 'Выберите актив:'
    await bot.send_message(message.chat.id, mess, reply_markup=spread_keyboard)

@dp.message_handler(Text(equals="Сигнал изменения спреда от точки входа, %"))
async def with_puree(message: types.Message):
    # открываем файл в режиме чтения
    mess = 'Выберите актив'
    await bot.send_message(message.chat.id, mess, reply_markup=signal_keyboard)

@dp.message_handler(Text(equals="Сигнал изменения спреда, %"))
async def with_puree(message: types.Message):
    # открываем файл в режиме чтения
    mess = 'Выберите актив'
    await bot.send_message(message.chat.id, mess, reply_markup=signal_only_keyboard)

@dp.message_handler(Text(equals="Сигнал изменения спреда, заданное значение"))
async def with_puree(message: types.Message):
    # открываем файл в режиме чтения
    mess = 'Выберите актив'
    await bot.send_message(message.chat.id, mess, reply_markup=signal_firstspread_keyboard)

@dp.message_handler(Text(equals="Главное меню"))
async def back_to_previous_menu(message: types.Message):
    mess = 'Главное меню'
    await bot.send_message(message.chat.id, mess, reply_markup=greet_kb1)

@dp.message_handler(Text(equals="Назад"))
async def back_to_previous_menu(message: types.Message):
    mess = 'Выберите актив:'
    await bot.send_message(message.chat.id, mess, reply_markup=spread_keyboard)

@dp.message_handler(Text(equals="Отмена"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Выберите актив'
    await bot.send_message(message.chat.id, mess, reply_markup=signal_keyboard)

@dp.message_handler(Text(equals="-Отмена-"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Выберите актив'
    await bot.send_message(message.chat.id, mess, reply_markup=signal_firstspread_keyboard)

@dp.message_handler(Text(equals="Отмена."))
async def fix_usd_tvh(message: types.Message):
    mess = 'Выберите актив'
    await bot.send_message(message.chat.id, mess, reply_markup=signal_only_keyboard)






@dp.message_handler(Text(equals="USD"))
async def action1(message: types.Message):
    # Здесь вы можете выполнять необходимые действия для "Действие 1"

    with open('usd.txt', 'r', encoding='utf-8') as fr:
        mess = fr.read()  # Corrected to call the read() method
        await bot.send_message(message.chat.id, mess, reply_markup=usd_fiks_keyboard)

@dp.message_handler(Text(equals="Текущая ТВХ USD"))
async def current_signal_usd(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        with open("usd_tvh.txt", "r") as file:
            tvh = file.read()
            if not tvh:
                await message.answer("Точка входа по USD не установлена", reply_markup=usd_fiks_keyboard)
            else:
                await message.answer(f"Точка входа по USD: {tvh}", reply_markup=usd_fiks_keyboard)
    except FileNotFoundError:
        await message.answer("Точка входа не найдена", reply_markup=usd_fiks_keyboard)

@dp.message_handler(Text(equals="Новая ТВХ USD"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Зафиксировать новую точку входа USD по спреду или вручную?'
    await bot.send_message(message.chat.id, mess, reply_markup=usd_yes_no_keyboard)


@dp.message_handler(Text(equals="Новая точка входа USD по спреду"))
async def fix_usd_tvh(message: types.Message):
    usd_tvh_file = 'usd_tvh.txt'

    if os.path.exists(usd_tvh_file):
        # Проверьте, является ли файл пустым
        is_empty = not bool(open(usd_tvh_file, 'r', encoding='utf-8').read())

        if is_empty:
            with open(usd_tvh_file, 'a', encoding='utf-8') as fw:
                with open('usd.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                x = None
                for line in lines:
                    if "Спред Si - USDRUBF:" in line:
                        parts = line.split()
                        x_index = parts.index('Спред') + 4
                        x = parts[x_index]
                        break

                if x is not None:
                    data_to_write = x
                    fw.write(data_to_write)
                    await message.answer(f"{checkmark}Точка входа {x} для USD зафиксирована.", reply_markup=usd_fiks_keyboard)
                else:
                    await message.answer("Не удалось найти точку входа для USD.", reply_markup=usd_fiks_keyboard)
        else:
            await message.answer("Есть зафиксированная точка входа. Для записи новой точки сбросьте старую.", reply_markup=usd_fiks_keyboard)
    else:
        # Файл не существует, создайте его и записывайте информацию
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            with open('usd.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            x = None
            for line in lines:
                if "Спред Si - USDRUBF:" in line:
                    parts = line.split()
                    x_index = parts.index('Спред') + 4
                    x = parts[x_index]
                    break

            if x is not None:
                data_to_write = x
                fw.write(data_to_write)
                await message.answer(f"{checkmark}Точка входа {x} для USD зафиксирована.", reply_markup=usd_fiks_keyboard)
            else:
                await message.answer("Не удалось найти точку входа для USD.", reply_markup=usd_fiks_keyboard)


@dp.message_handler(Text(equals="USD, %"))
async def with_puree(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами
    await message.answer("Выберите действие:", reply_markup=usd_signal_keyboard)


@dp.message_handler(Text(equals="Текущий сигнал в % по USD"))
async def current_signal_usd(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        with open("usd_signal.txt", "r") as file:
            signal = file.read()
            if not signal:
                await message.answer("Текущий сигнал по USD не установлен", reply_markup=usd_signal_keyboard)
            else:
                await message.answer(f"Текущий сигнал в % от точки входа по USD: {signal}", reply_markup=usd_signal_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал не найден", reply_markup=usd_signal_keyboard)

@dp.message_handler(Text(equals="Новый сигнал в % по USD"))
async def new_signal_usd(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите новое значение сигнала в % от точки входа по USD:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_usd.set()

@dp.message_handler(state=YourState.new_usd)
async def process_new_signal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text
        # Проверка, является ли введенное значение числом
        try:
            new_signal = float(data['new_signal'])
            # Сохраняем новый сигнал в файл
            with open("usd_signal.txt", "w") as file:
                file.write(data['new_signal'])
            await message.answer(f"{checkmark}Новый сигнал в % от точки входа по USD установлен: {data['new_signal']}",
                                 reply_markup=signal_keyboard)
        except ValueError:
            # Если введенное значение не является числом, открываем клавиатуру
            await message.answer("Введите число")
            return  # Выходим из обработчика



    # Завершаем состояние FSMContext
    await state.finish()


@dp.message_handler(Text(equals="Запись новой точки входа USD"))
async def new_signal_usd(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите значение точки входа по USD:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_usd_tvh.set()

@dp.message_handler(state=YourState.new_usd_tvh)
async def process_new_signal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text

        # Сохраняем новый сигнал в файл
        with open("usd_tvh.txt", "w") as file:
            file.write(data['new_signal'])
        await message.answer(f"{checkmark}Новая точка входа по USD: {data['new_signal']}",
                             reply_markup=usd_fiks_keyboard)

    # Завершаем состояние FSMContext
    await state.finish()





@dp.message_handler(Text(equals="Сброс сигнала в % по USD"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Сбросить сигнал по USD?'
    await bot.send_message(message.chat.id, mess, reply_markup=usd_signal_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить сигнал USD"))
async def reset_usd_tvh(message: types.Message):
    usd_tvh_file = 'usd_signal.txt'

    if os.path.exists(usd_tvh_file):
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Сигнал для USD сброшен.", reply_markup=usd_signal_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала.", reply_markup=usd_signal_keyboard)

@dp.message_handler(Text(equals="Сброс ТВХ USD"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Сбросить точку входа по USD?'
    await bot.send_message(message.chat.id, mess, reply_markup=usd_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить точку входа USD"))
async def reset_usd_tvh(message: types.Message):
    usd_tvh_file = 'usd_tvh.txt'

    if os.path.exists(usd_tvh_file):
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Точка входа для USD сброшена.", reply_markup=usd_fiks_keyboard)
    else:
        await message.answer("Нет сохранённой точки входа.", reply_markup=usd_fiks_keyboard)





@dp.message_handler(Text(equals="USD. %"))
async def with_puree(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами
    await message.answer("Выберите действие:", reply_markup=usd_signal_only_keyboard)


@dp.message_handler(Text(equals="Текущий сигнал в % по USD."))
async def current_signal_usd(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        with open("usd_signal_only.txt", "r") as file:
            signal = file.read()
            if not signal:
                await message.answer("Текущий сигнал по USD не установлен", reply_markup=usd_signal_only_keyboard)
            else:
                await message.answer(f"Текущий сигнал в % по USD: {signal}", reply_markup=usd_signal_only_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал не найден", reply_markup=usd_signal_only_keyboard)

@dp.message_handler(Text(equals="Новый сигнал в % по USD."))
async def new_signal_usd(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите новое значение сигнала в % по USD:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_usd_only.set()

@dp.message_handler(state=YourState.new_usd_only)
async def process_new_signal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text
        # Проверка, является ли введенное значение числом
        try:
            new_signal = float(data['new_signal'])
        except ValueError:
            # Если введенное значение не является числом, открываем клавиатуру
            await message.answer("Введите число")
            return  # Выходим из обработчика

        # Сохраняем новый сигнал в файл
        with open("usd_signal_only.txt", "w") as file:
            file.write(data['new_signal'])
        await message.answer(f"{checkmark}Новый сигнал в % по USD установлен: {data['new_signal']}",
                             reply_markup=signal_only_keyboard)

    # Завершаем состояние FSMContext
    await state.finish()
    with open('usd.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    x = None
    for line in lines:
        if "Спред Si - USDRUBF:" in line:
            parts = line.split()
            x_index = parts.index('Спред') + 4
            x = parts[x_index]
    with open("usd_spread_only.txt", "w") as file:
        pass
        file.write(x)

@dp.message_handler(Text(equals="Сброс сигнала в % по USD."))
async def fix_usd_tvh(message: types.Message):
    mess = 'Сбросить сигнал по USD?'
    await bot.send_message(message.chat.id, mess, reply_markup=usd_signal_only_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить сигнал USD."))
async def reset_usd_tvh(message: types.Message):
    usd_tvh_file = 'usd_signal_only.txt'

    if os.path.exists(usd_tvh_file):
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Сигнал для USD сброшен.", reply_markup=usd_signal_only_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала.", reply_markup=usd_signal_only_keyboard)








@dp.message_handler(Text(equals="USD, п"))
async def with_puree(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами
    await message.answer("Выберите действие:", reply_markup=usd_signal_firstspread_keyboard)


@dp.message_handler(Text(equals="Текущий сигнал по USD, п"))
async def current_signal_usd(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        usd_tvh_file = 'usd_firstspread_and_signal.txt'

        if os.path.exists(usd_tvh_file):
            with open(usd_tvh_file, "r") as file:
                data = file.read().strip()  # Убираем лишние пробелы и переводы строк

            if not data:
                await message.answer("Текущий сигнал по USD не установлен", reply_markup=usd_signal_firstspread_keyboard)
            else:
                values = data.split(', ')
                signal = values[-1]
                if not signal:
                    await message.answer("Текущий сигнал по USD не установлен", reply_markup=usd_signal_firstspread_keyboard)
                else:
                    await message.answer(f"Текущий сигнал по USD: {signal}", reply_markup=usd_signal_firstspread_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал не найден", reply_markup=usd_signal_firstspread_keyboard)


@dp.message_handler(Text(equals="Новый сигнал по USD, п"))
async def new_signal_usd(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите новое значение сигнала по USD:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_usd_spread_first.set()

@dp.message_handler(state=YourState.new_usd_spread_first)
async def process_new_signal(message: types.Message, state: FSMContext):
    usd_tvh_file = 'usd_tvh.txt'

    if os.path.exists(usd_tvh_file):
        # Проверьте, является ли файл пустым
        is_empty = not bool(open(usd_tvh_file, 'r', encoding='utf-8').read())

        if is_empty:
            with open(usd_tvh_file, 'a', encoding='utf-8') as fw:
                with open('usd.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                x = None
                for line in lines:
                    if "Спред Si - USDRUBF:" in line:
                        parts = line.split()
                        x_index = parts.index('Спред') + 4
                        x = parts[x_index]
                        break


    async with state.proxy() as data:
        data['new_signal'] = message.text

        # Проверка, является ли введенное значение числом
        try:
            new_signal = float(data['new_signal'])
        except ValueError:
            # Если введенное значение не является числом, открываем клавиатуру
            await message.answer("Введите число")
            return  # Выходим из обработчика

        # Сохраняем новый сигнал в файл
        with open("usd_firstspread_and_signal.txt", "w") as file:
            file.write(f"{x}, {data['new_signal']}")
        await message.answer(f"{checkmark}Новый сигнал по USD установлен: {data['new_signal']}",
                             reply_markup=signal_firstspread_keyboard)

    # Завершаем состояние FSMContext
    await state.finish()


@dp.message_handler(Text(equals="Сброс сигнала по USD, п"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Сбросить сигнал по USD?'
    await bot.send_message(message.chat.id, mess, reply_markup=usd_signal_firstspread_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить сигнал USD, п"))
async def reset_usd_tvh(message: types.Message):
    usd_tvh_file = 'usd_firstspread_and_signal.txt'

    if os.path.exists(usd_tvh_file):
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Сигнал для USD сброшен.", reply_markup=signal_firstspread_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала.", reply_markup=signal_firstspread_keyboard)




#_____________________________________________________________________________________________________________________________________

@dp.message_handler(Text(equals="EUR"))
async def action1(message: types.Message):
    # Здесь вы можете выполнять необходимые действия для "Действие 1"
    with open('eur.txt', 'r', encoding='utf-8') as fr:
        mess = fr.read()  # Corrected to call the read() method
        await bot.send_message(message.chat.id, mess, reply_markup=eur_fiks_keyboard)

@dp.message_handler(Text(equals="Текущая ТВХ EUR"))
async def current_signal_usd(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        with open("eur_tvh.txt", "r") as file:
            tvh = file.read()
            if not tvh:
                await message.answer("Точка входа по EUR не установлена", reply_markup=eur_fiks_keyboard)
            else:
                await message.answer(f"Точка входа по EUR: {tvh}", reply_markup=eur_fiks_keyboard)
    except FileNotFoundError:
        await message.answer("Точка входа не найдена", reply_markup=eur_fiks_keyboard)

@dp.message_handler(Text(equals="Новая ТВХ EUR"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Зафиксировать новую точку входа EUR по спреду или вручную?'
    await bot.send_message(message.chat.id, mess, reply_markup=eur_yes_no_keyboard)

@dp.message_handler(Text(equals="Новая точка входа EUR по спреду"))
async def fix_usd_tvh(message: types.Message):
    usd_tvh_file = 'eur_tvh.txt'

    if os.path.exists(usd_tvh_file):
        # Проверьте, является ли файл пустым
        is_empty = not bool(open(usd_tvh_file, 'r', encoding='utf-8').read())

        if is_empty:
            with open(usd_tvh_file, 'a', encoding='utf-8') as fw:
                with open('eur.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                x = None
                for line in lines:
                    if "Спред Eu - EURRUBF:" in line:
                        parts = line.split()
                        x_index = parts.index('Спред') + 4
                        x = parts[x_index]
                        break

                if x is not None:
                    data_to_write = x
                    fw.write(data_to_write)
                    await message.answer(f"{checkmark}Точка входа {x} для USD зафиксирована.", reply_markup=eur_fiks_keyboard)
                else:
                    await message.answer("Не удалось найти точку входа для EUR.", reply_markup=eur_fiks_keyboard)
        else:
            await message.answer("Есть зафиксированная точка входа. Для записи новой точки сбросьте старую.", reply_markup=eur_fiks_keyboard)
    else:
        # Файл не существует, создайте его и записывайте информацию
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            with open('eur.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            x = None
            for line in lines:
                if "Спред Eu - EURRUBF:" in line:
                    parts = line.split()
                    x_index = parts.index('Спред') + 4
                    x = parts[x_index]
                    break

            if x is not None:
                data_to_write = x
                fw.write(data_to_write)
                await message.answer(f"{checkmark}Точка входа {x} для EUR зафиксирована.", reply_markup=eur_fiks_keyboard)
            else:
                await message.answer("Не удалось найти точку входа для USD.", reply_markup=eur_fiks_keyboard)

@dp.message_handler(Text(equals="EUR, %"))
async def with_eur_signal(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами по EUR
    await message.answer("Выберите действие для EUR:", reply_markup=eur_signal_keyboard)

@dp.message_handler(Text(equals="Текущий сигнал в % по EUR"))
async def current_signal_eur(message: types.Message):
    try:
        with open("eur_signal.txt", "r") as file:
            signal = file.read()
            if not signal:
                await message.answer("Текущий сигнал по EUR не установлен", reply_markup=eur_signal_keyboard)
            else:
                await message.answer(f"Текущий сигнал в % от точки входа по EUR: {signal}", reply_markup=eur_signal_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал по EUR не найден", reply_markup=eur_signal_keyboard)

@dp.message_handler(Text(equals="Новый сигнал в % по EUR"))
async def new_signal_eur(message: types.Message, state: FSMContext):
    await message.answer("Введите новое значение сигнала в % от точки входа по EUR:")
    await YourState.new_eur.set()

@dp.message_handler(state=YourState.new_eur)
async def process_new_signal_eur(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text
        # Проверка, является ли введенное значение числом
        try:
            new_signal = float(data['new_signal'])
        except ValueError:
            # Если введенное значение не является числом, открываем клавиатуру
            await message.answer("Введите число")
            return  # Выходим из обработчика

        with open("eur_signal.txt", "w") as file:
            file.write(data['new_signal'])
        await message.answer(f"{checkmark}Новый сигнал в % от точки входа по EUR установлен: {data['new_signal']}", reply_markup=signal_keyboard)

    await state.finish()

@dp.message_handler(Text(equals="Запись новой точки входа EUR"))
async def new_signal_usd(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите значение точки входа по EUR:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_eur_tvh.set()

@dp.message_handler(state=YourState.new_eur_tvh)
async def process_new_signal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text


        # Сохраняем новый сигнал в файл
        with open("eur_tvh.txt", "w") as file:
            file.write(data['new_signal'])
        await message.answer(f"{checkmark}Новая точка входа по EUR: {data['new_signal']}",
                             reply_markup=eur_fiks_keyboard)

    # Завершаем состояние FSMContext
    await state.finish()

@dp.message_handler(Text(equals="Сброс сигнала в % по EUR"))
async def fix_eur_signal(message: types.Message):
    mess = 'Сбросить сигнал по EUR?'
    await bot.send_message(message.chat.id, mess, reply_markup=eur_signal_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить сигнал EUR"))
async def reset_eur_signal(message: types.Message):
    eur_signal_file = 'eur_signal.txt'

    if os.path.exists(eur_signal_file):
        with open(eur_signal_file, 'w', encoding='utf-8') as fw:
            pass
        await message.answer("Сигнал для EUR сброшен.", reply_markup=eur_signal_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала для EUR.", reply_markup=eur_signal_keyboard)

@dp.message_handler(Text(equals="Сброс ТВХ EUR"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Сбросить точку входа по EUR?'
    await bot.send_message(message.chat.id, mess, reply_markup=eur_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить точку входа EUR"))
async def reset_usd_tvh(message: types.Message):
    usd_tvh_file = 'eur_tvh.txt'

    if os.path.exists(usd_tvh_file):
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Точка входа для EUR сброшена.", reply_markup=eur_fiks_keyboard)
    else:
        await message.answer("Нет сохранённой точки входа.", reply_markup=eur_fiks_keyboard)

@dp.message_handler(Text(equals="EUR. %"))
async def with_puree(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами
    await message.answer("Выберите действие:", reply_markup=eur_signal_only_keyboard)


@dp.message_handler(Text(equals="Текущий сигнал в % по EUR."))
async def current_signal_usd(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        with open("eur_signal_only.txt", "r") as file:
            signal = file.read()
            if not signal:
                await message.answer("Текущий сигнал по EUR не установлен", reply_markup=eur_signal_only_keyboard)
            else:
                await message.answer(f"Текущий сигнал в % по EUR: {signal}", reply_markup=eur_signal_only_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал не найден", reply_markup=eur_signal_only_keyboard)

@dp.message_handler(Text(equals="Новый сигнал в % по EUR."))
async def new_signal_usd(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите новое значение сигнала в % по EUR:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_eur_only.set()

@dp.message_handler(state=YourState.new_eur_only)
async def process_new_signal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text
        # Проверка, является ли введенное значение числом
        try:
            new_signal = float(data['new_signal'])
        except ValueError:
            # Если введенное значение не является числом, открываем клавиатуру
            await message.answer("Введите число")
            return  # Выходим из обработчика

        # Сохраняем новый сигнал в файл
        with open("eur_signal_only.txt", "w") as file:
            file.write(data['new_signal'])
        await message.answer(f"{checkmark}Новый сигнал в % по EUR установлен: {data['new_signal']}",
                             reply_markup=signal_only_keyboard)

    # Завершаем состояние FSMContext
    await state.finish()
    with open('eur.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    x = None
    for line in lines:
        if "Спред Eu - EURRUBF:" in line:
            parts = line.split()
            x_index = parts.index('Спред') + 4
            x = parts[x_index]
    with open("eur_spread_only.txt", "w") as file:
        pass
        file.write(x)

@dp.message_handler(Text(equals="Сброс сигнала в % по EUR."))
async def fix_usd_tvh(message: types.Message):
    mess = 'Сбросить сигнал по EUR?'
    await bot.send_message(message.chat.id, mess, reply_markup=eur_signal_only_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить сигнал EUR."))
async def reset_usd_tvh(message: types.Message):
    usd_tvh_file = 'eur_signal_only.txt'

    if os.path.exists(usd_tvh_file):
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Сигнал для EUR сброшен.", reply_markup=eur_signal_only_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала.", reply_markup=eur_signal_only_keyboard)


@dp.message_handler(Text(equals="EUR, п"))
async def with_puree(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами
    await message.answer("Выберите действие:", reply_markup=eur_signal_firstspread_keyboard)


@dp.message_handler(Text(equals="Текущий сигнал по EUR, п"))
async def current_signal_usd(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        usd_tvh_file = 'eur_firstspread_and_signal.txt'

        if os.path.exists(usd_tvh_file):
            with open(usd_tvh_file, "r") as file:
                data = file.read().strip()  # Убираем лишние пробелы и переводы строк

            if not data:
                await message.answer("Текущий сигнал по EUR не установлен", reply_markup=eur_signal_firstspread_keyboard)
            else:
                values = data.split(', ')
                signal = values[-1]
                if not signal:
                    await message.answer("Текущий сигнал по EUR не установлен", reply_markup=eur_signal_firstspread_keyboard)
                else:
                    await message.answer(f"Текущий сигнал по EUR: {signal}", reply_markup=eur_signal_firstspread_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал не найден", reply_markup=eur_signal_firstspread_keyboard)


@dp.message_handler(Text(equals="Новый сигнал по EUR, п"))
async def new_signal_usd(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите новое значение сигнала по EUR:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_eur_spread_first.set()

@dp.message_handler(state=YourState.new_eur_spread_first)
async def process_new_signal(message: types.Message, state: FSMContext):
    usd_tvh_file = 'eur_tvh.txt'

    if os.path.exists(usd_tvh_file):
        # Проверьте, является ли файл пустым
        is_empty = not bool(open(usd_tvh_file, 'r', encoding='utf-8').read())

        if is_empty:
            with open(usd_tvh_file, 'a', encoding='utf-8') as fw:
                with open('eur.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                x = None
                for line in lines:
                    if "Спред Eu - EURRUBF:" in line:
                        parts = line.split()
                        x_index = parts.index('Спред') + 4
                        x = parts[x_index]
                        break


    async with state.proxy() as data:
        data['new_signal'] = message.text

        # Проверка, является ли введенное значение числом
        try:
            new_signal = float(data['new_signal'])
        except ValueError:
            # Если введенное значение не является числом, открываем клавиатуру
            await message.answer("Введите число")
            return  # Выходим из обработчика

        # Сохраняем новый сигнал в файл
        with open("eur_firstspread_and_signal.txt", "w") as file:
            file.write(f"{x}, {data['new_signal']}")
        await message.answer(f"{checkmark}Новый сигнал по EUR установлен: {data['new_signal']}",
                             reply_markup=signal_firstspread_keyboard)

    # Завершаем состояние FSMContext
    await state.finish()


@dp.message_handler(Text(equals="Сброс сигнала по EUR, п"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Сбросить сигнал по EUR?'
    await bot.send_message(message.chat.id, mess, reply_markup=eur_signal_firstspread_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить сигнал EUR, п"))
async def reset_usd_tvh(message: types.Message):
    usd_tvh_file = 'eur_firstspread_and_signal.txt'

    if os.path.exists(usd_tvh_file):
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Сигнал для EUR сброшен.", reply_markup=signal_firstspread_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала.", reply_markup=signal_firstspread_keyboard)


#_____________________________________________________________________________________________________________________________________

@dp.message_handler(Text(equals="CNY"))
async def action1(message: types.Message):
    # Здесь вы можете выполнять необходимые действия для "Действие 1"
    with open('cny.txt', 'r', encoding='utf-8') as fr:
        mess = fr.read()  # Corrected to call the read() method
        await bot.send_message(message.chat.id, mess, reply_markup=cny_fiks_keyboard)

@dp.message_handler(Text(equals="Текущая ТВХ CNY"))
async def current_signal_usd(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        with open("cny_tvh.txt", "r") as file:
            tvh = file.read()
            if not tvh:
                await message.answer("Точка входа по CNY не установлена", reply_markup=cny_fiks_keyboard)
            else:
                await message.answer(f"Точка входа по CNY: {tvh}", reply_markup=cny_fiks_keyboard)
    except FileNotFoundError:
        await message.answer("Точка входа не найдена", reply_markup=cny_fiks_keyboard)

@dp.message_handler(Text(equals="Новая ТВХ CNY"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Зафиксировать новую точку входа CNY по спреду или вручную?'
    await bot.send_message(message.chat.id, mess, reply_markup=cny_yes_no_keyboard)

@dp.message_handler(Text(equals="Новая точка входа CNY по спреду"))
async def fix_usd_tvh(message: types.Message):
    usd_tvh_file = 'cny_tvh.txt'

    if os.path.exists(usd_tvh_file):
        # Проверьте, является ли файл пустым
        is_empty = not bool(open(usd_tvh_file, 'r', encoding='utf-8').read())

        if is_empty:
            with open(usd_tvh_file, 'a', encoding='utf-8') as fw:
                with open('cny.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                x = None
                for line in lines:
                    if "Спред Cny - CNYRUBF:" in line:
                        parts = line.split()
                        x_index = parts.index('Спред') + 4
                        x = parts[x_index]
                        break

                if x is not None:
                    data_to_write = x
                    fw.write(data_to_write)
                    await message.answer(f"{checkmark}Точка входа {x} для CNY зафиксирована.", reply_markup=cny_fiks_keyboard)
                else:
                    await message.answer("Не удалось найти точку входа для CNY.", reply_markup=cny_fiks_keyboard)
        else:
            await message.answer("Есть зафиксированная точка входа. Для записи новой точки сбросьте старую.", reply_markup=cny_fiks_keyboard)
    else:
        # Файл не существует, создайте его и записывайте информацию
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            with open('cny.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            x = None
            for line in lines:
                if "Спред Cny - CNYRUBF:" in line:
                    parts = line.split()
                    x_index = parts.index('Спред') + 4
                    x = parts[x_index]
                    break

            if x is not None:
                data_to_write = x
                fw.write(data_to_write)
                await message.answer(f"{checkmark}Точка входа {x} для CNY зафиксирована.", reply_markup=cny_fiks_keyboard)
            else:
                await message.answer("Не удалось найти точку входа для CNY.", reply_markup=cny_fiks_keyboard)

@dp.message_handler(Text(equals="CNY, %"))
async def with_eur_signal(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами по EUR
    await message.answer("Выберите действие для CNY:", reply_markup=cny_signal_keyboard)

@dp.message_handler(Text(equals="Текущий сигнал в % по CNY"))
async def current_signal_eur(message: types.Message):
    try:
        with open("cny_signal.txt", "r") as file:
            signal = file.read()
            if not signal:
                await message.answer("Текущий сигнал от точки входа по CNY не установлен", reply_markup=cny_signal_keyboard)
            else:
                await message.answer(f"Текущий сигнал в % от точки входа по CNY: {signal}", reply_markup=cny_signal_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал по CNY не найден", reply_markup=cny_signal_keyboard)

@dp.message_handler(Text(equals="Новый сигнал в % по CNY"))
async def new_signal_eur(message: types.Message, state: FSMContext):
    await message.answer("Введите новое значение сигнала в % от точки входа по CNY:")
    await YourState.new_cny.set()

@dp.message_handler(state=YourState.new_cny)
async def process_new_signal_eur(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text
        # Проверка, является ли введенное значение числом
        try:
            new_signal = float(data['new_signal'])
        except ValueError:
            # Если введенное значение не является числом, открываем клавиатуру
            await message.answer("Введите число")
            return  # Выходим из обработчика

        with open("cny_signal.txt", "w") as file:
            file.write(data['new_signal'])
        await message.answer(f"{checkmark}Новый сигнал в % от точки входа по CNY установлен: {data['new_signal']}", reply_markup=signal_keyboard)

    await state.finish()

@dp.message_handler(Text(equals="Запись новой точки входа CNY"))
async def new_signal_usd(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите значение точки входа по CNY:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_cny_tvh.set()

@dp.message_handler(state=YourState.new_cny_tvh)
async def process_new_signal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text

        # Сохраняем новый сигнал в файл
        with open("cny_tvh.txt", "w") as file:
            file.write(data['new_signal'])
        await message.answer(f"{checkmark}Новая точка входа по CNY: {data['new_signal']}",
                             reply_markup=cny_fiks_keyboard)

    # Завершаем состояние FSMContext
    await state.finish()
@dp.message_handler(Text(equals="Сброс сигнала в % по CNY"))
async def fix_eur_signal(message: types.Message):
    mess = 'Сбросить сигнал по CNY?'
    await bot.send_message(message.chat.id, mess, reply_markup=cny_signal_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить сигнал CNY"))
async def reset_eur_signal(message: types.Message):
    cny_signal_file = 'cny_signal.txt'

    if os.path.exists(cny_signal_file):
        with open(cny_signal_file, 'w', encoding='utf-8') as fw:
            pass
        await message.answer("Сигнал для CNY сброшен.", reply_markup=cny_signal_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала для CNY.", reply_markup=cny_signal_keyboard)

@dp.message_handler(Text(equals="Сброс ТВХ CNY"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Сбросить точку входа по CNY?'
    await bot.send_message(message.chat.id, mess, reply_markup=cny_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить точку входа CNY"))
async def reset_usd_tvh(message: types.Message):
    usd_tvh_file = 'cny_tvh.txt'

    if os.path.exists(usd_tvh_file):
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Точка входа для CNY сброшена.", reply_markup=cny_fiks_keyboard)
    else:
        await message.answer("Нет сохранённой точки входа.", reply_markup=cny_fiks_keyboard)


@dp.message_handler(Text(equals="CNY. %"))
async def with_puree(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами
    await message.answer("Выберите действие:", reply_markup=cny_signal_only_keyboard)


@dp.message_handler(Text(equals="Текущий сигнал в % по CNY."))
async def current_signal_usd(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        with open("cny_signal_only.txt", "r") as file:
            signal = file.read()
            if not signal:
                await message.answer("Текущий сигнал по CNY не установлен", reply_markup=cny_signal_only_keyboard)
            else:
                await message.answer(f"Текущий сигнал в % по CNY: {signal}", reply_markup=cny_signal_only_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал не найден", reply_markup=cny_signal_only_keyboard)

@dp.message_handler(Text(equals="Новый сигнал в % по CNY."))
async def new_signal_usd(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите новое значение сигнала в % по CNY:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_cny_only.set()

@dp.message_handler(state=YourState.new_cny_only)
async def process_new_signal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text
        # Проверка, является ли введенное значение числом
        try:
            new_signal = float(data['new_signal'])
        except ValueError:
            # Если введенное значение не является числом, открываем клавиатуру
            await message.answer("Введите число",
                                 reply_markup=cny_signal_only_keyboard)
            return  # Выходим из обработчика

        # Сохраняем новый сигнал в файл
        with open("cny_signal_only.txt", "w") as file:
            file.write(data['new_signal'])
        await message.answer(f"{checkmark}Новый сигнал в % по CNY установлен: {data['new_signal']}",
                             reply_markup=signal_only_keyboard)

    # Завершаем состояние FSMContext
    await state.finish()
    with open('cny.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    x = None
    for line in lines:
        if "Спред Cny - CNYRUBF:" in line:
            parts = line.split()
            x_index = parts.index('Спред') + 4
            x = parts[x_index]
    with open("cny_spread_only.txt", "w") as file:
        pass
        file.write(x)

@dp.message_handler(Text(equals="Сброс сигнала в % по CNY."))
async def fix_usd_tvh(message: types.Message):
    mess = 'Сбросить сигнал по CNY?'
    await bot.send_message(message.chat.id, mess, reply_markup=cny_signal_only_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить сигнал CNY."))
async def reset_usd_tvh(message: types.Message):
    usd_tvh_file = 'cny_signal_only.txt'

    if os.path.exists(usd_tvh_file):
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Сигнал для CNY сброшен.", reply_markup=cny_signal_only_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала.", reply_markup=cny_signal_only_keyboard)





@dp.message_handler(Text(equals="CNY, п"))
async def with_puree(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами
    await message.answer("Выберите действие:", reply_markup=cny_signal_firstspread_keyboard)


@dp.message_handler(Text(equals="Текущий сигнал по CNY, п"))
async def current_signal_usd(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        usd_tvh_file = 'cny_firstspread_and_signal.txt'

        if os.path.exists(usd_tvh_file):
            with open(usd_tvh_file, "r") as file:
                data = file.read().strip()  # Убираем лишние пробелы и переводы строк

            if not data:
                await message.answer("Текущий сигнал по CNY не установлен", reply_markup=cny_signal_firstspread_keyboard)
            else:
                values = data.split(', ')
                signal = values[-1]
                if not signal:
                    await message.answer("Текущий сигнал по CNY не установлен", reply_markup=cny_signal_firstspread_keyboard)
                else:
                    await message.answer(f"Текущий сигнал по CNY: {signal}", reply_markup=cny_signal_firstspread_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал не найден", reply_markup=cny_signal_firstspread_keyboard)


@dp.message_handler(Text(equals="Новый сигнал по CNY, п"))
async def new_signal_usd(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите новое значение сигнала по CNY:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_cny_spread_first.set()

@dp.message_handler(state=YourState.new_cny_spread_first)
async def process_new_signal(message: types.Message, state: FSMContext):
    usd_tvh_file = 'cny_tvh.txt'
    if os.path.exists(usd_tvh_file):
        # Проверьте, является ли файл пустым
        is_empty = not bool(open(usd_tvh_file, 'r', encoding='utf-8').read())

    if is_empty:
        with open(usd_tvh_file, 'a', encoding='utf-8') as fw:
            with open('cny.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for line in lines:
                if "Спред Cny - CNYRUBF:" in line:
                    parts = line.split()
                    x_index = parts.index('Спред') + 4
                    x = parts[x_index]
                    break


        async with state.proxy() as data:
            data['new_signal'] = message.text

            # Проверка, является ли введенное значение числом с использованием регулярного выражения
            if re.match(r'^-?\d+(\.\d+)?$', data['new_signal']):
                # Если введенное значение является числом, обрабатываем его
                new_signal = float(data['new_signal'])


                # Сохраняем новый сигнал в файл
                with open("cny_firstspread_and_signal.txt", "w") as file:
                    file.write(f"{x}, {new_signal}")
                await message.answer(f"{checkmark}Новый сигнал по CNY установлен: {data['new_signal']}",
                                     reply_markup=signal_firstspread_keyboard)

        # Завершаем состояние FSMContext
        await state.finish()
    else:

        await message.answer("Есть зафиксированный сигнал. Для записи нового сигнала сбросьте старый.", reply_markup=cny_signal_firstspread_keyboard)


@dp.message_handler(Text(equals="Сброс сигнала по CNY, п"))
async def fix_usd_tvh(message: types.Message):
    mess = 'Сбросить сигнал по CNY?'
    await bot.send_message(message.chat.id, mess, reply_markup=cny_signal_firstspread_sbros_keyboard)

@dp.message_handler(Text(equals="Сбросить сигнал CNY, п"))
async def reset_usd_tvh(message: types.Message):
    usd_tvh_file = 'cny_firstspread_and_signal.txt'

    if os.path.exists(usd_tvh_file):
        with open(usd_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Сигнал для CNY сброшен.", reply_markup=signal_firstspread_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала.", reply_markup=signal_firstspread_keyboard)




#_____________________________________________________________________________________________________________________________________


@dp.message_handler(Text(equals="MGNT"))
async def action1(message: types.Message):
    # Здесь вы можете выполнять необходимые действия для "Действие 1"

    with open('mgnt.txt', 'r', encoding='utf-8') as fr:
        mess = fr.read()  # Corrected to call the read() method
        await bot.send_message(message.chat.id, mess, reply_markup=mgnt_fiks_keyboard)


@dp.message_handler(Text(equals="Текущая ТВХ MGNT"))
async def current_signal_mgnt(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        with open("mgnt_tvh.txt", "r") as file:
            tvh = file.read()
            if not tvh:
                await message.answer("Точка входа по MGNT не установлена", reply_markup=mgnt_fiks_keyboard)
            else:
                await message.answer(f"Точка входа по MGNT: {tvh}", reply_markup=mgnt_fiks_keyboard)
    except FileNotFoundError:
        await message.answer("Точка входа не найдена", reply_markup=mgnt_fiks_keyboard)


@dp.message_handler(Text(equals="Новая ТВХ MGNT"))
async def fix_mgnt_tvh(message: types.Message):
    mess = 'Зафиксировать новую точку входа MGNT по спреду или вручную?'
    await bot.send_message(message.chat.id, mess, reply_markup=mgnt_yes_no_keyboard)


@dp.message_handler(Text(equals="Новая точка входа MGNT по спреду"))
async def fix_mgnt_tvh(message: types.Message):
    mgnt_tvh_file = 'mgnt_tvh.txt'

    if os.path.exists(mgnt_tvh_file):
        # Проверьте, является ли файл пустым
        is_empty = not bool(open(mgnt_tvh_file, 'r', encoding='utf-8').read())

        if is_empty:
            with open(mgnt_tvh_file, 'a', encoding='utf-8') as fw:
                with open('mgnt.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                x = None
                for line in lines:
                    if "Спред MGNT - MGNT-12.23:" in line:
                        parts = line.split()
                        x_index = parts.index('Спред') + 4
                        x = parts[x_index]
                        break

                if x is not None:
                    data_to_write = x
                    fw.write(data_to_write)
                    await message.answer(f"{checkmark}Точка входа {x} для MGNT зафиксирована.",
                                         reply_markup=mgnt_fiks_keyboard)
                else:
                    await message.answer("Не удалось найти точку входа для MGNT.", reply_markup=mgnt_fiks_keyboard)
        else:
            await message.answer("Есть зафиксированная точка входа. Для записи новой точки сбросьте старую.",
                                 reply_markup=mgnt_fiks_keyboard)
    else:
        # Файл не существует, создайте его и записывайте информацию
        with open(mgnt_tvh_file, 'w', encoding='utf-8') as fw:
            with open('mgnt.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            x = None
            for line in lines:
                if "Спред MGNT - MGNT-12.23:" in line:
                    parts = line.split()
                    x_index = parts.index('Спред') + 4
                    x = parts[x_index]
                    break

            if x is not None:
                data_to_write = x
                fw.write(data_to_write)
                await message.answer(f"{checkmark}Точка входа {x} для MGNT зафиксирована.",
                                     reply_markup=mgnt_fiks_keyboard)
            else:
                await message.answer("Не удалось найти точку входа для MGNT.", reply_markup=mgnt_fiks_keyboard)


@dp.message_handler(Text(equals="MGNT, %"))
async def with_puree(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами
    await message.answer("Выберите действие:", reply_markup=mgnt_signal_keyboard)


@dp.message_handler(Text(equals="Текущий сигнал в % по MGNT"))
async def current_signal_mgnt(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        with open("mgnt_signal.txt", "r") as file:
            signal = file.read()
            if not signal:
                await message.answer("Текущий сигнал по MGNT не установлен", reply_markup=mgnt_signal_keyboard)
            else:
                await message.answer(f"Текущий сигнал в % от точки входа по MGNT: {signal}",
                                     reply_markup=mgnt_signal_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал не найден", reply_markup=mgnt_signal_keyboard)


@dp.message_handler(Text(equals="Новый сигнал в % по MGNT"))
async def new_signal_mgnt(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите новое значение сигнала в % от точки входа по MGNT:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_mgnt.set()


@dp.message_handler(state=YourState.new_mgnt)
async def process_new_signal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text
        # Проверка, является ли введенное значение числом
        try:
            new_signal = float(data['new_signal'])
            # Сохраняем новый сигнал в файл
            with open("mgnt_signal.txt", "w") as file:
                file.write(data['new_signal'])
            await message.answer(f"{checkmark}Новый сигнал в % от точки входа по MGNT установлен: {data['new_signal']}",
                                 reply_markup=signal_keyboard)
        except ValueError:
            # Если введенное значение не является числом, открываем клавиатуру
            await message.answer("Введите число")
            return  # Выходим из обработчика

    # Завершаем состояние FSMContext
    await state.finish()


@dp.message_handler(Text(equals="Запись новой точки входа MGNT"))
async def new_signal_mgnt(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите значение точки входа по MGNT:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_mgnt_tvh.set()


@dp.message_handler(state=YourState.new_mgnt_tvh)
async def process_new_signal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text

        # Сохраняем новый сигнал в файл
        with open("mgnt_tvh.txt", "w") as file:
            file.write(data['new_signal'])
        await message.answer(f"{checkmark}Новая точка входа по MGNT: {data['new_signal']}",
                             reply_markup=mgnt_fiks_keyboard)

    # Завершаем состояние FSMContext
    await state.finish()


@dp.message_handler(Text(equals="Сброс сигнала в % по MGNT"))
async def fix_mgnt_tvh(message: types.Message):
    mess = 'Сбросить сигнал по MGNT?'
    await bot.send_message(message.chat.id, mess, reply_markup=mgnt_signal_sbros_keyboard)


@dp.message_handler(Text(equals="Сбросить сигнал MGNT"))
async def reset_mgnt_tvh(message: types.Message):
    mgnt_tvh_file = 'mgnt_signal.txt'

    if os.path.exists(mgnt_tvh_file):
        with open(mgnt_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Сигнал для MGNT сброшен.", reply_markup=mgnt_signal_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала.", reply_markup=mgnt_signal_keyboard)


@dp.message_handler(Text(equals="Сброс ТВХ MGNT"))
async def fix_mgnt_tvh(message: types.Message):
    mess = 'Сбросить точку входа по MGNT?'
    await bot.send_message(message.chat.id, mess, reply_markup=mgnt_sbros_keyboard)


@dp.message_handler(Text(equals="Сбросить точку входа MGNT"))
async def reset_mgnt_tvh(message: types.Message):
    mgnt_tvh_file = 'mgnt_tvh.txt'

    if os.path.exists(mgnt_tvh_file):
        with open(mgnt_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Точка входа для MGNT сброшена.", reply_markup=mgnt_fiks_keyboard)
    else:
        await message.answer("Нет сохранённой точки входа.", reply_markup=mgnt_fiks_keyboard)


@dp.message_handler(Text(equals="MGNT. %"))
async def with_puree(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами
    await message.answer("Выберите действие:", reply_markup=mgnt_signal_only_keyboard)


@dp.message_handler(Text(equals="Текущий сигнал в % по MGNT."))
async def current_signal_mgnt(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        with open("mgnt_signal_only.txt", "r") as file:
            signal = file.read()
            if not signal:
                await message.answer("Текущий сигнал по MGNT не установлен", reply_markup=mgnt_signal_only_keyboard)
            else:
                await message.answer(f"Текущий сигнал в % по MGNT: {signal}", reply_markup=mgnt_signal_only_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал не найден", reply_markup=mgnt_signal_only_keyboard)


@dp.message_handler(Text(equals="Новый сигнал в % по MGNT."))
async def new_signal_mgnt(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите новое значение сигнала в % по MGNT:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_mgnt_only.set()


@dp.message_handler(state=YourState.new_mgnt_only)
async def process_new_signal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_signal'] = message.text
        # Проверка, является ли введенное значение числом
        try:
            new_signal = float(data['new_signal'])
        except ValueError:
            # Если введенное значение не является числом, открываем клавиатуру
            await message.answer("Введите число")
            return  # Выходим из обработчика

        # Сохраняем новый сигнал в файл
        with open("mgnt_signal_only.txt", "w") as file:
            file.write(data['new_signal'])
        await message.answer(f"{checkmark}Новый сигнал в % по MGNT установлен: {data['new_signal']}",
                             reply_markup=signal_only_keyboard)

    # Завершаем состояние FSMContext
    await state.finish()
    with open('mgnt.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    x = None
    for line in lines:
        if "Спред MGNT - MGNT-12.23:" in line:
            parts = line.split()
            x_index = parts.index('Спред') + 4
            x = parts[x_index]
    with open("mgnt_spread_only.txt", "w") as file:
        pass
        file.write(x)


@dp.message_handler(Text(equals="Сброс сигнала в % по MGNT."))
async def fix_mgnt_tvh(message: types.Message):
    mess = 'Сбросить сигнал по MGNT?'
    await bot.send_message(message.chat.id, mess, reply_markup=mgnt_signal_only_sbros_keyboard)


@dp.message_handler(Text(equals="Сбросить сигнал MGNT."))
async def reset_mgnt_tvh(message: types.Message):
    mgnt_tvh_file = 'mgnt_signal_only.txt'

    if os.path.exists(mgnt_tvh_file):
        with open(mgnt_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Сигнал для MGNT сброшен.", reply_markup=mgnt_signal_only_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала.", reply_markup=mgnt_signal_only_keyboard)


@dp.message_handler(Text(equals="MGNT, п"))
async def with_puree(message: types.Message):
    # Открываем клавиатуру с кнопками для управления сигналами
    await message.answer("Выберите действие:", reply_markup=mgnt_signal_firstspread_keyboard)


@dp.message_handler(Text(equals="Текущий сигнал по MGNT, п"))
async def current_signal_mgnt(message: types.Message):
    # Считываем текущий сигнал из файла и отправляем его пользователю
    try:
        mgnt_tvh_file = 'mgnt_firstspread_and_signal.txt'

        if os.path.exists(mgnt_tvh_file):
            with open(mgnt_tvh_file, "r") as file:
                data = file.read().strip()  # Убираем лишние пробелы и переводы строк

            if not data:
                await message.answer("Текущий сигнал по MGNT не установлен",
                                     reply_markup=mgnt_signal_firstspread_keyboard)
            else:
                values = data.split(', ')
                signal = values[-1]
                if not signal:
                    await message.answer("Текущий сигнал по MGNT не установлен",
                                         reply_markup=mgnt_signal_firstspread_keyboard)
                else:
                    await message.answer(f"Текущий сигнал по MGNT: {signal}",
                                         reply_markup=mgnt_signal_firstspread_keyboard)
    except FileNotFoundError:
        await message.answer("Сигнал не найден", reply_markup=mgnt_signal_firstspread_keyboard)


@dp.message_handler(Text(equals="Новый сигнал по MGNT, п"))
async def new_signal_mgnt(message: types.Message, state: FSMContext):
    # Запрашиваем новое значение сигнала и записываем его в файл
    await message.answer("Введите новое значение сигнала по MGNT:")
    # Устанавливаем состояние для ожидания нового значения сигнала
    await YourState.new_mgnt_spread_first.set()


@dp.message_handler(state=YourState.new_mgnt_spread_first)
async def process_new_signal(message: types.Message, state: FSMContext):
    mgnt_tvh_file = 'mgnt_tvh.txt'

    if os.path.exists(mgnt_tvh_file):
        # Проверьте, является ли файл пустым
        is_empty = not bool(open(mgnt_tvh_file, 'r', encoding='utf-8').read())

        if is_empty:
            with open(mgnt_tvh_file, 'a', encoding='utf-8') as fw:
                with open('mgnt.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                x = None
                for line in lines:
                    if "Спред MGNT - MGNT-12.23:" in line:
                        parts = line.split()
                        x_index = parts.index('Спред') + 4
                        x = parts[x_index]
                        break

    async with state.proxy() as data:
        data['new_signal'] = message.text

        # Проверка, является ли введенное значение числом
        try:
            new_signal = float(data['new_signal'])
        except ValueError:
            # Если введенное значение не является числом, открываем клавиатуру
            await message.answer("Введите число")
            return  # Выходим из обработчика

        # Сохраняем новый сигнал в файл
        with open("mgnt_firstspread_and_signal.txt", "w") as file:
            file.write(f"{x}, {data['new_signal']}")
        await message.answer(f"{checkmark}Новый сигнал по MGNT установлен: {data['new_signal']}",
                             reply_markup=signal_firstspread_keyboard)

    # Завершаем состояние FSMContext
    await state.finish()


@dp.message_handler(Text(equals="Сброс сигнала по MGNT, п"))
async def fix_mgnt_tvh(message: types.Message):
    mess = 'Сбросить сигнал по MGNT?'
    await bot.send_message(message.chat.id, mess, reply_markup=mgnt_signal_firstspread_sbros_keyboard)


@dp.message_handler(Text(equals="Сбросить сигнал MGNT, п"))
async def reset_mgnt_tvh(message: types.Message):
    mgnt_tvh_file = 'mgnt_firstspread_and_signal.txt'

    if os.path.exists(mgnt_tvh_file):
        with open(mgnt_tvh_file, 'w', encoding='utf-8') as fw:
            pass  # Это создаст пустой файл, стирая всё содержимое
        await message.answer("Сигнал для MGNT сброшен.", reply_markup=signal_firstspread_keyboard)
    else:
        await message.answer("Нет сохранённого сигнала.", reply_markup=signal_firstspread_keyboard)





if __name__ == '__main__':
    executor.start_polling(dp)





