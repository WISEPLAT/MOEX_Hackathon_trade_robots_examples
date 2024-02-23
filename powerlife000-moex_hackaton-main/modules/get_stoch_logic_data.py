#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Построение логических конструкцих на датасете стохастика
def get_stoch_logic_data(df, prefix = ':1d'):
    
    import pandas as pd
    import numpy as np
    
    new_df = pd.DataFrame()
    new_df.index = df.index
    
    #Получаем смещенный датасет
    df_shift = df.copy(deep = True).shift(1)
    
    #Получаем список колонок 
    STOCHk_arr = []
    STOCHd_arr = []
    indicators = []
    for col in df.columns:
        if 'STOCHk' in col:
            STOCHk_arr.append(col)
            indicators.append(col.split(':')[0])
        elif 'STOCHd' in col:
            STOCHd_arr.append(col)
            
    indicators = np.array(indicators).tolist()
            
    #Рост или падение по отношению к предыдущему бару
    def check_rise(x, y):
        if x > y:
            return 1
        elif x < y:
            return -1
        else:
            return 0
    
    #Все индикаторы
    all_arr = STOCHk_arr+STOCHd_arr
    
    for indicator in all_arr:
        #Рост или падение по отношению к предыдущему бару
        #Инициализируем поле
        new_df[indicator+':check_rise'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_rise'] = np.where(df[indicator] > df_shift[indicator], 1, new_df[indicator+':check_rise'])
        new_df[indicator+':check_rise'] = np.where(df[indicator] < df_shift[indicator], -1, new_df[indicator+':check_rise'])
        new_df[indicator+':check_rise'] = np.where(df[indicator] == df_shift[indicator], 0, new_df[indicator+':check_rise'])
        new_df[indicator+':check_rise'] = np.where(df_shift[indicator].isna(), 0, new_df[indicator+':check_rise'])
        new_df[indicator+':check_rise'] = np.where(df[indicator].isna(), 0, new_df[indicator+':check_rise'])
    
        #Расположение в уровне
        #Инициализируем поле
        #new_df[indicator+':check_0'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_0'] = np.where(df[indicator] == 0, 1, 0)
        
        #Инициализируем поле
        #new_df[indicator+':check_0_0.1'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_0_0.1'] = np.where((df[indicator] > 0) & (df[indicator] <= 0.1) , 1, 0)
        
        #Инициализируем поле
        #new_df[indicator+':check_0.1_0.2'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_0.1_0.2'] = np.where((df[indicator] > 0.1) & (df[indicator] <= 0.2) , 1, 0)
        
        #Инициализируем поле
        #new_df[indicator+':check_0.2_0.3'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_0.2_0.3'] = np.where((df[indicator] > 0.2) & (df[indicator] <= 0.3) , 1, 0)
        
        #Инициализируем поле
        #new_df[indicator+':check_0.3_0.4'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_0.3_0.4'] = np.where((df[indicator] > 0.3) & (df[indicator] <= 0.4) , 1, 0)
        
        #Инициализируем поле
        #new_df[indicator+':check_0.4_0.5'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_0.4_0.5'] = np.where((df[indicator] > 0.4) & (df[indicator] <= 0.5) , 1, 0)
        
        #Инициализируем поле
        #new_df[indicator+':check_0.5_0.6'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_0.5_0.6'] = np.where((df[indicator] > 0.5) & (df[indicator] <= 0.6) , 1, 0)
        
        #Инициализируем поле
        #new_df[indicator+':check_0.6_0.7'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_0.6_0.7'] = np.where((df[indicator] > 0.6) & (df[indicator] <= 0.7) , 1, 0)
        
        #Инициализируем поле
        #new_df[indicator+':check_0.7_0.8'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_0.7_0.8'] = np.where((df[indicator] > 0.7) & (df[indicator] <= 0.8) , 1, 0)
        
        #Инициализируем поле
        #new_df[indicator+':check_0.8_0.9'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_0.8_0.9'] = np.where((df[indicator] > 0.8) & (df[indicator] <= 0.9) , 1, 0)
        
        #Инициализируем поле
        #new_df[indicator+':check_0.9_1.0'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_0.9_1.0'] = np.where((df[indicator] > 0.9) & (df[indicator] < 1) , 1, 0)
        
        #Инициализируем поле
        #new_df[indicator+':check_1'] = 0
        #Заполняем поле, формируем признак
        new_df[indicator+':check_1'] = np.where(df[indicator] == 1, 1, 0)
    
    #Переход с одного уровня на другой по отношению к предыдущему бару
    #НЕ ФОРМРУЕМ ПРИЗНАК, ТАК КАК ПРИ ФОРМРОВАНИИ ЛАГОВЫХ ПРИЗНАКОВ ЭТО БУДЕТ СФОРМИРОВАНО АВТОМАТИЧЕСКИ
    
    #Отношение k к d (что выше)
    for indicator in indicators:
        
        if (indicator == 'Low') &(indicator == 'High') & (indicator == 'Open') & (indicator == 'Close'):
            for i in [3,5,7,9,14,20,50]:
                k = i
                d = 3
                #Инициализируем поле
                new_df[indicator+str(i)+':STOCHk_to_STOCHd'] = 0
                #Заполняем поле, формируем признак
                new_df[indicator+str(i)+':STOCHk_to_STOCHd'] = np.where(df[indicator+':STOCHk'+':'+str(k)+':'+str(d)+prefix] > df[indicator+':STOCHd'+':'+str(k)+':'+str(d)+prefix] , 1, new_df[indicator+str(i)+':STOCHk_to_STOCHd'])
                new_df[indicator+str(i)+':STOCHk_to_STOCHd'] = np.where(df[indicator+':STOCHk'+':'+str(k)+':'+str(d)+prefix] < df[indicator+':STOCHd'+':'+str(k)+':'+str(d)+prefix] , -1, new_df[indicator+str(i)+':STOCHk_to_STOCHd'])

        
        if (indicator != 'Low') &(indicator != 'High') & (indicator != 'Open') & (indicator != 'Close') & (indicator != 'STOCHk_14') & (indicator != 'STOCHd_14') & (indicator != 'STOCHk_50') & (indicator != 'STOCHd_50'):
            #Инициализируем поле
            new_df[indicator+':STOCHk_to_STOCHd'] = 0
            #Заполняем поле, формируем признак
            new_df[indicator+':STOCHk_to_STOCHd'] = np.where(df[indicator+':STOCHk'+prefix] > df[indicator+':STOCHd'+prefix] , 1, new_df[indicator+':STOCHk_to_STOCHd'])
            new_df[indicator+':STOCHk_to_STOCHd'] = np.where(df[indicator+':STOCHk'+prefix] < df[indicator+':STOCHd'+prefix] , -1, new_df[indicator+':STOCHk_to_STOCHd'])
    
    #Инициализируем поле
    new_df['STOCHk_14'+':STOCHk_to_STOCHd'] = 0
    new_df['STOCHk_14'+':STOCHk_to_STOCHd'] = np.where(df['STOCHk_14:STOCHk'+prefix] > df['STOCHd_14:STOCHd'+prefix] , 1, new_df['STOCHk_14'+':STOCHk_to_STOCHd'])
    new_df['STOCHk_14'+':STOCHk_to_STOCHd'] = np.where(df['STOCHk_14:STOCHk'+prefix] < df['STOCHd_14:STOCHd'+prefix] , -1, new_df['STOCHk_14'+':STOCHk_to_STOCHd'])
    
    #Инициализируем поле
    new_df['STOCHk_50'+':STOCHk_to_STOCHd'] = 0
    new_df['STOCHk_50'+':STOCHk_to_STOCHd'] = np.where(df['STOCHk_50:STOCHk'+prefix] > df['STOCHd_50:STOCHd'+prefix] , 1, new_df['STOCHk_50'+':STOCHk_to_STOCHd'])
    new_df['STOCHk_50'+':STOCHk_to_STOCHd'] = np.where(df['STOCHk_50:STOCHk'+prefix] < df['STOCHd_50:STOCHd'+prefix] , -1, new_df['STOCHk_50'+':STOCHk_to_STOCHd'])
    
    new_df['PSAR'+prefix] = df['PSAR'+prefix]
        
    return new_df

