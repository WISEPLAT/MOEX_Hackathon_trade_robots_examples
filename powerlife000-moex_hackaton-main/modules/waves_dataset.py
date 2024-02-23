#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def waves_dataset(df, prefix = ':1d'):
    
    import pandas as pd
    import numpy as np

    #Волны + дивергенции
    #OBV
    #MACD
    #МАCD гистограмма
    #RSI
    #Стохастик
    #CCI
    temp_df = df.copy(deep = True)

    #Датасет только с точками экстремума
    extr_df = temp_df.dropna(subset = ['extr'])
    #Датасет с точками минимумов
    min_extr_df = extr_df[extr_df['extr'] == 'min']
    #Датасет с точками максимумов
    max_extr_df = extr_df[extr_df['extr'] == 'max']

    #Добавляем поля с предыдущей точкой
    min_extr_df['last_Close'] = min_extr_df['Close'].shift(1)
    min_extr_df['last_'+'MACD_12_26_9'+prefix] = min_extr_df['MACD_12_26_9'+prefix].shift(1)
    min_extr_df['last_'+'OBV'+prefix] = min_extr_df['OBV'+prefix].shift(1)
    
    min_extr_df['last_'+'RSI_14'+prefix] = min_extr_df['RSI_14'+prefix].shift(1)
    min_extr_df['last_'+'CCI_9'+prefix] = min_extr_df['CCI_9'+prefix].shift(1)
    min_extr_df['last_'+'STOCHRSIk_14'+prefix] = min_extr_df['STOCHRSIk_14'+prefix].shift(1)
    min_extr_df['last_'+'STOCHk_14'+prefix] = min_extr_df['STOCHk_14'+prefix].shift(1)
    min_extr_df['last_'+'STOCHk_50'+prefix] = min_extr_df['STOCHk_50'+prefix].shift(1)
    min_extr_df['last_'+'MACDh_12_26_9'+prefix] = min_extr_df['MACDh_12_26_9'+prefix].shift(1)

    max_extr_df['last_Close'] = max_extr_df['Close'].shift(1)
    max_extr_df['last_'+'MACD_12_26_9'+prefix] = max_extr_df['MACD_12_26_9'+prefix].shift(1)
    max_extr_df['last_'+'OBV'+prefix] = max_extr_df['OBV'+prefix].shift(1)
    
    max_extr_df['last_'+'RSI_14'+prefix] = max_extr_df['RSI_14'+prefix].shift(1)
    max_extr_df['last_'+'CCI_9'+prefix] = max_extr_df['CCI_9'+prefix].shift(1)
    max_extr_df['last_'+'STOCHRSIk_14'+prefix] = max_extr_df['STOCHRSIk_14'+prefix].shift(1)
    max_extr_df['last_'+'STOCHk_14'+prefix] = max_extr_df['STOCHk_14'+prefix].shift(1)
    max_extr_df['last_'+'STOCHk_50'+prefix] = max_extr_df['STOCHk_50'+prefix].shift(1)
    max_extr_df['last_'+'MACDh_12_26_9'+prefix] = max_extr_df['MACDh_12_26_9'+prefix].shift(1)

    #Очищаем датасет
    min_extr_df = min_extr_df.dropna(subset = ['last_Close'])
    min_extr_df = min_extr_df.dropna(subset = ['last_'+'MACD_12_26_9'+prefix])
    min_extr_df = min_extr_df.dropna(subset = ['last_'+'OBV'+prefix])
    
    min_extr_df = min_extr_df.dropna(subset = ['last_'+'RSI_14'+prefix])
    min_extr_df = min_extr_df.dropna(subset = ['last_'+'CCI_9'+prefix])
    min_extr_df = min_extr_df.dropna(subset = ['last_'+'STOCHRSIk_14'+prefix])
    min_extr_df = min_extr_df.dropna(subset = ['last_'+'STOCHk_14'+prefix])
    min_extr_df = min_extr_df.dropna(subset = ['last_'+'STOCHk_50'+prefix])
    min_extr_df = min_extr_df.dropna(subset = ['last_'+'MACDh_12_26_9'+prefix])

    max_extr_df = max_extr_df.dropna(subset = ['last_Close'])
    max_extr_df = max_extr_df.dropna(subset = ['last_'+'MACD_12_26_9'+prefix])
    max_extr_df = max_extr_df.dropna(subset = ['last_'+'OBV'+prefix])
    
    max_extr_df = max_extr_df.dropna(subset = ['last_'+'RSI_14'+prefix])
    max_extr_df = max_extr_df.dropna(subset = ['last_'+'CCI_9'+prefix])
    max_extr_df = max_extr_df.dropna(subset = ['last_'+'STOCHRSIk_14'+prefix])
    max_extr_df = max_extr_df.dropna(subset = ['last_'+'STOCHk_14'+prefix])
    max_extr_df = max_extr_df.dropna(subset = ['last_'+'STOCHk_50'+prefix])
    max_extr_df = max_extr_df.dropna(subset = ['last_'+'MACDh_12_26_9'+prefix])

    #Рост или падение котировок по вершинкам/впадинам
    #Рост или падение OBV по вершинам/впадинам
    #Рост или падение по MACD

    min_extr_df['waves_'+'close_min'+prefix] = np.where(min_extr_df['Close'] > min_extr_df['last_Close'], 1, -1)
    min_extr_df['waves_'+'MACD_12_26_9_min'+prefix] = np.where(min_extr_df['MACD_12_26_9'+prefix] > min_extr_df['last_'+'MACD_12_26_9'+prefix], 1, -1)
    min_extr_df['waves_'+'OBV_min'+prefix] = np.where(min_extr_df['OBV'+prefix] > min_extr_df['last_'+'OBV'+prefix], 1, -1)
    
    min_extr_df['waves_'+'RSI_14_min'+prefix] = np.where(min_extr_df['RSI_14'+prefix] > min_extr_df['last_'+'RSI_14'+prefix], 1, -1)
    min_extr_df['waves_'+'CCI_9_min'+prefix] = np.where(min_extr_df['CCI_9'+prefix] > min_extr_df['last_'+'CCI_9'+prefix], 1, -1)
    min_extr_df['waves_'+'STOCHRSIk_14_min'+prefix] = np.where(min_extr_df['STOCHRSIk_14'+prefix] > min_extr_df['last_'+'STOCHRSIk_14'+prefix], 1, -1)
    min_extr_df['waves_'+'STOCHk_14_min'+prefix] = np.where(min_extr_df['STOCHk_14'+prefix] > min_extr_df['last_'+'STOCHk_14'+prefix], 1, -1)
    min_extr_df['waves_'+'STOCHk_50_min'+prefix] = np.where(min_extr_df['STOCHk_50'+prefix] > min_extr_df['last_'+'STOCHk_50'+prefix], 1, -1)
    min_extr_df['waves_'+'MACDh_12_26_9_min'+prefix] = np.where(min_extr_df['MACDh_12_26_9'+prefix] > min_extr_df['last_'+'MACDh_12_26_9'+prefix], 1, -1)

    max_extr_df['waves_'+'close_max'+prefix] = np.where(max_extr_df['Close'] > max_extr_df['last_Close'], 1, -1)
    max_extr_df['waves_'+'MACD_12_26_9_max'+prefix] = np.where(max_extr_df['MACD_12_26_9'+prefix] > max_extr_df['last_'+'MACD_12_26_9'+prefix], 1, -1)
    max_extr_df['waves_'+'OBV_max'+prefix] = np.where(max_extr_df['OBV'+prefix] > max_extr_df['last_'+'OBV'+prefix], 1, -1)
    
    max_extr_df['waves_'+'RSI_14_max'+prefix] = np.where(max_extr_df['RSI_14'+prefix] > max_extr_df['last_'+'RSI_14'+prefix], 1, -1)
    max_extr_df['waves_'+'CCI_9_max'+prefix] = np.where(max_extr_df['CCI_9'+prefix] > max_extr_df['last_'+'CCI_9'+prefix], 1, -1)
    max_extr_df['waves_'+'STOCHRSIk_14_max'+prefix] = np.where(max_extr_df['STOCHRSIk_14'+prefix] > max_extr_df['last_'+'STOCHRSIk_14'+prefix], 1, -1)
    max_extr_df['waves_'+'STOCHk_14_max'+prefix] = np.where(max_extr_df['STOCHk_14'+prefix] > max_extr_df['last_'+'STOCHk_14'+prefix], 1, -1)
    max_extr_df['waves_'+'STOCHk_50_max'+prefix] = np.where(max_extr_df['STOCHk_50'+prefix] > max_extr_df['last_'+'STOCHk_50'+prefix], 1, -1)
    max_extr_df['waves_'+'MACDh_12_26_9_max'+prefix] = np.where(max_extr_df['MACDh_12_26_9'+prefix] > max_extr_df['last_'+'MACDh_12_26_9'+prefix], 1, -1)

    
    #Дивергенции
    ind_temp_arr = [
        'MACD_12_26_9_min',
        'OBV_min',
        'RSI_14_min',
        'CCI_9_min', 
        'STOCHRSIk_14_min',
        'STOCHk_14_min',
        'STOCHk_50_min',
        'MACDh_12_26_9_min'
    ]
    
    for ind_temp in ind_temp_arr:
        min_extr_df['div_'+ind_temp+prefix] = np.where(
            (
                (min_extr_df['waves_'+ind_temp+prefix] == 1) & (min_extr_df['waves_'+'close_min'+prefix] == 1)
                | (min_extr_df['waves_'+ind_temp+prefix] == -1) & (min_extr_df['waves_'+'close_min'+prefix] == -1)
            ),
            1, -1)
        
    ind_temp_arr = [
        'MACD_12_26_9_max',
        'OBV_max', 
        'RSI_14_max',
        'CCI_9_max', 
        'STOCHRSIk_14_max',
        'STOCHk_14_max',
        'STOCHk_50_max',
        'MACDh_12_26_9_max'
    ]
    
    for ind_temp in ind_temp_arr:
        max_extr_df['div_'+ind_temp+prefix] = np.where(
            (
                (max_extr_df['waves_'+ind_temp+prefix] == 1) & (max_extr_df['waves_'+'close_max'+prefix] == 1)
                | (max_extr_df['waves_'+ind_temp+prefix] == -1) & (max_extr_df['waves_'+'close_max'+prefix] == -1)
            ),
            1, -1)
    
    
    min_extr_df_1 = min_extr_df[
        [
            'waves_'+'close_min'+prefix, 
            'waves_'+'MACD_12_26_9_min'+prefix, 
            'waves_'+'OBV_min'+prefix,
            
            'waves_'+'RSI_14_min'+prefix,
            'waves_'+'CCI_9_min'+prefix,
            'waves_'+'STOCHRSIk_14_min'+prefix,
            'waves_'+'STOCHk_14_min'+prefix,
            'waves_'+'STOCHk_50_min'+prefix,
            'waves_'+'MACDh_12_26_9_min'+prefix,
            
            'div_'+'MACD_12_26_9_min'+prefix, 
            'div_'+'OBV_min'+prefix,
            
            'div_'+'RSI_14_min'+prefix,
            'div_'+'CCI_9_min'+prefix,
            'div_'+'STOCHRSIk_14_min'+prefix,
            'div_'+'STOCHk_14_min'+prefix,
            'div_'+'STOCHk_50_min'+prefix,
            'div_'+'MACDh_12_26_9_min'+prefix
        ]
    ]
    max_extr_df_1 = max_extr_df[
        [
            'waves_'+'close_max'+prefix, 
            'waves_'+'MACD_12_26_9_max'+prefix, 
            'waves_'+'OBV_max'+prefix,
            
            'waves_'+'RSI_14_max'+prefix,
            'waves_'+'CCI_9_max'+prefix,
            'waves_'+'STOCHRSIk_14_max'+prefix,
            'waves_'+'STOCHk_14_max'+prefix,
            'waves_'+'STOCHk_50_max'+prefix,
            'waves_'+'MACDh_12_26_9_max'+prefix,
            
            'div_'+'MACD_12_26_9_max'+prefix, 
            'div_'+'OBV_max'+prefix,
            
            'div_'+'RSI_14_max'+prefix,
            'div_'+'CCI_9_max'+prefix,
            'div_'+'STOCHRSIk_14_max'+prefix,
            'div_'+'STOCHk_14_max'+prefix,
            'div_'+'STOCHk_50_max'+prefix,
            'div_'+'MACDh_12_26_9_max'+prefix
        ]
    ]

    
    #Собираем датасет
    new_df = pd.DataFrame()
    new_df.index = temp_df.index
    new_df = new_df.join(min_extr_df_1)
    new_df = new_df.join(max_extr_df_1)

    #Заполняем пустые ячейки
    new_df = new_df.fillna(0)

    return new_df

