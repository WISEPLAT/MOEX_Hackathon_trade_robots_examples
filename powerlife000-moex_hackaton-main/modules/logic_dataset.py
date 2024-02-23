#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Логический датасет
def logic_dataset(df, prefix = ':1d'):
    import pandas as pd
    import numpy as np
    
    #Построение логических конструкций на числовом датасете*
    
    new_df = pd.DataFrame()
    new_df.index = df.index

    #Получаем список колонок с EMA
    EMA_indicators = []
    for col in df.columns:
        if 'EMA' in col:
            EMA_indicators.append(col)

    #Расположение цены открытия, закрытия, максимума и минимума относительно ЕМА
    for EMA in EMA_indicators:
        #Положение всех точек бара относительно ЕМА
        #Расположение цены закрытия и открытия относительно друг друга
        #Инициализируем поле
        new_df['Close_'+EMA+prefix] = 0
        new_df['Open_'+EMA+prefix] = 0
        new_df['High_'+EMA+prefix] = 0
        new_df['Low_'+EMA+prefix] = 0
        new_df['All_points_'+EMA+prefix] = 0
        #Заполняем поле, формируем признак
        new_df['Close_'+EMA+prefix] = np.where(df['Close'] > df[EMA], 1, -1)
        new_df['Open_'+EMA+prefix] = np.where(df['Open'] > df[EMA], 1, -1)
        new_df['High_'+EMA+prefix] = np.where(df['High'] > df[EMA], 1, -1)
        new_df['Low_'+EMA+prefix] = np.where(df['Low'] > df[EMA], 1, -1)
        new_df['All_points_'+EMA+prefix] = np.where(
            (df['Close'] > df[EMA]) 
            & (df['Open'] > df[EMA]) 
            & (df['High'] > df[EMA])
            & (df['Low'] > df[EMA]),
            1, -1)
    
    #Веер ЕМА, пересечение МА
    for EMA_1 in EMA_indicators:
        for EMA_2 in EMA_indicators:
            #Инициализируем поле
            new_df[EMA_1+'_x_'+EMA_2+prefix] = 0
            #Заполняем поле, формируем признак
            new_df[EMA_1+'_x_'+EMA_2+prefix] = np.where(df[EMA_1] > df[EMA_2], 1, -1)
    
    #Веер ЕМА, Взаимное расположение соседних по периодам ЕМА
    last_EMA = None
    last_EMA_name = None
    temp_flag = False
    for EMA in EMA_indicators:
        if temp_flag:
            #Инициализируем поле
            new_df[last_EMA_name+'_||_'+EMA+prefix] = 0
            #Заполняем поле, формируем признак
            new_df[last_EMA_name+'_||_'+EMA+prefix] = np.where(last_EMA > df[EMA], 1, -1)
        
        last_EMA_name = EMA
        last_EMA = df[EMA]
        temp_flag = True
        
    #Касание котировкой уровня: раньше не касался бар по high и low, а теперь касается
        #Формирование поля касания баром ЕМА
    for EMA in EMA_indicators:
        #Инициализируем поле
        new_df['Touch_'+EMA+prefix] = 0
        #Заполняем поле, формируем признак
        new_df['Touch_'+EMA+prefix] = np.where(
            (df['High'] > df[EMA])
            & (df['Low'] < df[EMA]),
            1, -1)
        
        #Проверяем коснулась ли она только сейчас
        #Инициализируем поле
        new_df['New_touch_'+EMA+prefix] = 0
        #Заполняем поле, формируем признак
        new_df['New_touch_'+EMA+prefix] = np.where(
            (new_df['Touch_'+EMA+prefix] == 1)
            & (new_df['Touch_'+EMA+prefix].shift(1) == -1),
            1, -1)

    #Экстремумы
    #Предыдущая точка большей/меньше текущей и 2-х предыдущих
    def extr_min(x):
        current = x
        last_1 = x.shift(1)
        last_2 = x.shift(2)
        last_3 = x.shift(3)
        
        return np.where(
            (last_1 > current)
            & (last_1 > last_2)
            & (last_1 > last_3),
            1, 0)
    
    def extr_max(x):
        current = x
        last_1 = x.shift(1)
        last_2 = x.shift(2)
        last_3 = x.shift(3)
        
        return np.where(
            (last_1 < current)
            & (last_1 < last_2)
            & (last_1 < last_3),
            1, 0)
    #!!! АНАЛИЗ ЭКСТРЕМУМОВ ИНДИКАТОРОВ
    indicators = ['Open', 'High', 'Low', 'Close', 
       'EMA_3', 'EMA_5', 'EMA_8', 'EMA_9',
       'EMA_13', 'EMA_14', 'EMA_20', 'EMA_25', 'EMA_49',
       'EMA_50', 'EMA_89', 'EMA_100', 'EMA_150', 'EMA_200',
       'EMA_256', 'EMA_356','RSI_14', 'CCI_9', 
       'STOCHRSIk_14', 'STOCHk_14', 'STOCHd_14', 'STOCHk_50',
       'STOCHd_50', 'OBV', 'MACD_12_26_9', 'MACDh_12_26_9',
       'MACDs_12_26_9', 'AC', 'FI_14', 'BEARS_14']
    
    for col in indicators:
        try:
            if col in ['Open', 'High', 'Low', 'Close']:
                new_df['extr_max'+prefix] = extr_max(df[col])
                new_df['extr_min'+prefix] = extr_min(df[col])
            else:
                new_df['extr_max'+prefix] = extr_max(df[col+prefix])
                new_df['extr_min'+prefix] = extr_min(df[col+prefix])
        except:
            #print("Отсутствует колонка: ", col)
            pass
    
    #Текущая точка больше/меньше 3-х предыдущих
    def four_rise(x):
        current = x
        last_1 = x.shift(1)
        last_2 = x.shift(2)
        last_3 = x.shift(3)
        
        return np.where(
            (current > last_1)
            & (current > last_2)
            & (current > last_3),
            1, 0)
    
    def four_fall(x):
        current = x
        last_1 = x.shift(1)
        last_2 = x.shift(2)
        last_3 = x.shift(3)
        
        return np.where(
            (current < last_1)
            & (current < last_2)
            & (current < last_3),
            1, 0)
    #!!! АНАЛИЗ РОСТА И ПАДЕНИЯ ИНДИКАТОРОВ

    indicators = ['Open', 'High', 'Low', 'Close', 
       'EMA_3', 'EMA_5', 'EMA_8', 'EMA_9',
       'EMA_13', 'EMA_14', 'EMA_20', 'EMA_25', 'EMA_49',
       'EMA_50', 'EMA_89', 'EMA_100', 'EMA_150', 'EMA_200',
       'EMA_256', 'EMA_356','RSI_14', 'CCI_9', 
       'STOCHRSIk_14', 'STOCHk_14', 'STOCHd_14', 'STOCHk_50',
       'STOCHd_50', 'OBV', 'MACD_12_26_9', 'MACDh_12_26_9',
       'MACDs_12_26_9', 'AC', 'FI_14', 'BEARS_14']
    
    for col in indicators:
        try:
            if col in ['Open', 'High', 'Low', 'Close']:
                new_df['rise'+prefix] = four_rise(df[col])
                new_df['fall'+prefix] = four_fall(df[col])
            else:
                new_df['rise'+prefix] = four_rise(df[col+prefix])
                new_df['fall'+prefix] = four_fall(df[col+prefix])
        except:
            #print("Отсутствует колонка: ", col)
            pass

    #Касание границ каналов
    #Получаем список колонок с EMA
    channel_indicators = []
    for col in df.columns:
        if ('KC' in col) | ('BB' in col):
            channel_indicators.append(col)

    for channel in channel_indicators:

        temp_df = df.copy(deep = True).dropna(subset = channel)

        if temp_df.shape[0] != 0:

            #Создаём новый df для записи результатов
            temp_df_result = pd.DataFrame()
            temp_df_result.index = temp_df.index

            #Инициализируем поле
            temp_df_result['Touch_'+channel+prefix] = 0
            #Заполняем поле, формируем признак
            temp_df_result['Touch_'+channel+prefix] = np.where(
                (temp_df['High'] > temp_df[channel])
                & (temp_df['Low'] < temp_df[channel]),
                1, -1)

            new_df = new_df.join(temp_df_result)
    
    #Определение цены закрытия относительно границ и середины
    new_df['KC_20_10_3.2_UPPER'+'_upper'+prefix] = np.where(df['Close'] >= df['KC_20_10_3.2_UPPER'+prefix], 1, 0)
    new_df['KC_20_10_3.2_UPPER'+'_in'+prefix] = np.where(
        (df['Close'] < df['KC_20_10_3.2_UPPER'+prefix])
        & (df['Close'] > df['EMA_20'+prefix])
        , 1, 0)
    new_df['KC_20_10_3.2_LOWER'+'_in'+prefix] = np.where(
        (df['Close'] > df['KC_20_10_3.2_LOWER'+prefix])
        & (df['Close'] < df['EMA_20'+prefix])
        , 1, 0)
    new_df['KC_20_10_3.2_LOWER'+'_lower'+prefix] = np.where(df['Close'] <= df['KC_20_10_3.2_LOWER'+prefix], 1, 0)
    
    #
    new_df['KC_50_18_3.2_UPPER'+'_upper'+prefix] = np.where(df['Close'] >= df['KC_50_18_3.2_UPPER'+prefix], 1, 0)
    new_df['KC_50_18_3.2_UPPER'+'_in'+prefix] = np.where(
        (df['Close'] < df['KC_50_18_3.2_UPPER'+prefix])
        & (df['Close'] > df['EMA_50'+prefix])
        , 1, 0)
    new_df['KC_50_18_3.2_LOWER'+'_in'+prefix] = np.where(
        (df['Close'] > df['KC_50_18_3.2_LOWER'+prefix])
        & (df['Close'] < df['EMA_50'+prefix])
        , 1, 0)
    new_df['KC_50_18_3.2_LOWER'+'_lower'+prefix] = np.where(df['Close'] <= df['KC_50_18_3.2_LOWER'+prefix], 1, 0)
    
    #
    new_df['BBU_20_2.0'+'_upper'+prefix] = np.where(df['Close'] >= df['BBU_20_2.0'+prefix], 1, 0)
    new_df['BBU_20_2.0'+'_in'+prefix] = np.where(
        (df['Close'] < df['BBU_20_2.0'+prefix])
        & (df['Close'] > df['BBM_20_2.0'+prefix])
        , 1, 0)
    new_df['BBL_20_2.0'+'_in'+prefix] = np.where(
        (df['Close'] > df['BBL_20_2.0'+prefix])
        & (df['Close'] < df['BBM_20_2.0'+prefix])
        , 1, 0)
    new_df['BBL_20_2.0'+'_lower'+prefix] = np.where(df['Close'] <= df['BBL_20_2.0'+prefix], 1, 0)
    
    new_df['BBU_20_3.0'+'_upper'+prefix] = np.where(df['Close'] >= df['BBU_20_3.0'+prefix], 1, 0)
    new_df['BBU_20_3.0'+'_in'+prefix] = np.where(
        (df['Close'] < df['BBU_20_3.0'+prefix])
        & (df['Close'] > df['BBU_20_3.0'+prefix])
        , 1, 0)
    new_df['BBU_20_3.0'+'_in'+prefix] = np.where(
        (df['Close'] > df['BBU_20_3.0'+prefix])
        & (df['Close'] < df['BBU_20_3.0'+prefix])
        , 1, 0)
    new_df['BBU_20_3.0'+'_lower'+prefix] = np.where(df['Close'] <= df['BBU_20_3.0'+prefix], 1, 0)
    
    #
    new_df['BBU_50_2.0'+'_upper'+prefix] = np.where(df['Close'] >= df['BBU_50_2.0'+prefix], 1, 0)
    new_df['BBU_50_2.0'+'_in'+prefix] = np.where(
        (df['Close'] < df['BBU_50_2.0'+prefix])
        & (df['Close'] > df['BBU_50_2.0'+prefix])
        , 1, 0)
    new_df['BBU_50_2.0'+'_in'+prefix] = np.where(
        (df['Close'] > df['BBU_50_2.0'+prefix])
        & (df['Close'] < df['BBU_50_2.0'+prefix])
        , 1, 0)
    new_df['BBU_50_2.0'+'_lower'+prefix] = np.where(df['Close'] <= df['BBU_50_2.0'+prefix], 1, 0)
    
    #
    new_df['BBU_50_3.0'+'_upper'+prefix] = np.where(df['Close'] >= df['BBU_50_3.0'+prefix], 1, 0)
    new_df['BBU_50_3.0'+'_in'+prefix] = np.where(
        (df['Close'] < df['BBU_50_3.0'+prefix])
        & (df['Close'] > df['BBU_50_3.0'+prefix])
        , 1, 0)
    new_df['BBU_50_3.0'+'_in'+prefix] = np.where(
        (df['Close'] > df['BBU_50_3.0'+prefix])
        & (df['Close'] < df['BBU_50_3.0'+prefix])
        , 1, 0)
    new_df['BBU_50_3.0'+'_lower'+prefix] = np.where(df['Close'] <= df['BBU_50_3.0'+prefix], 1, 0)
    
    #(Положение относительно канала: хотя бы частично в канале 1; иначе 0)
    
    new_df['KC_20_10_3.2_UPPER'+'_in'+prefix] = np.where(
        (
            (df['Close'] < df['KC_20_10_3.2_UPPER'+prefix])
            | (df['Open'] < df['KC_20_10_3.2_UPPER'+prefix])
            | (df['High'] < df['KC_20_10_3.2_UPPER'+prefix])
            | (df['Low'] < df['KC_20_10_3.2_UPPER'+prefix])
        )
        & (
            (df['Close'] > df['EMA_20'+prefix])
            | (df['Open'] > df['EMA_20'+prefix])
            | (df['High'] > df['EMA_20'+prefix])
            | (df['Low'] > df['EMA_20'+prefix])
        )
        , 1, 0)
    new_df['KC_20_10_3.2_LOWER'+'_in'+prefix] = np.where(
        (
            (df['Close'] > df['KC_20_10_3.2_LOWER'+prefix])
            | (df['Open'] > df['KC_20_10_3.2_LOWER'+prefix])
            | (df['High'] > df['KC_20_10_3.2_LOWER'+prefix])
            | (df['Low'] > df['KC_20_10_3.2_LOWER'+prefix])
        )
        & (
            (df['Close'] < df['EMA_20'+prefix])
            | (df['Open'] < df['EMA_20'+prefix])
            | (df['High'] < df['EMA_20'+prefix])
            | (df['Low'] < df['EMA_20'+prefix])
        )
        , 1, 0)
    
    new_df['KC_50_18_3.2_UPPER'+'_in'+prefix] = np.where(
        (
            (df['Close'] < df['KC_50_18_3.2_UPPER'+prefix])
            | (df['Open'] < df['KC_50_18_3.2_UPPER'+prefix])
            | (df['High'] < df['KC_50_18_3.2_UPPER'+prefix])
            | (df['Low'] < df['KC_50_18_3.2_UPPER'+prefix])
        )
        & (
            (df['Close'] > df['EMA_50'+prefix])
            | (df['Open'] > df['EMA_50'+prefix])
            | (df['High'] > df['EMA_50'+prefix])
            | (df['Low'] > df['EMA_50'+prefix])
        )
        , 1, 0)
    new_df['KC_50_18_3.2_LOWER'+'_in'+prefix] = np.where(
        (
            (df['Close'] > df['KC_50_18_3.2_LOWER'+prefix])
            | (df['Open'] > df['KC_50_18_3.2_LOWER'+prefix])
            | (df['High'] > df['KC_50_18_3.2_LOWER'+prefix])
            | (df['Low'] > df['KC_50_18_3.2_LOWER'+prefix])
        )
        & (
            (df['Close'] < df['EMA_50'+prefix])
            | (df['Open'] < df['EMA_50'+prefix])
            | (df['High'] < df['EMA_50'+prefix])
            | (df['Low'] < df['EMA_50'+prefix])
        )
        , 1, 0)
    
    new_df['BBU_20_2.0'+'_in'+prefix] = np.where(
        (
            (df['Close'] < df['BBU_20_2.0'+prefix])
            | (df['Open'] < df['BBU_20_2.0'+prefix])
            | (df['High'] < df['BBU_20_2.0'+prefix])
            | (df['Low'] < df['BBU_20_2.0'+prefix])
        )
        & (
            (df['Close'] > df['BBM_20_2.0'+prefix])
            | (df['Open'] > df['BBM_20_2.0'+prefix])
            | (df['High'] > df['BBM_20_2.0'+prefix])
            | (df['Low'] > df['BBM_20_2.0'+prefix])
        )
        , 1, 0)
        
    new_df['BBL_20_2.0'+'_in'+prefix] = np.where(
        (
            (df['Close'] > df['BBL_20_2.0'+prefix])
            | (df['Open'] > df['BBL_20_2.0'+prefix])
            | (df['High'] > df['BBL_20_2.0'+prefix])
            | (df['Low'] > df['BBL_20_2.0'+prefix])
        )
        & (
            (df['Close'] < df['BBM_20_2.0'+prefix])
            | (df['Open'] < df['BBM_20_2.0'+prefix])
            | (df['High'] < df['BBM_20_2.0'+prefix])
            | (df['Low'] < df['BBM_20_2.0'+prefix])
        )
        , 1, 0)
    
    new_df['BBU_20_3.0'+'_in'+prefix] = np.where(
        (
            (df['Close'] < df['BBU_20_3.0'+prefix])
            | (df['Open'] < df['BBU_20_3.0'+prefix])
            | (df['High'] < df['BBU_20_3.0'+prefix])
            | (df['Low'] < df['BBU_20_3.0'+prefix])
        )
        & (
            (df['Close'] > df['BBM_20_3.0'+prefix])
            | (df['Open'] > df['BBM_20_3.0'+prefix])
            | (df['High'] > df['BBM_20_3.0'+prefix])
            | (df['Low'] > df['BBM_20_3.0'+prefix])
        )
        , 1, 0)
    new_df['BBL_20_3.0'+'_in'+prefix] = np.where(
        (
            (df['Close'] > df['BBL_20_3.0'+prefix])
            | (df['Open'] > df['BBL_20_3.0'+prefix])
            | (df['High'] > df['BBL_20_3.0'+prefix])
            | (df['Low'] > df['BBL_20_3.0'+prefix])
        )
        & (
            (df['Close'] < df['BBM_20_3.0'+prefix])
            | (df['Open'] < df['BBM_20_3.0'+prefix])
            | (df['High'] < df['BBM_20_3.0'+prefix])
            | (df['Low'] < df['BBM_20_3.0'+prefix])
        )
        , 1, 0)
    
    new_df['BBU_50_2.0'+'_in'+prefix] = np.where(
        (
            (df['Close'] < df['BBU_50_2.0'+prefix])
            | (df['Open'] < df['BBU_50_2.0'+prefix])
            | (df['High'] < df['BBU_50_2.0'+prefix])
            | (df['Low'] < df['BBU_50_2.0'+prefix])
        )
        & (
            (df['Close'] > df['BBM_50_2.0'+prefix])
            | (df['Open'] > df['BBM_50_2.0'+prefix])
            | (df['High'] > df['BBM_50_2.0'+prefix])
            | (df['Low'] > df['BBM_50_2.0'+prefix])
        )
        , 1, 0)
    new_df['BBL_50_2.0'+'_in'+prefix] = np.where(
        (
            (df['Close'] > df['BBL_50_2.0'+prefix])
            | (df['Open'] > df['BBL_50_2.0'+prefix])
            | (df['High'] > df['BBL_50_2.0'+prefix])
            | (df['Low'] > df['BBL_50_2.0'+prefix])
        )
        & (
            (df['Close'] < df['BBM_50_2.0'+prefix])
            | (df['Open'] < df['BBM_50_2.0'+prefix])
            | (df['High'] < df['BBM_50_2.0'+prefix])
            | (df['Low'] < df['BBM_50_2.0'+prefix])
        )
        , 1, 0)
    
    new_df['BBU_50_3.0'+'_in'+prefix] = np.where(
        (
            (df['Close'] < df['BBU_50_3.0'+prefix])
            | (df['Open'] < df['BBU_50_3.0'+prefix])
            | (df['High'] < df['BBU_50_3.0'+prefix])
            | (df['Low'] < df['BBU_50_3.0'+prefix])
        )
        & (
            (df['Close'] > df['BBM_50_3.0'+prefix])
            | (df['Open'] > df['BBM_50_3.0'+prefix])
            | (df['High'] > df['BBM_50_3.0'+prefix])
            | (df['Low'] > df['BBM_50_3.0'+prefix])
        )
        , 1, 0)
    new_df['BBU_50_3.0'+'_in'+prefix] = np.where(
        (
            (df['Close'] > df['BBL_50_3.0'+prefix])
            | (df['Open'] > df['BBL_50_3.0'+prefix])
            | (df['High'] > df['BBL_50_3.0'+prefix])
            | (df['Low'] > df['BBL_50_3.0'+prefix])
        )
        & (
            (df['Close'] < df['BBM_50_3.0'+prefix])
            | (df['Open'] < df['BBM_50_3.0'+prefix])
            | (df['High'] < df['BBM_50_3.0'+prefix])
            | (df['Low'] < df['BBM_50_3.0'+prefix])
        )
        , 1, 0)
    

    #Направления тренда индикаторов по предыдущему бару
    indicators = ['Open', 'High', 'Low', 'Close', 
       'EMA_3', 'EMA_5', 'EMA_8', 'EMA_9',
       'EMA_13', 'EMA_14', 'EMA_20', 'EMA_25', 'EMA_49',
       'EMA_50', 'EMA_89', 'EMA_100', 'EMA_150', 'EMA_200',
       'EMA_256', 'EMA_356','RSI_14', 'CCI_9', 
       'STOCHRSIk_14', 'STOCHk_14', 'STOCHd_14', 'STOCHk_50',
       'STOCHd_50', 'OBV', 'MACD_12_26_9', 'MACDh_12_26_9',
       'MACDs_12_26_9', 'AC', 'FI_14', 'BEARS_14']
    
    def last_rise(x):
        current = x
        last_1 = x.shift(1)
        
        return np.where(
            current > last_1,
            1, -1)
    
    for col in indicators:
        try:
            if col in ['Open', 'High', 'Low', 'Close']:
                new_df['last_rise'+prefix] = last_rise(df[col])
            else:
                new_df['last_rise'+prefix] = last_rise(df[col+prefix])
        except:
            #print("Отсутствует колонка: ", col)
            pass
    
    
    #Сила тренда:
    #AC > 0
    new_df['AC'+'_to_0'+prefix] = np.where(df['AC'+prefix] > 0, 1, -1)
    
    #AC рост?
    temp = df['AC'+prefix].shift(1)
    temp = temp.fillna(0)
    new_df['AC'+'_rise'+prefix] = np.where(df['AC'+prefix] > temp, 1, -1)
    
    #Fi > 0?
    new_df['FI_14'+'_to_0'+prefix] = np.where(df['FI_14'+prefix] > 0, 1, -1)
    
    #Fi рост?
    temp = df['FI_14'+prefix].shift(1)
    temp = temp.fillna(0)
    new_df['FI_14'+'_rise'+prefix] = np.where(df['FI_14'+prefix] > temp, 1, -1)
    
    #Bears > 0, рост?
    new_df['BEARS_14'+'_to_0'+prefix] = np.where(df['BEARS_14'+prefix] > 0, 1, -1)

    #Котировки 
    #Текущая цена закрытия больше предыдущего минимума??
    #Текущая цена закрытия больше предыдущей цены закрытия??

    #Положение относительно уровней осцилляторов (другой датасет stoch_logic)

    #Гэпы по low, high относительно предыдущего бара, анализ ряда в %: 0.5, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 40
    gaps = [0.5, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 40]
    
    temp_shift = df[['High','Low']].shift(1)
    temp_shift = temp_shift.fillna(method = 'bfill')

    abs((temp_shift['High'] - df['Low'])/temp_shift['High'])

    for gap in gaps:

        temp_gap = pd.DataFrame()
        temp_gap['gap_1'] = abs((temp_shift['Low'] - df['High'])/temp_shift['Low'])
        temp_gap['gap_2'] = abs((temp_shift['High'] - df['Low'])/temp_shift['High'])

        new_df['gap_'+str(gap)+prefix] = np.where(
            (
                (temp_shift['Low'] > df['High']) | 
                (temp_shift['High'] < df['Low'])
            ) &
            (
                temp_gap[['gap_1','gap_2']].min(axis=1) >= gap/100
            ),
            1, 0)

    return new_df

