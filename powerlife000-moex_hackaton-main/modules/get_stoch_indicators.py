#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def get_stoch_indicators(df, prefix = ':1d'):
    import pandas as pd
    import pandas_ta as ta
    import numpy as np
    
    #Close, Open, Low, High на разных периодах
    
                #Скользящие средние
    #EMA_3 период 3
    #EMA_5 период 5
    #EMA_8 период 8
    #EMA_9 период 9
    #EMA_13 период 13
    #EMA_14 период 14
    #EMA_20 период 20
    #EMA_25 период 25
    #EMA_49 период 49
    #EMA_50 период 50
    #EMA_89 период 89
    #EMA_100 период 100
    #EMA_150 период 150
    #EMA_200 период 200
    #EMA_256 период 256
    #EMA_356 период 356
    
                #Каналы
    #KC 20,10,3.2  период 20
    #KC 50,18,3.2  период 50
    
    #BB 20 2  период 20
    #BB 20 3 период 20
    
    #BB 50 2 период 50
    #BB 50 3 период 50
    
                #Осцилляторы
    #RSI_14  период 14
    #CCI_9  период 9
    #StochasticRSI 14,14,14,3,3  период 14
    #Stochastic 14,3 повторение
    #Stochastic 50,3 повторение
    
                #Объёмные индикаторы
    #OBV  период 14
    
                #Дивергенция
    #MACD 12 26 9  период 26 26 9
    
                #Сила тренда
    #AC 5 34 5  период 3
    #ADX 7  период 3
    #ForceIndex 14  период 3
    #Bears  период 3
    
    #-----------------------------------------------------------------------------------------------
    
    #Создаём новый датафрейм
    new_df = pd.DataFrame()
    new_df.index = df.index
    
    #Генерируем признаки стохастика над данными бара
    indicators = ['Close', 'Open', 'High', 'Low']
    params_k = [3, 5, 7, 9, 14, 20, 50]
    d = 3
    smooth_k = 3
    for indicator in indicators:
        for k in params_k:
            try:
                data = df[indicator]
                stoch = ta.stoch(data, data, data, k=k, d=d, smooth_k=smooth_k)
                new_df[indicator+':STOCHk'+':'+str(k)+':'+str(d)+prefix] = (stoch['STOCHk_'+str(k)+'_'+str(d)+'_'+str(smooth_k)]-50)/50
                new_df[indicator+':STOCHd'+':'+str(k)+':'+str(d)+prefix] = (stoch['STOCHd_'+str(k)+'_'+str(d)+'_'+str(smooth_k)]-50)/50
                new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix] = 0
                new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix] = np.where(
                    new_df[indicator+':STOCHk'+':'+str(k)+':'+str(d)+prefix] > new_df[indicator+':STOCHd'+':'+str(k)+':'+str(d)+prefix],
                    1,
                    new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix]
                )
                new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix] = np.where(
                    new_df[indicator+':STOCHk'+':'+str(k)+':'+str(d)+prefix] < new_df[indicator+':STOCHd'+':'+str(k)+':'+str(d)+prefix],
                    -1,
                    new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix]
                )
            except Exception as e:
                print("stoch: indicator |", indicator," k| ", k, ' d| ', d, ' ', e)
                new_df[indicator+':STOCHk'+':'+str(k)+':'+str(d)+prefix] = None
                new_df[indicator+':STOCHd'+':'+str(k)+':'+str(d)+prefix] = None
                new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix] = None
    
        
    #Генерируем признаки стохастика над данными индикаторами
    arr = [
        ('EMA_3', 3),
        ('EMA_5', 5),
        ('EMA_8', 8),
        ('EMA_9', 9),
        ('EMA_13', 13),
        ('EMA_14', 14),
        ('EMA_20', 20),
        ('EMA_25', 25),
        ('EMA_49', 49),
        ('EMA_50', 50),
        ('EMA_89', 89),
        ('KC_20_10_3.2_UPPER', 20),
        ('KC_20_10_3.2_LOWER', 20),
        ('KC_50_18_3.2_UPPER', 50),
        ('KC_50_18_3.2_LOWER', 50),
        ('BBL_20_2.0', 20),
        ('BBM_20_2.0', 20),
        ('BBU_20_2.0', 20),
        ('BBL_20_3.0', 20),
        ('BBM_20_3.0', 20),
        ('BBU_20_3.0', 20),
        ('BBL_50_2.0', 50),
        ('BBM_50_2.0', 50),
        ('BBU_50_2.0', 50),
        ('BBL_50_3.0', 50),
        ('BBM_50_3.0', 50),
        ('BBU_50_3.0', 50),
        ('RSI_14', 14),
        ('CCI_9', 9),
        ('STOCHRSIk_14', 9),
        ('OBV', 9),
        ('MACD_12_26_9', 26),
        ('MACDh_12_26_9', 9),
        ('MACDs_12_26_9', 26),
        ('AC', 3),
        ('FI_14', 3),
        ('BEARS_14', 3)
    ]
    d = 3
    smooth_k = 3
    for indicator, k in arr:
        for k in params_k:
            try:
                data = df[indicator+prefix]
                stoch = ta.stoch(data, data, data, k=k, d=d, smooth_k=smooth_k)
                new_df[indicator+':STOCHk'+prefix] = stoch['STOCHk_'+str(k)+'_'+str(d)+'_'+str(smooth_k)]/100
                new_df[indicator+':STOCHd'+prefix] = stoch['STOCHd_'+str(k)+'_'+str(d)+'_'+str(smooth_k)]/100
                new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix] = 0
                new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix] = np.where(
                    new_df[indicator+':STOCHk'+prefix] > new_df[indicator+':STOCHd'+prefix],
                    1,
                    new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix]
                )
                new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix] = np.where(
                    new_df[indicator+':STOCHk'+prefix] < new_df[indicator+':STOCHd'+prefix],
                    -1,
                    new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix]
                )
            except Exception as e:
                print("stoch: indicator |", indicator," k| ", k, ' d| ', d, ' ', e)
                new_df[indicator+':STOCHk'+prefix] = None
                new_df[indicator+':STOCHd'+prefix] = None
                new_df[indicator+':STOCH'+':'+str(k)+':'+str(d)+prefix] = None
    
    #Stochastic 14,3 повторение
    indicator = 'STOCHk_14'
    new_df[indicator+':STOCHk'+prefix] = df[indicator+prefix]/100
    
    indicator = 'STOCHd_14'
    new_df[indicator+':STOCHd'+prefix] = df[indicator+prefix]/100
    
    #Stochastic 50,3 повторение
    indicator = 'STOCHk_50'
    new_df[indicator+':STOCHk'+prefix] = df[indicator+prefix]/100
    
    indicator = 'STOCHd_50'
    new_df[indicator+':STOCHd'+prefix] = df[indicator+prefix]/100
    
    new_df['PSAR'+prefix] = df['PSAR'+prefix]
        
    return new_df

