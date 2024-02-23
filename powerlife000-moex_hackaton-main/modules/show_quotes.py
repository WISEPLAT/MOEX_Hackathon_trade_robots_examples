#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Смотрим исходные данные
def show_quotes(quotes):
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    import pandas as pd
    from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator  

    from mpl_finance import candlestick_ohlc  #  pip install mpl-finance
    import mplfinance as mpf
    
    fig, ax = plt.subplots(figsize=(26,18))
    fig.subplots_adjust(bottom=0.2)
    #ax.xaxis.set_major_locator(mondays)
    #ax.xaxis.set_minor_locator(alldays)
    #ax.xaxis.set_major_formatter(weekFormatter)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %Y"))
    #ax.xaxis.set_minor_formatter(dayFormatter)

    # plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax, zip(mdates.date2num(quotes.index),
                             quotes['Open'], quotes['High'],
                             quotes['Low'], quotes['Close']),
                     width=4)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')

    plt.show()

