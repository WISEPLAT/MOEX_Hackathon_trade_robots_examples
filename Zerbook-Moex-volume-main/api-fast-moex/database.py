import psycopg2
import pandas as pd
import logging
from settings import HOST, USER, DB_NAME, PASSWORD
from date_format import convertStr
from utils import create_empty_df, processed_data


def get_dateAllInstr(instrument, start_date, end_date):
    # Чтение из базы данных массив дат по определенному инструменту
    dates_base = []
    df_by_instrument = {}

    df_by_instrument = create_empty_df()
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
                f"""SELECT I.nameindex, O.date, O.jurl, O.jurs, O.phyl, O.phys, O.summary
                                 FROM openpos AS O, instruments AS I
                                 WHERE O.IndexId = I.Id AND I.nameindex = '{instrument}' AND (O.date between '{start_date}' and '{end_date}') ORDER BY O.date ASC;"""
            )
            for results in cursor.fetchall():
                if results[6] != 0:
                    proces_df = processed_data(results)
                    df_by_instrument = pd.concat([df_by_instrument, proces_df])



            #     buf_str = convertStr(results[1])
            #     dates_base.append(buf_str)
            # ttt = df_by_instrument.to_json(orient="records")
            # yyyui = ttt
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
    return df_by_instrument.to_json(orient="records")


def get_deltaJur(instrument, start_date, end_date):
    # Чтение из базы данных массив дат по определенному инструменту
    logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
    logger = logging.getLogger(__name__)
    dates_base = []
    df_by_instrument = {}

    df_by_instrument = create_empty_df()
    logger.info(HOST)
    logger.info(USER)
    logger.info(PASSWORD)
    logger.info(DB_NAME)


    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME,
        )
        connection.autocommit = True
        logger.info('11111111')
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT I.nameindex, O.date, O.jurl, O.jurs, O.phyl, O.phys, O.summary
                                 FROM openpos AS O, instruments AS I
                                 WHERE O.IndexId = I.Id AND I.nameindex = '{instrument}' AND (O.date between '{start_date}' and '{end_date}') ORDER BY O.date ASC;"""
            )
            for results in cursor.fetchall():
                if results[6] != 0:
                    proces_df = processed_data(results)
                    df_by_instrument = pd.concat([df_by_instrument, proces_df])
    except Exception as _ex:
        logger.info(_ex)
        print("[INFO] Error while working with PostgreSQL", _ex)
        
    finally:
        print(f'{instrument}    {start_date}   {end_date} ' )
        if connection:
            connection.close()

    df_by_instrument['value'] = df_by_instrument['jurl'] - df_by_instrument['jurs']
    df_by_instrument.rename(columns={"date": "time"}, inplace = True)
    df_by_instrument.drop(['instrument', 'jurl', 'jurs', 'phyl', 'phys', 'summary'], axis= 1 , inplace= True )
    # print(type(df_by_instrument))
    return df_by_instrument.to_json(orient="records")

    # "instrument": result[0],
    # "date": convertStr(result[1]),
    # "jurl": result[2],
    # "jurs": result[3],
    # "phyl": result[4],
    # "phys": result[5],
    # "summary": result[6]