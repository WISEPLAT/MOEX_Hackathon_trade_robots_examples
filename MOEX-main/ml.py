import pandas as pd
from xgboost import XGBRegressor
import time


def gen_dates(start_date, finish_date):
    year_a = int(start_date.split('-')[0])
    month_a = int(start_date.split('-')[1])
    day_a = int(start_date.split('-')[2])
    year_b = int(finish_date.split('-')[0])
    month_b = int(finish_date.split('-')[1])
    day_b = int(finish_date.split('-')[2])
    dates = []
    days = [31, 28, 31,
            30, 31, 30,
            31, 31, 30,
            31, 30, 31]
    for month in range(month_a, month_b + 12 * (year_b - year_a) + 1):
        year = year_a + (month - 1) // 12
        days[1] = 28 + (year % 4 == 0)
        for day in range(day_a, days[month % 12 - 1] + 1):
            dates.append(f'{year}-{((month - 1) % 12 + 1):02d}-{day:02d}')
        day_a = 1
    return dates


class Algo:
    def __init__(self,
                 models_size='M',
                 features_dict_size='M',
                 ):
        if models_size == 'S':
            self.models = {
                'Gradient Boosting': XGBRegressor(max_depth=4,
                                                  n_estimators=10000),
            }
        elif models_size == 'M':
            self.models = {
                'Gradient Boosting': XGBRegressor(max_depth=4,
                                                  n_estimators=20000),
            }
        elif models_size == 'L':
            self.models = {
                'Gradient Boosting': XGBRegressor(max_depth=4,
                                                  n_estimators=35000),
            }
        elif models_size == 'XL':
            self.models = {
                'Gradient Boosting': XGBRegressor(max_depth=4,
                                                  n_estimators=50000),
            }
        self.features_dict_size = features_dict_size
        self.feats_transforms = {
            'S': ['lag'],
            'M': ['lag', 'avg'],
            'L': ['lag', 'avg', 'cum_sum']
        }

    def get_data(self, dates, train_size=0.8):
        tradestats = pd.DataFrame()
        for date in dates:
            for cursor in range(1):
                url = f'https://iss.moex.com/iss/datashop/algopack/eq/tradestats.csv?date={date}&start={cursor * 1000}&iss.only=data'
                df = pd.read_csv(url, sep=';', skiprows=2)
                tradestats = pd.concat([tradestats, df])
                if df.shape[0] < 1000:
                    break
                time.sleep(0.5)
        df = tradestats.loc[tradestats['secid'] == 'AFLT'][['pr_open', 'pr_high', 'pr_low',
                                                            'pr_close', 'pr_std', 'vol', 'val', 'trades', 'pr_vwap',
                                                            'pr_change',
                                                            'trades_b', 'trades_s', 'val_b', 'val_s', 'vol_b', 'vol_s',
                                                            'disb',
                                                            'pr_vwap_b', 'pr_vwap_s']]
        df = df.apply(pd.to_numeric, errors='coerce')

        features = ['pr_open', 'pr_high', 'pr_low', 'pr_std', 'vol', 'val',
                    'trades', 'pr_vwap', 'pr_change',
                    'trades_b', 'trades_s', 'val_b', 'val_s', 'vol_b', 'vol_s', 'disb',
                    'pr_vwap_b', 'pr_vwap_s']
        periods = [30, 60, 120, 720, 1440, 2880]

        df['target'] = tradestats.loc[tradestats['secid'] == 'AFLT']['pr_close'].shift(-1)
        df['target30'] = tradestats.loc[tradestats['secid'] == 'AFLT']['pr_close'].shift(-6)
        df['target60'] = tradestats.loc[tradestats['secid'] == 'AFLT']['pr_close'].shift(-12)
        df['target120'] = tradestats.loc[tradestats['secid'] == 'AFLT']['pr_close'].shift(-24)
        df['target720'] = tradestats.loc[tradestats['secid'] == 'AFLT']['pr_close'].shift(-144)
        df['target1440'] = tradestats.loc[tradestats['secid'] == 'AFLT']['pr_close'].shift(-288)
        df['target2880'] = tradestats.loc[tradestats['secid'] == 'AFLT']['pr_close'].shift(-576)

        for i in features:
            for period in periods:
                df[f'{i}{str(period)}'] = tradestats.loc[tradestats['secid'] == 'AFLT'][i].shift(period // 5)

        df = df.iloc[576:-576]
        for i in features:
            for period in periods:
                df[i + '_dyn_' + str(period)] = df[i] - df[i + str(period)]

        for i in df.columns:
            df[i] = df[i].astype(float)

        df_train = df.iloc[:int(len(df) * 0.8)]
        df_test = df.iloc[int(len(df) * 0.8):]
        train_feats = list(df.columns[134:]) + ['vol', 'val', 'trades', 'pr_change',
                                                'trades_b', 'trades_s', 'val_b', 'val_s', 'vol_b', 'vol_s', 'disb']
        X_train = df_train[train_feats]
        y_train = df_train['target']
        y_train30 = df_train['target30']
        y_train60 = df_train['target60']
        y_train120 = df_train['target120']
        y_train720 = df_train['target720']
        y_train1440 = df_train['target1440']
        y_train2880 = df_train['target2880']

        X_test = df_test[train_feats]
        y_test = df_test['target']
        y_test30 = df_test['target30']
        y_test60 = df_test['target60']
        y_test120 = df_test['target120']
        y_test720 = df_test['target720']
        y_test1440 = df_test['target1440']
        y_test2880 = df_test['target2880']
        return X_train, y_train, X_test, y_test

    def add_model(self, model, model_name):
        self.models[model_name] = model

    def get_all_algos_names(self) -> list[str]:
        return [i for i in self.models]

    async def execute_algo(self, name: str, **user_params):
        # if 'train' in user_params:
        #     if user_params['train']:
        X_train, y_train, X_test, y_test = self.get_data(gen_dates('2023-01-01', '2023-01-05'))
        self.models[name].fit(X_train, y_train)
        return gen_dates('2023-01-01', '2023-01-05'), self.models[name].predict(X_test)
        # return []

    def get_algo_params(self, name: str):
        """Отдаёт словарь. Ключи - названия параметров, которые может крутить пользователь.
         Значения - список возможных значений для этих параметров (например,
         {"trade_strategy": ["aggressive", "middle", "soft"]})"""
        return {
            'trade_strategy': ['reliable', 'normal', 'risky'],
            # interval length of training data
            'interval': ['30 sec', '1 min', '5 min'],
            # target time shift
            'pred_shift': ['5 min', '1 hour', '2 hours',
                           '6 hours', '12 hours', '24 hours'],
            'tickers': 'list of tickers',
            'features_dict_size': ['S', 'M', 'L', 'XL'],
            'models_size': ['S', 'M', 'L', 'XL']
        }


algos = Algo()
