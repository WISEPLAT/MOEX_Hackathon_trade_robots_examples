import logging
import asyncio
from datetime import datetime

import pandas as pd
import aiohttp
from random import randint
import json
import time
from threading import Thread

from support.database import readListIndex, get_param_date, get_dateBaseR, set_date_stActual, set_table_data, \
    get_realbase_date, base_addOneDay, get_dateMaxToInstrum, set_date_endActual
from support.date_format import convForRequest, sravDateNot, sravRealTime, \
    sravBothDate, data_MinusOneDay
from support.util import date_range, processed_data, create_empty_df

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
logger = logging.getLogger(__name__)
logger.info("jskdfhjksdhfhksjdf9843983")

def function1():
    pass
    # while True:
    #     time.sleep(3)
    #     print(f'цукцукцукуцкуаывсчм')



async def trade(Index,dateS):
    try:
        async with aiohttp.ClientSession() as session:  # [3]
            iter = str(randint(90000, 99999))
            async with session.get('https://www.moex.com/api/contract/OpenOptionService/' + dateS + '/F/' + Index + '/json?_=' + iter) as resp:
                response = await resp.read()
                print(f"| Инструмент: {Index}, дата: {dateS}")

                data = json.loads(response)
                # print(f"укуукукку {data}")
                return processed_data(data,dateS)
    except Exception as ex:
        logger.error(ex)

if __name__ == '__main__':
    
    try:
        Thread(target=function1).start()
        Key_change = True
        while True:

            param_date = get_param_date()
            if sravRealTime(param_date[1]) and not Key_change:   # Если реальное время превышает которое в базе с учетом 22:10 а также ключ false означает что по выбранному дипазону все записи сохранены в базу
                base_addOneDay(param_date[1]) # увеличивает в базе дату окончания на 1 день
                param_date = get_param_date() # получаем дату окончания из базы

            realbase_date = get_realbase_date()

            # sravRealTime
            if sravDateNot(param_date[0],realbase_date[0]) or sravDateNot(param_date[1],realbase_date[1]) or Key_change:
                Key_change = False

                instruments = readListIndex()
                for instrument in instruments:

                    df_bufer = create_empty_df()
                    dates = date_range(instrument, param_date)
                    dates_base = get_dateBaseR(instrument, param_date)
                    for str_day in dates_base:
                        if str_day in dates:
                            dates.remove(str_day)

                    if dates:
                        for dateBuf in dates:
                            dateS = convForRequest(dateBuf)
                            proces_df = asyncio.run(trade(instrument, dateS))
                            # print(type(proces_df).__name__)

                            if type(proces_df).__name__ == 'IndexError':
                                print(f'это IndexError')

                                st_dateMaxInst = get_dateMaxToInstrum(instrument)
                                if sravBothDate(dateBuf, st_dateMaxInst) :
                                    #print(f'это дата: {dateBuf}')
                                    dateBuf1 = data_MinusOneDay(dateBuf)

                                    set_date_endActual(instrument, dateBuf1)
                                else:
                                    set_date_stActual(instrument, dateBuf)
                                # print(f"| такой даты: {dateS}, в инструменте {instrument} нет |")
                            else:
                                df_bufer = pd.concat([df_bufer, proces_df])


                        if not df_bufer.empty:
                            Key_change = True
                            set_table_data(instrument, df_bufer)
            time.sleep(20)  # 0.500 миллисекунд

            now = datetime.now()
            date_string = now.strftime('%H:%M:%S')
            print(f'текущее время: {date_string}')
    except Exception as ex:
        logger.error(ex)
