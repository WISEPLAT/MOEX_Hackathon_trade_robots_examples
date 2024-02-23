import psycopg2
from settings import HOST, USER, DB_NAME, PASSWORD
from support.date_format import convertStr, convertTimestampDate, check_correct, data_AddOneDay


def readListIndex():
    # Чтение списка инструментов из базы данных
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        buf_index = []
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT nameindex FROM instruments ORDER BY id ASC"
            )
            for person in cursor.fetchall():
                buf_index.append(person[0])
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
    return buf_index

def get_date_stActual(instrument):
    # Чтение из базы данных актуальной стартовой даты
    dateAct = ''
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT nameindex, startdate FROM instruments WHERE nameindex = '{instrument}'; "
            )
            result = cursor.fetchone()
            if not result[1] is None:
                dateAct = result[1]
                #print(f"{result[1]}")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
    return dateAct
def get_date_endActual(instrument):
    # Чтение из базы данных актуальной оследней даты
    dateAct = ''
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT nameindex, enddate FROM instruments WHERE nameindex = '{instrument}'; "
            )
            result = cursor.fetchone()
            if not result[1] is None:
                dateAct = result[1]
                #print(f"{result[1]}")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
    return dateAct

def get_dateMaxToInstrum(instrument):
    # Получение максимальной (последней даты по определенному инструменту)
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT MAX(O.date)
                                 FROM openpos AS O, instruments AS I
                                 WHERE O.IndexId = I.Id AND I.nameindex = '{instrument}';"""
            )
            result = cursor.fetchone()
            # print(result[0])
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
    return convertStr(result[0])

def get_param_date():
    # Чтение из базы данных параметров стандартного периода
    param_date = []
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT value FROM Settings WHERE parameter = 'start_date'"""
            )
            results = cursor.fetchone()
            param_date.append(results[0])
            cursor.execute(
                f"""SELECT value FROM Settings WHERE parameter = 'end_date'"""
            )
            results = cursor.fetchone()
            param_date.append(results[0])


    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
    return param_date

def get_realbase_date():
    # Чтение максимум и минимум дат из базы
    realbase_date = []
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT MIN(date) FROM openpos;"""
            )
            results = cursor.fetchone()
            realbase_date.append(convertStr(results[0]))
            cursor.execute(
                f"""SELECT MAX(date) FROM openpos;"""
            )
            results = cursor.fetchone()
            realbase_date.append(convertStr(results[0]))


    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
    return realbase_date

def get_dateBaseR(instrument, param_date):
    # Чтение из базы данных массив дат по определенному инструменту
    dates_base = []
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT I.nameindex, O.date
                                 FROM openpos AS O, instruments AS I
                                 WHERE O.IndexId = I.Id AND I.nameindex = '{instrument}' AND (O.date between '{param_date[0]}' and '{param_date[1]}') ORDER BY O.date ASC;"""
            )
            for results in cursor.fetchall():
                buf_str = convertStr(results[1])
                dates_base.append(buf_str)

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
    return dates_base
def set_date_stActual(instrument, dateAct):
    # Запись в базу начальной актуальной даты
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(

                f"update instruments set StartDate = '{dateAct}' where nameindex = '{instrument}';"
            )
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()

def set_date_endActual(instrument, dateAct):
    # Запись в базу последней актуальной даты
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(

                f"update instruments set endDate = '{dateAct}' where nameindex = '{instrument}';"
            )
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()

def set_table_data(instrument, df_bufer):
    # Сохранение загруженных данных в базу данных
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT Id FROM Instruments WHERE Nameindex='{instrument}'")
            id_index = cursor.fetchone()
            for index, row in df_bufer.iterrows():
                if check_correct(row):
                    buf_date = convertTimestampDate(row['date'])
                    print(f"запись в базу {instrument}  {buf_date}")
                    cursor.execute(
                        f"""INSERT INTO openpos(IndexId, date, JurL, JurS, PhyL, PhyS, Summary, actual)
                                VALUES
                                (
                                    {id_index[0]},
                                    '{buf_date}',
                                    {row['JurL']},
                                    {row['JurS']},
                                    {row['PhyL']},
                                    {row['PhyS']},
                                    {row['Summary']},
                                    true 
                                );"""
                    )

            # print(f"Server version: {cursor.fetchone}")
            connection.commit()

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
def base_addOneDay(pr_dateEnd):
    # в параметрах увеличивает дату на один день и записывает обратно в базу

    pr_dateEnd = data_AddOneDay(pr_dateEnd)
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                #  f"""SELECT value FROM Settings WHERE parameter = 'start_date'"""
                f"update settings set value = '{pr_dateEnd}' where parameter = 'end_date';"
            )
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()