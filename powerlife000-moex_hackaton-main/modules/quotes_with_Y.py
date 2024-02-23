#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Разметка Y
def quotes_with_Y(quotes_with_extrems, extr_bar_count, Y_shift, max_unmark = 0.3):
    
    try:
        quotes_with_extrems.drop(columns = ['Datetime'], inplace = True)
    except:
        pass
    
    quotes_with_extrems.reset_index(inplace = True)
    
    quotes_with_extrems['Y'] = None
    
    last_extr = quotes_with_extrems.iloc[0]['extr']
    bar_count = 0
    
    max_bar_count = 0
    
    for i, quote in quotes_with_extrems.iterrows():
        if (quote['extr'] != last_extr) & ((quote['extr'] == 'min') | (quote['extr'] == 'max')):
            last_extr = quote['extr']
            bar_count = 0
            
            #Считаем сколько баров до следующей точки экстремума
            max_bar_count = 0
            if quotes_with_extrems[quotes_with_extrems.index > i]['extr'].isin(['min', 'max']).any():
                for j, row in quotes_with_extrems[quotes_with_extrems.index > i].iterrows():
                    if (row['extr'] == 'min') | (row['extr'] == 'max'):
                        break
                    else:
                        max_bar_count += 1
            else:
                max_bar_count = quotes_with_extrems[quotes_with_extrems.index > i].shape[0]

        if (bar_count < extr_bar_count) & (bar_count < max_bar_count*(1-max_unmark)):
            if last_extr == 'min':
                quotes_with_extrems.at[i, 'Y'] = 1 + Y_shift
                bar_count = bar_count + 1
            elif last_extr == 'max':
                quotes_with_extrems.at[i, 'Y'] = -1 + Y_shift
                bar_count = bar_count + 1
        else:
            quotes_with_extrems.at[i, 'Y'] = 0 + Y_shift
            
    quotes_with_extrems.index = quotes_with_extrems['Datetime']

    return quotes_with_extrems

