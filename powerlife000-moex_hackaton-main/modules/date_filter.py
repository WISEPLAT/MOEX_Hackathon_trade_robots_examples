#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def date_filter(quotes, filter_data_timezone, filter_data_start, filter_data_end):
    import datetime
    import pytz
    
    tz_ny= pytz.timezone(filter_data_timezone)

    date1 = datetime.datetime.strptime(filter_data_start, '%Y-%m-%d %H:%M:%S')
    date1 = tz_ny.localize(date1)
    date2 = datetime.datetime.strptime(filter_data_end, '%Y-%m-%d %H:%M:%S')
    date2 = tz_ny.localize(date2)

    # select desired range of dates
    try:
        quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]
    except:
        try:
            date1 = np.datetime64(date1)
            date2 = np.datetime64(date2)
            quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]
        except:
            pass
    
    return quotes

