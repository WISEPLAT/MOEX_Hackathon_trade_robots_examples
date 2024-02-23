#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def get_indicators(df, prefix = ':1d'):
    import pandas as pd
    import pandas_ta as ta
    
    new_df = df.copy(deep = True)
    
    #Перечень индикаторов
                #Скользящие средние
    #EMA_3
    #EMA_5
    #EMA_8
    #EMA_9
    #EMA_13
    #EMA_14
    #EMA_20
    #EMA_25
    #EMA_49
    #EMA_50
    #EMA_89
    #EMA_100
    #EMA_150
    #EMA_200
    #EMA_256
    #EMA_356
    
                #Каналы
    #KC 20,10,3.2
    #KC 50,18,3.2
    
    #BB 20 2
    #BB 20 3
    
    #BB 50 2
    #BB 50 3
    
                #Осцилляторы
    #RSI_14
    #CCI_9
    #StochasticRSI 14,14,14,3,3
    #Stochastic 14,3
    #Stochastic 50,3
    
                #Объёмные индикаторы
    #OBV
    
                #Дивергенция
    #MACD 12 26 9
    
                #Сила тренда
    #AC 5 34 5
    #ADX 7
    #ForceIndex 14
    #Bears
    
                #Тренд
    #PSAR 0.02 0.2
    
    #-----------------------------------------------------------------------------------------------
    
                #Скользящие средние
    #EMA_3
    try:
        new_df['EMA_3'+prefix] = df.ta.ema(length = 3)
    except:
        new_df['EMA_3'+prefix] = None
        
    #EMA_5
    try:
        new_df['EMA_5'+prefix] = df.ta.ema(length = 5)
    except:
        new_df['EMA_5'+prefix] = None
    
    #EMA_8
    try:
        new_df['EMA_8'+prefix] = df.ta.ema(length = 8)
    except:
        new_df['EMA_8'+prefix] = None
    
    #EMA_9
    try:
        new_df['EMA_9'+prefix] = df.ta.ema(length = 9)
    except:
        new_df['EMA_9'+prefix] = None
    
    #EMA_13
    try:
        new_df['EMA_13'+prefix] = df.ta.ema(length = 13)
    except:
        new_df['EMA_13'+prefix] = None
    
    #EMA_14
    try:
        new_df['EMA_14'+prefix] = df.ta.ema(length = 14)
    except:
        new_df['EMA_14'+prefix] = None
    
    #EMA_20
    try:
        new_df['EMA_20'+prefix] = df.ta.ema(length = 20)
    except:
        new_df['EMA_20'+prefix] = None
    
    #EMA_25
    try:
        new_df['EMA_25'+prefix] = df.ta.ema(length = 25)
    except:
        new_df['EMA_25'+prefix] = None
    
    #EMA_49
    try:
        new_df['EMA_49'+prefix] = df.ta.ema(length = 49)
    except:
        new_df['EMA_49'+prefix] = None
    
    #EMA_50
    try:
        new_df['EMA_50'+prefix] = df.ta.ema(length = 50)
    except:
        new_df['EMA_50'+prefix] = None
    
    #EMA_89
    try:
        new_df['EMA_89'+prefix] = df.ta.ema(length = 89)
    except:
        new_df['EMA_89'+prefix] = None
    
                #Каналы
    #KC 20,10,3.2
    try:
        new_df['KC_20_10_3.2_UPPER'+prefix] = new_df['EMA_20'+prefix] + 3.2 * df.ta.atr(length = 10)
    except:
        new_df['KC_20_10_3.2_UPPER'+prefix] = None
        
    try:
        new_df['KC_20_10_3.2_LOWER'+prefix] = new_df['EMA_20'+prefix] - 3.2 * df.ta.atr(length = 10)
    except:
        new_df['KC_20_10_3.2_LOWER'+prefix] = None
    
    #KC 50,18,3.2
    try:
        new_df['KC_50_18_3.2_UPPER'+prefix] = new_df['EMA_50'+prefix] + 3.2 * df.ta.atr(length = 18)
    except:
        new_df['KC_50_18_3.2_UPPER'+prefix] = None
        
    try:
        new_df['KC_50_18_3.2_LOWER'+prefix] = new_df['EMA_50'+prefix] - 3.2 * df.ta.atr(length = 18)
    except:
        new_df['KC_50_18_3.2_LOWER'+prefix] = None
    
    #BB 20 2
    try:
        bb = df.ta.bbands(length = 20, std = 2)
        new_df['BBL_20_2.0'+prefix] = bb['BBL_20_2.0']#Нижняя граница
        new_df['BBM_20_2.0'+prefix] = bb['BBM_20_2.0']#Средняя линяя
        new_df['BBU_20_2.0'+prefix] = bb['BBU_20_2.0']#Верхняя граница
    except:
        new_df['BBL_20_2.0'+prefix] = None
        new_df['BBM_20_2.0'+prefix] = None
        new_df['BBU_20_2.0'+prefix] = None
    
    #BB 20 3
    try:
        bb = df.ta.bbands(length = 20, std = 3)
        new_df['BBL_20_3.0'+prefix] = bb['BBL_20_3.0']#Нижняя граница
        new_df['BBM_20_3.0'+prefix] = bb['BBM_20_3.0']#Средняя линяя
        new_df['BBU_20_3.0'+prefix] = bb['BBU_20_3.0']#Верхняя граница
    except:
        new_df['BBL_20_3.0'+prefix] = None
        new_df['BBM_20_3.0'+prefix] = None
        new_df['BBU_20_3.0'+prefix] = None
    
    #BB 50 2
    try:
        bb = df.ta.bbands(length = 50, std = 2)
        new_df['BBL_50_2.0'+prefix] = bb['BBL_50_2.0']#Нижняя граница
        new_df['BBM_50_2.0'+prefix] = bb['BBM_50_2.0']#Средняя линяя
        new_df['BBU_50_2.0'+prefix] = bb['BBU_50_2.0']#Верхняя граница
    except:
        new_df['BBL_50_2.0'+prefix] = None
        new_df['BBM_50_2.0'+prefix] = None
        new_df['BBU_50_2.0'+prefix] = None
    
    #BB 50 3
    try:
        bb = df.ta.bbands(length = 50, std = 3)
        new_df['BBL_50_3.0'+prefix] = bb['BBL_50_3.0']#Нижняя граница
        new_df['BBM_50_3.0'+prefix] = bb['BBM_50_3.0']#Средняя линяя
        new_df['BBU_50_3.0'+prefix] = bb['BBU_50_3.0']#Верхняя граница
    except:
        new_df['BBL_50_3.0'+prefix] = None
        new_df['BBM_50_3.0'+prefix] = None
        new_df['BBU_50_3.0'+prefix] = None
    
                #Осцилляторы
    #RSI_14
    try:
        new_df['RSI_14'+prefix] = df.ta.rsi(length = 14)
    except:
        new_df['RSI_14'+prefix] = None
    
    #CCI_9
    try:
        new_df['CCI_9'+prefix] = df.ta.cci(length = 9)
    except:
        new_df['CCI_9'+prefix] = None
        
    #StochasticRSI 14,14,14,3,3
    try:
        stochrsi = df.ta.stochrsi(length=14, rsi_length=14, k=3, d=3)
        new_df['STOCHRSIk_14'+prefix] = stochrsi['STOCHRSIk_14_14_3_3']
    except:
        new_df['STOCHRSIk_14'+prefix] = None
    
    #Stochastic 14,3
    try:
        stoch = df.ta.stoch(k=14, d=3, smooth_k=3)
        new_df['STOCHk_14'+prefix] = stoch['STOCHk_14_3_3']
    except:
        new_df['STOCHk_14'+prefix] = None
        
    try:
        stoch = df.ta.stoch(k=14, d=3, smooth_k=3)
        new_df['STOCHd_14'+prefix] = stoch['STOCHd_14_3_3']
    except:
        new_df['STOCHd_14'+prefix] = None
    
    #Stochastic 50,3
    try:
        stoch = df.ta.stoch(k=50, d=3, smooth_k=3)
        new_df['STOCHk_50'+prefix] = stoch['STOCHk_50_3_3']
    except:
        new_df['STOCHk_50'+prefix] = None
        
    try:
        stoch = df.ta.stoch(k=50, d=3, smooth_k=3)
        new_df['STOCHd_50'+prefix] = stoch['STOCHd_50_3_3']
    except:
        new_df['STOCHd_50'+prefix] = None
    
                #Объёмные индикаторы
    #OBV
    try:
        new_df['OBV'+prefix] = df.ta.obv()
    except:
        new_df['OBV'+prefix] = None
    
                #Дивергенция
    #MACD 12 26 9
    try:
        macd = df.ta.macd(fast=12, slow=26, signal=9)
        new_df['MACD_12_26_9'+prefix] = macd['MACD_12_26_9']
        new_df['MACDh_12_26_9'+prefix] = macd['MACDh_12_26_9']
        new_df['MACDs_12_26_9'+prefix] = macd['MACDs_12_26_9']
    except:
        new_df['MACD_12_26_9'] = None
        new_df['MACDh_12_26_9'] = None
        new_df['MACDs_12_26_9'] = None
    
                #Сила тренда
    #AC 5 34 5
    try:
        sma_5=ta.sma((df['High']-df['Low'])/2, length = 5)
        sma_34=ta.sma((df['High']-df['Low'])/2, length = 34)
        AO = sma_5-sma_34
        new_df['AC'+prefix] = AO - ta.sma(AO, length = 5)
    except:
        new_df['AC'+prefix] = None
        
    #ForceIndex 14
    try:
        last_close = df['Close'].shift(1)
        raw_force_index = (df['Close'] - last_close)*df['Volume']
        new_df['FI_14'+prefix] = ta.ema(raw_force_index, length = 14)
    except:
        new_df['FI_14'+prefix] = None
        
    #Bears
    try:
        new_df['BEARS_14'+prefix] = df['Low'] - df.ta.ema(length = 14)
    except:
        new_df['BEARS_14'+prefix] = None
    
                #Тренд
    #PSAR 0.02 0.2
    try:
        psar = df.ta.psar()
        def transform_psar(x):
            if x > 0: 
                return 1
            else:
                return -1
        new_df['PSAR'+prefix] = psar['PSARl_0.02_0.2'].apply(lambda x: transform_psar(x))
    except:
        new_df['PSAR'+prefix] = None
    
    return new_df

