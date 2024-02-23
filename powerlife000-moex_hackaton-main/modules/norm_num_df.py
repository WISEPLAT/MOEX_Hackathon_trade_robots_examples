#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Нормализация числового датасета
def norm_num_df(df_temp, prefix = ':1d'):
    import pandas as pd
    import pandas_ta as ta
    import numpy as np
    
    df = df_temp.copy(deep = True)
    
    #Инициализируем пустой датасет
    new_df = pd.DataFrame()
    new_df.index = df.index
        
    #Список индикаторов для нормализации по close
    columns = ['Open', 'High', 'Low']
    
    for col in columns:
        try:
            new_df[col+prefix] = (df[col] / df['Close']) - 1
        except:
            #print("Отсутствует колонка: ", col)
            pass
        
    #Список индикаторов для нормализации по close
    columns = ['EMA_3', 'EMA_5', 'EMA_8', 'EMA_9', 'EMA_13',
       'EMA_14', 'EMA_20', 'EMA_25', 'EMA_49', 'EMA_50',
       'EMA_89', 'EMA_100', 'EMA_150', 'EMA_200', 'EMA_256',
       'EMA_356', 'KC_20_10_3.2_UPPER', 'KC_20_10_3.2_LOWER',
       'KC_50_18_3.2_UPPER', 'KC_50_18_3.2_LOWER', 'BBL_20_2.0',
       'BBM_20_2.0', 'BBU_20_2.0', 'BBL_20_3.0', 'BBM_20_3.0',
       'BBU_20_3.0', 'BBL_50_2.0', 'BBM_50_2.0', 'BBU_50_2.0',
       'BBL_50_3.0', 'BBM_50_3.0', 'BBU_50_3.0']
    
    for col in columns:
        try:
            new_df[col+prefix] = (df[col+prefix] / df['Close']) - 1
        except:
            #print("Отсутствует колонка: ", col)
            pass
        
    #'RSI_14:1d'
    test = df['RSI_14'+prefix]
    new_df['RSI_14'+prefix] = (test - 50)/50
    
    #'CCI_9'
    test = df['CCI_9'+prefix]
    new_df['CCI_9'+prefix] = test/300
    
    #STOCHRSIk_14
    test = df['STOCHRSIk_14'+prefix]
    new_df['STOCHRSIk_14'+prefix] = (test - 50)/50
    
    #STOCHk_14
    test = df['STOCHk_14'+prefix]
    new_df['STOCHk_14'+prefix] = (test - 50)/50
    
    #STOCHd_14
    test = df['STOCHd_14'+prefix]
    new_df['STOCHd_14'+prefix] = (test - 50)/50
    
    #STOCHk_50
    test = df['STOCHk_50'+prefix]
    new_df['STOCHk_50'+prefix] = (test - 50)/50
    
    #STOCHd_50
    test = df['STOCHd_50'+prefix]
    new_df['STOCHd_50'+prefix] = (test - 50)/50

    #Заменяем 0 на близкое значение
    df['OBV'+prefix] = df['OBV'+prefix].replace(0, 0.0001)

    for i in [1,2,3,5,7,9,14,50]:
        new_df['OBV_'+str(i)+prefix] = (df['OBV'+prefix]/df['OBV'+prefix].shift(i))-1

    #Заменяем 0 на близкое значение
    df['MACD_12_26_9'+prefix] = df['MACD_12_26_9'+prefix].replace(0, 0.0001)
    df['MACDs_12_26_9'+prefix] = df['MACDs_12_26_9'+prefix].replace(0, 0.0001)

    new_df['MACD'+prefix] = df.apply(lambda x: x['MACD_12_26_9'+prefix] / x['MACDs_12_26_9'+prefix], axis = 1)
    
    for i in range (1,8):
        new_df['MACD_'+str(i)+prefix] = (df['MACD_12_26_9'+prefix] / df['MACD_12_26_9'+prefix].shift(i))-1   
        new_df['MACDs_'+str(i)+prefix] = (df['MACDs_12_26_9'+prefix] / df['MACDs_12_26_9'+prefix].shift(i))-1
        new_df['MACDh_'+str(i)+prefix] = (df['MACDh_12_26_9'+prefix]/df['MACDh_12_26_9'+prefix].shift(i))-1
    
    #Заменяем 0 на близкое значение
    df['AC'+prefix] = df['AC'+prefix].replace(0, 0.0001)
    for i in range (1,8):
        new_df['AC_'+str(i)+prefix] = (df['AC'+prefix]/df['AC'+prefix].shift(i))-1

    #Заменяем 0 на близкое значение
    df['FI_14'+prefix] = df['FI_14'+prefix].replace(0, 0.0001)
    for i in range (1,8):
        new_df['FI_14_'+str(i)+prefix] = (df['FI_14'+prefix]/df['FI_14'+prefix].shift(i))-1
    
    #Заменяем 0 на близкое значение
    df['BEARS_14'+prefix] = df['BEARS_14'+prefix].replace(0, 0.0001)
    for i in range (1,8):
        new_df['BEARS_14_'+str(i)+prefix] = (df['BEARS_14'+prefix]/df['BEARS_14'+prefix].shift(i))-1


    #'PSAR' оставляем без изменений
    new_df['PSAR'+prefix] = df['PSAR'+prefix]
    
    return new_df

