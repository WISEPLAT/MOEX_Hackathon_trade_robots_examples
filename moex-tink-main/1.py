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
