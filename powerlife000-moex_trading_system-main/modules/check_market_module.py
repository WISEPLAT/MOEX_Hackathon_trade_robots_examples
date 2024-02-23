#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def check_market(config, is_notebook):
    import pandas_market_calendars as mcal
    from datetime import datetime
    import pandas as pd
    import numpy as np

    status = 'closed'

    # Create a calendar
    nyse = mcal.get_calendar('XMOS')

    now = datetime.now().strftime("%Y-%m-%d")

    early = nyse.schedule(start_date=now, end_date=now)

    if early.shape[0] != 0:
        utcnow = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        early['now'] = np.datetime64(utcnow)
        early['now'] = early['now'].dt.tz_localize('UTC')

        early['check_market'] = (early['now'] >= early['market_open']) & (early['now'] < early['market_close'])

        early['time_to_close'] = early['market_close'] - early['now']

        if early.shape[0] > 0:
            if early.iloc[0]['check_market'] == True:
                status = 'open'

        time_to_close = early.iloc[0]['time_to_close'].total_seconds()
    else:
        status = 'closed'
        time_to_close = None

    return status, time_to_close

