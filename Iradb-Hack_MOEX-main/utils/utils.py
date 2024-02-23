import pandas as pd
import datetime
from catboost import CatBoostRegressor, Pool
import time
from moexalgo import Market, Ticker
from sklearn.metrics import mean_absolute_percentage_error

class Data(): # Создаем класс для подгрузки данных с API MOEX
    def __init__(self):
        self.data = pd.DataFrame()
        self.data_rate = pd.DataFrame()
        self.dict_name = {}
    def load_data(self):
        self.data = pd.read_csv("Data/tradestats.csv")
        self.data_ticket = pd.read_csv("Data/tickers.csv",sep=',')
        self.data_rate = pd.read_csv("Data/rates.csv",encoding='cp1251',sep=';',header=1)
    def load_data_columns(self,columns_pd,column):
        return self.data[self.data[f"{columns_pd}"]==column]
    def take_uniq_val(self,columns_pd):
        data_ret = self.data[columns_pd].unique()
        for i in data_ret:
            self.dict_name[i] = self.data_rate[self.data_rate["SECID"] == i]["NAME"].values[0]
        return 
    def load_data_from_url(self,ticker,date,type): # Функция для вывода данных на центральный график, Обзор или Свечной анализ
        tradestats = pd.DataFrame()
        back_date = datetime.datetime.now()- datetime.timedelta(days=3)
        now_date = datetime.datetime.now().date()
        stock = Ticker(ticker)
        if type in ["Svecha","Obzor"]:
            tradestats = stock.tradestats(date=str(now_date))
            tradestats = pd.DataFrame(tradestats)
        elif type in ["Stakan"]:
            tradestats = stock.orderstats(date=str(now_date))
            tradestats = pd.DataFrame(tradestats)
        tradestats["ts"] = pd.to_datetime(tradestats["ts"])
        tradestats.rename(columns={"ts":"tradedate"},inplace=True)
        tradestats["tradetime"] = [str(i).split(" ")[1] for i in tradestats["tradedate"]]
        tradestats = tradestats.sort_values(by=["tradetime"],ascending=False)
        return tradestats
       
    
class ML(): # Класс для ML модели с преподготовкой данных и предсказанием
    def __init__(self) -> None:
        self.model = CatBoostRegressor() # Инициализируем модель
        self.model.load_model('assets/catboost_model_timesplit.bin') # подгружаем модель
        self.max_min = pd.read_csv('assets/tickets_maxmin.csv',sep=';', index_col=None)
        self.stocks = Market('stocks')
        self.columns_to_train=[  'ticker',  'vol', 'trades',
       'trades_b', 'trades_s', 'vol_b', 'vol_s',
       'Normpr_open', 'Normpr_high', 'Normpr_low', 'Normpr_close', 'val','pr_std', 
       'pr_change', 'val_b', 'val_s', 'disb', 'Normpr_vwap', 'Normpr_vwap_b', 'Normpr_vwap_s',
        'dayofweek', 'quarter', 'month', 'year', 'dayofyear',
       'dayofmonth', 'weekofyear', 'hour', 'minute']
        self.data_rate = pd.read_csv("Data/rates.csv",encoding='cp1251',sep=';',header=1)
        self.data_ticket = pd.read_csv("Data/tickers.csv",sep=',')
    def prepare(self): # Преподготовка данных
        date = datetime.datetime.now().date()
        print(date-datetime.timedelta(days=2))
        test=self.stocks.tradestats(date=str(date-datetime.timedelta(days=3)))
        test = pd.DataFrame(test)
        # print(test.head(10))
        test.rename(columns={"secid":"ticker","ts":"TimeValue"},inplace=True)
        test["tradetime"] = [str(i).split(" ")[1] for i in test["TimeValue"]]
        val=self.stocks.tradestats(date=str(date-datetime.timedelta(days=2)))
        val = pd.DataFrame(val)
        val.rename(columns={"secid":"ticker","ts":"TimeValue"},inplace=True)
        val["tradetime"] = [str(i).split(" ")[1] for i in val["TimeValue"]]
        test = test.merge(self.max_min,how="left",on='ticker')
        val = val.merge(self.max_min,how="left",on='ticker')
        test,val = self.prepare_date(test,val)
        test,val = self.Normalize(test,val)
        test = test.fillna(0)
        val = val.fillna(0)
        test_all = test
        test = test[self.columns_to_train]
        return test,val,test_all

    def Normalize(self,test,val):
        # Нормализация данных 'Normpr_open', 'Normpr_high', 'Normpr_low', 'Normpr_close',  'Normpr_vwap', 'Normpr_vwap_b', 'Normpr_vwap_s'
        test['Normpr_open']=(test['pr_open']-test['pr_close_Min'])/(test['pr_close_Max']-test['pr_close_Min'])
        test['Normpr_high']=(test['pr_high']-test['pr_close_Min'])/(test['pr_close_Max']-test['pr_close_Min'])
        test['Normpr_low']=(test['pr_low']-test['pr_close_Min'])/(test['pr_close_Max']-test['pr_close_Min'])
        test['Normpr_close']=(test['pr_open']-test['pr_close_Min'])/(test['pr_close_Max']-test['pr_close_Min'])
        test['Normpr_vwap']=(test['pr_close']-test['pr_close_Min'])/(test['pr_close_Max']-test['pr_close_Min'])
        test['Normpr_vwap_b']=(test['pr_vwap_b']-test['pr_close_Min'])/(test['pr_close_Max']-test['pr_close_Min'])
        test['Normpr_vwap_s']=(test['pr_vwap_s']-test['pr_close_Min'])/(test['pr_close_Max']-test['pr_close_Min'])

        val['Normpr_open']=(val['pr_open']-val['pr_close_Min'])/(val['pr_close_Max']-val['pr_close_Min'])
        val['Normpr_high']=(val['pr_high']-val['pr_close_Min'])/(val['pr_close_Max']-val['pr_close_Min'])
        val['Normpr_low']=(val['pr_low']-val['pr_close_Min'])/(val['pr_close_Max']-val['pr_close_Min'])
        val['Normpr_close']=(val['pr_open']-val['pr_close_Min'])/(val['pr_close_Max']-val['pr_close_Min'])
        val['Normpr_vwap']=(val['pr_close']-val['pr_close_Min'])/(val['pr_close_Max']-val['pr_close_Min'])
        val['Normpr_vwap_b']=(val['pr_vwap_b']-val['pr_close_Min'])/(val['pr_close_Max']-val['pr_close_Min'])
        val['Normpr_vwap_s']=(val['pr_vwap_s']-val['pr_close_Min'])/(val['pr_close_Max']-val['pr_close_Min'])
        return test,val

    def prepare_date(self,test,val):

        test['TimeValue'] = pd.to_datetime(test['TimeValue'])
        val['TimeValue'] = pd.to_datetime(val['TimeValue'])

                # создание полей времени
        test['dayofweek'] = test['TimeValue'].dt.dayofweek
        test['quarter'] = test['TimeValue'].dt.quarter
        test['month'] = test['TimeValue'].dt.month
        test['year'] = test['TimeValue'].dt.year
        test['dayofyear'] = test['TimeValue'].dt.dayofyear
        test['dayofmonth'] = test['TimeValue'].dt.day
        test['weekofyear'] = test['TimeValue'].dt.isocalendar().week
        test['hour'] = test['TimeValue'].dt.hour
        test['minute'] = test['TimeValue'].dt.minute

        val['dayofweek'] = val['TimeValue'].dt.dayofweek
        val['quarter'] = val['TimeValue'].dt.quarter
        val['month'] = val['TimeValue'].dt.month
        val['year'] = val['TimeValue'].dt.year
        val['dayofyear'] = val['TimeValue'].dt.dayofyear
        val['dayofmonth'] = val['TimeValue'].dt.day
        val['weekofyear'] = val['TimeValue'].dt.isocalendar().week
        val['hour'] = val['TimeValue'].dt.hour
        val['minute'] = val['TimeValue'].dt.minute

        return test,val
    def predict(self): # Предсказание модели, данные будем хранить в памяти 
        test,val,test_all = self.prepare()
        y_pred = self.model.predict(test)
        test_all["PrognozVal"]=y_pred
        test = test_all[['ticker','tradetime','PrognozVal']]
        val=val.merge(test, how='left',on=['ticker','tradetime'])
        val = val[val['PrognozVal'].notna()]
        # Теперь вернем цены из нормализации
        self.val = val
        self.val['PrognozValAbs']=val['PrognozVal']*(val['pr_close_Max']-val['pr_close_Min'])+val['pr_close_Min']
        val_all=val[self.columns_to_train]
        y_prog=self.model.predict(val_all)
        self.val['PrognozNew']=y_prog
        self.val['PrognozNewAbs']=val['PrognozNew']*(val['pr_close_Max']-val['pr_close_Min'])+val['pr_close_Min']
        self.update_sort_val()
    def show(self,Ticker): # Вывод данных на графики рекомендателой системы
        val_tik=self.val.loc[self.val['ticker']==Ticker]
        loss_data_val = mean_absolute_percentage_error(val_tik['pr_close'],val_tik['PrognozValAbs'])
        max_min_val = val_tik["PrognozNewAbs"].max(),val_tik["PrognozNewAbs"].min()
        sum_benefit = ((val_tik['PrognozNewAbs'].max()/val_tik['PrognozNewAbs'].min())-1)*100
        return val_tik,loss_data_val,round(max_min_val[0],2),round(max_min_val[1],2),round(sum_benefit,2)
    
    def update_sort_val(self): # Функция подгрузки наименования тикетов
        self.PD_sorted = pd.DataFrame(columns=["tickers","name","mape","benefits"])
        for Tickers in self.val['ticker'].unique():
            val = self.val[self.val['ticker']==Tickers]
            mape_v = mean_absolute_percentage_error(self.val[self.val['ticker']==Tickers]["PrognozValAbs"],self.val[self.val['ticker']==Tickers]["pr_close"])
            name = self.data_rate[self.data_rate["SECID"] == Tickers]["NAME"].values[0]
            benefits = ((val['PrognozNewAbs'].max()/val['PrognozNewAbs'].min())-1)*100
            pd_add = pd.DataFrame([{"tickers":Tickers,"name":name,"mape":mape_v,"benefits":benefits}])
            self.PD_sorted = pd.concat([self.PD_sorted,pd_add])
        




