#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def start(dataset):
    #экстремумы по 20 точкам
    
    #Число точек, относительно по которым ищутся экстремумы
    count_points = 20
    #count_points = 30
    #count_points = 45
    
    dataset['extr'] = None
    
    #Инициализируем переменные
    new_min = 10000000;
    new_max = 0;

    find_first = False;

    count_extr = 0;
    current_top_number = 0;
    current_bot_number = 0;

    extrems = []
    last_extr = None;
    last_extr_i = 0;
    
    
    
    min = []
    max = []
    
    for i in range(count_points+1):
        min.append(0)
        max.append(0)   

    
    i_filter = 1; #Фильтр близости предыдущего экстремума. Он должен быть дальше чем 1 день
    
    print("Общее число данных графика для обработки: ", dataset.shape[0])
    
    quote_count = 0;
    
    for i, quote in dataset.iterrows():
        
        if quote_count+count_points >= dataset.shape[0]:
            break
            
        for j in range(count_points+1):
            
            if dataset.iloc[quote_count+j].Open > dataset.iloc[quote_count+j].Close:
                max[j] = dataset.iloc[quote_count+j].Open;
                min[j] = dataset.iloc[quote_count+j].Close;
            else:
                max[j] = dataset.iloc[quote_count+j].Close;
                min[j] = dataset.iloc[quote_count+j].Open;
            
        if find_first == False: #Ищем первую точку
            
            logic_max = True
            for j in range(1, count_points+1):
                logic_max = logic_max & (max[0] > max[j])
            
            if logic_max:
                find_first = True;#Первый максимум найден

                new_min = max[0];
                dataset.at[i, 'extr'] = 'max'
                extrems.append([quote,quote_count,'max'])
                last_extr = 'max'

            
            logic_min = True
            for j in range(1, count_points+1):
                logic_min = logic_min & (min[0] < min[j])
                
            if logic_min:
                find_first = True;#Первый минимум найден

                new_max = min[0];
                dataset.at[i, 'extr'] = 'min'
                extrems.append([quote,quote_count,'min'])
                last_extr = 'min'
        
        else: #Ищем остальные точки
            
            if last_extr == 'min':
                
                if dataset.iloc[quote_count].High > new_max:
                    new_max = max[0];
                    
                    logic_max = True
                    for j in range(1, count_points+1):
                        logic_max = logic_max & (max[0] > max[j])
                    
                    if logic_max:
                        find_first = True;#Максимум найден
                        
                        new_min = max[0]
                        dataset.at[i, 'extr'] = 'max'
                        extrems.append([quote,'max'])
                        last_extr = 'max'                        
            
            elif last_extr == 'max':
                
                if dataset.iloc[quote_count].Low < new_min:
                    new_min = min[0]
                    
                    logic_min = True
                    for j in range(1, count_points+1):
                        logic_min = logic_min & (min[0] < min[j])

                    if logic_min:
                        find_first = True;#Минимум найден

                        new_max = min[0];
                        dataset.at[i, 'extr'] = 'min'
                        extrems.append([quote,'min'])
                        last_extr = 'min'
        
        quote_count = quote_count+1
        
    return dataset

