#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def show_quotes_with_trends(quotes_with_extrems, show = False):

    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    import pandas as pd
    from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator  

    from mpl_finance import candlestick_ohlc  #  pip install mpl-finance
    import mplfinance as mpf
    
    quotes_with_extrems['Color'] = None
    quotes_with_extrems['Trend'] = None
    
    #Раскрашиваем тренды
    last_extr = None

    for i, quote in quotes_with_extrems.iterrows():

        if quote['extr'] == 'max':
            last_extr = 'max'
        elif quote['extr'] == 'min':
            last_extr = 'min'

        if last_extr == 'min':
            quotes_with_extrems.at[i, 'Color'] = '#AFE1AF'#green
            quotes_with_extrems.at[i, 'Trend'] = 'buy'
        elif last_extr == 'max':
            quotes_with_extrems.at[i, 'Color'] = '#880808'#red
            quotes_with_extrems.at[i, 'Trend'] = 'sell'
    
    quotes_with_extrems['x'] = quotes_with_extrems.index
    
    y_max = quotes_with_extrems['High'].max()*1.05
    y_min = quotes_with_extrems['Low'].min()*0.95
    
    if show:
        fig, ax = plt.subplots(figsize=(26,18))
        fig.subplots_adjust(bottom=0.2)
        #ax.xaxis.set_major_locator(mondays)
        #ax.xaxis.set_minor_locator(alldays)
        #ax.xaxis.set_major_formatter(weekFormatter)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %Y"))
        #ax.xaxis.set_minor_formatter(dayFormatter)

        quote_count = 0
        for i, quote in quotes_with_extrems.iterrows():

            x = []
            y = []

            if quote_count+1 >= quotes_with_extrems.shape[0]:
                    break

            x.append(mdates.date2num(quotes_with_extrems.iloc[quote_count]['x']))
            x.append(mdates.date2num(quotes_with_extrems.iloc[quote_count+1]['x']))
            y.append(mdates.date2num(quotes_with_extrems.iloc[quote_count]['High']))
            y.append(mdates.date2num(quotes_with_extrems.iloc[quote_count+1]['High'])) 

            plt.fill_between(
                x = x,
                y1 = y_min,
                y2 = y_max,
                color = quotes_with_extrems.iloc[quote_count]['Color'], 
                alpha=0.3)

            quote_count = quote_count + 1



    
        # plot_day_summary(ax, quotes, ticksize=3)
        candlestick_ohlc(ax, zip(mdates.date2num(quotes_with_extrems.index),
                                 quotes_with_extrems['Open'], quotes_with_extrems['High'],
                                 quotes_with_extrems['Low'], quotes_with_extrems['Close']),
                         width=4)

        ax.xaxis_date()
        ax.autoscale_view()
        plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')

        plt.show()

