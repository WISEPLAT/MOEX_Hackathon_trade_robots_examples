# Standard python libraries
import os
import datetime

# Installed libraries
import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import requests
import pyod

# Imports from our package
from lightautoml.tasks import Task
from lightautoml.addons.autots.base import AutoTS
from lightautoml.dataset.roles import DatetimeRole
from lightautoml.automl.base import AutoML
from lightautoml.ml_algo.boost_cb import BoostCB
from lightautoml.ml_algo.linear_sklearn import LinearLBFGS
from lightautoml.pipelines.features.lgb_pipeline import LGBSeqSimpleFeatures
from lightautoml.pipelines.features.linear_pipeline import LinearTrendFeatures
from lightautoml.pipelines.ml.base import MLPipeline
from lightautoml.reader.base import DictToPandasSeqReader
from lightautoml.automl.blend import WeightedBlender
from lightautoml.ml_algo.random_forest import RandomForestSklearn

from moexalgo import Market, Ticker

from company_conf import company_configs

# Disable warnings
import warnings
warnings.filterwarnings("ignore")

def train(ticker_name):
    print(f'Обучение модели для акции {ticker_name}')

    HORIZON = company_configs[ticker_name]['horizon']
    TARGET_COLUMN = "close"
    DATE_COLUMN = "date"

    # Настройки
    period = '1D'
    date_from = '2007-07-20'
    date_to = datetime.date.today()

    # Акции
    name = ""
    for i in ticker_name:
        if not i.isnumeric():
            name += i
    print('TICKER_NAME', name)
    ticker = Ticker(name)

    # Свечи по акциям за период. Период в минутах 1, 10, 60 или '1m', '10m', '1h', 'D', 'W', 'M', 'Q'; по умолчанию 60
    df = ticker.candles(date=date_from, till_date=date_to, period=period)
    df = pd.DataFrame([*df])

    df.drop(['end'], axis=1, inplace=True)
    df.rename(columns={"begin": "date"}, inplace=True)

    # Построение стратегии анализа
    MyStrategy = ta.Strategy(
        name="mystrat",
        ta=[
            {'kind': 'above_value', 'append': True},
            {'kind': 'accbands', 'append': True},
            {'kind': 'ad', 'append': True},
            {'kind': 'adosc', 'append': True},
            {'kind': 'adx', 'append': True},
            {'kind': 'alma', 'append': True},
            {'kind': 'amat', 'append': True},
            {'kind': 'ao', 'append': True},
            {'kind': 'aobv', 'append': True},
            {'kind': 'apo', 'append': True},
            {'kind': 'aroon', 'append': True},
            {'kind': 'atr', 'append': True},
            {'kind': 'bbands', 'append': True},
            {'kind': 'below', 'append': True},
            {'kind': 'below_value', 'append': True},
            {'kind': 'bias', 'append': True},
            {'kind': 'bop', 'append': True},
            {'kind': 'brar', 'append': True},
            {'kind': 'cci', 'append': True},
            {'kind': 'cdl_pattern', 'append': True},
            {'kind': 'cdl_z', 'append': True},
            {'kind': 'cfo', 'append': True},
            {'kind': 'cg', 'append': True},
            {'kind': 'chop', 'append': True},
            {'kind': 'cksp', 'append': True},
            {'kind': 'cmf', 'append': True},
            {'kind': 'cmo', 'append': True},
            {'kind': 'coppock', 'append': True},
            {'kind': 'cross', 'append': True},
            {'kind': 'cross_value', 'append': True},
            {'kind': 'cti', 'append': True},
            {'kind': 'decreasing', 'append': True},
            {'kind': 'dema', 'append': True},
            {'kind': 'dm', 'append': True},
            {'kind': 'donchian', 'append': True},
            {'kind': 'dpo', 'append': True},
            {'kind': 'efi', 'append': True},
            {'kind': 'ema', 'append': True},
            {'kind': 'entropy', 'append': True},
            {'kind': 'eom', 'append': True},
            {'kind': 'er', 'append': True},
            {'kind': 'eri', 'append': True},
            {'kind': 'fisher', 'append': True},
            {'kind': 'fwma', 'append': True},
            {'kind': 'hilo', 'append': True},
            {'kind': 'hl2', 'append': True},
            {'kind': 'hlc3', 'append': True},
            {'kind': 'hma', 'append': True},
            {'kind': 'hwma', 'append': True},
            {'kind': 'ichimoku', 'append': True},
            {'kind': 'increasing', 'append': True},
            {'kind': 'inertia', 'append': True},
            {'kind': 'kama', 'append': True},
            {'kind': 'kc', 'append': True},
            {'kind': 'kdj', 'append': True},
            {'kind': 'kst', 'append': True},
            {'kind': 'kurtosis', 'append': True},
            {'kind': 'kvo', 'append': True},
            {'kind': 'linreg', 'append': True},
            {'kind': 'log_return', 'append': True},
            {'kind': 'long_run', 'append': True},
            {'kind': 'macd', 'append': True},
            {'kind': 'mad', 'append': True},
            {'kind': 'massi', 'append': True},
            {'kind': 'mcgd', 'append': True},
            {'kind': 'median', 'append': True},
            {'kind': 'mfi', 'append': True},
            {'kind': 'midpoint', 'append': True},
            {'kind': 'midprice', 'append': True},
            {'kind': 'mom', 'append': True},
            {'kind': 'natr', 'append': True},
            {'kind': 'nvi', 'append': True},
            {'kind': 'obv', 'append': True},
            {'kind': 'ohlc4', 'append': True},
            {'kind': 'pdist', 'append': True},
            {'kind': 'percent_return', 'append': True},
            {'kind': 'pgo', 'append': True},
            {'kind': 'ppo', 'append': True},
            {'kind': 'psar', 'append': True},
            {'kind': 'psl', 'append': True},
            {'kind': 'pvi', 'append': True},
            {'kind': 'pvo', 'append': True},
            {'kind': 'pvol', 'append': True},
            {'kind': 'pvr', 'append': True},
            {'kind': 'pvt', 'append': True},
            {'kind': 'pwma', 'append': True},
            {'kind': 'qqe', 'append': True},
            {'kind': 'qstick', 'append': True},
            {'kind': 'quantile', 'append': True},
            {'kind': 'rma', 'append': True},
            {'kind': 'roc', 'append': True},
            {'kind': 'rsi', 'append': True},
            {'kind': 'rsx', 'append': True},
            {'kind': 'rvgi', 'append': True},
            {'kind': 'rvi', 'append': True},
            {'kind': 'short_run', 'append': True},
            {'kind': 'sinwma', 'append': True},
            {'kind': 'skew', 'append': True},
            {'kind': 'slope', 'append': True},
            {'kind': 'sma', 'append': True},
            {'kind': 'smi', 'append': True},
            {'kind': 'squeeze', 'append': True},
            {'kind': 'squeeze_pro', 'append': True},
            {'kind': 'ssf', 'append': True},
            {'kind': 'stdev', 'append': True},
            {'kind': 'stoch', 'append': True},
            {'kind': 'stochrsi', 'append': True},
            {'kind': 'supertrend', 'append': True},
            {'kind': 'swma', 'append': True},
            {'kind': 't3', 'append': True},
            {'kind': 'td_seq', 'append': True},
            {'kind': 'tema', 'append': True},
            {'kind': 'thermo', 'append': True},
            {'kind': 'tos_stdevall', 'append': True},
            {'kind': 'trima', 'append': True},
            {'kind': 'trix', 'append': True},
            {'kind': 'true_range', 'append': True},
            {'kind': 'tsi', 'append': True},
            {'kind': 'tsignals', 'append': True},
            {'kind': 'ttm_trend', 'append': True},
            {'kind': 'ui', 'append': True},
            {'kind': 'uo', 'append': True},
            {'kind': 'variance', 'append': True},
            {'kind': 'vhf', 'append': True},
            {'kind': 'vidya', 'append': True},
            {'kind': 'vortex', 'append': True},
            {'kind': 'vp', 'append': True},
            {'kind': 'vwma', 'append': True},
            {'kind': 'wcp', 'append': True},
            {'kind': 'willr', 'append': True},
            {'kind': 'wma', 'append': True},
            {'kind': 'xsignals', 'append': True},
            {'kind': 'zlma', 'append': True},
            {'kind': 'zscore', 'append': True}
        ]
    )

    try:
        df.ta.strategy(MyStrategy, append=True)
    except:
        try:
            df.ta.strategy(MyStrategy, append=True)
        except:
            df.ta.strategy(MyStrategy, append=True)

    # удалим колонки индикаторов с пропусками значений больше N
    col_to_del = []

    cols = list(df.columns)
    for col in cols:
        if df[col].isnull().sum() > 100:
            col_to_del.append(col)

    df.drop(col_to_del, axis=1, inplace=True)

    col_to_del = []

    cols = list(df.columns)
    for col in cols:
        if df[col].iloc[-100:].isnull().sum() > 0:
            col_to_del.append(col)

    df.drop(col_to_del, axis=1, inplace=True)

    # Удалим строки с пустыми ячейками индикаторов
    df = df.dropna()
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])

    # Сделаем временной ряд непрерывным и смержим с датасетом
    date = pd.DataFrame(pd.date_range(start=df.date.iloc[0], end=date_to), columns=['date'])
    df = date.merge(df, how='left', on='date')

    # Заполним пропуски
    for col in df.columns:
        if col == 'date':
            continue
        df.fillna(method='ffill', inplace=True)

    train = df

    task = Task("multi:reg", greater_is_better=False, metric="mae", loss="mae")

    roles = {
        "target": TARGET_COLUMN,
        DatetimeRole(seasonality=('d', 'm', 'wd'), base_date=True): DATE_COLUMN,
    }

    seq_params = {
        "seq0": {
            "case": "next_values",
            "params": {
                "n_target": HORIZON,
                "history": company_configs[ticker_name]['history'],
                "step": company_configs[ticker_name]['step'],
                "from_last": company_configs[ticker_name]['from_last'],
                "test_last": company_configs[ticker_name]['test_last']
            }
        }
    }

    transformers_params = {
        "lag_features": company_configs[ticker_name]['lag_features'],
        "lag_time_features": company_configs[ticker_name]['lag_time_features'],
        "diff_features": company_configs[ticker_name]['diff_features']
    }

    ### Параметры для модели тренда.
    trend_params = {
        'trend': company_configs[ticker_name]['trend'],
        'train_on_trend': company_configs[ticker_name]['train_on_trend'],
        'trend_type': company_configs[ticker_name]['trend_type'],
        'trend_size': company_configs[ticker_name]['trend_size'],
        'decompose_period': company_configs[ticker_name]['decompose_period'],
        'detect_step_quantile': company_configs[ticker_name]['detect_step_quantile'],
        'detect_step_window': company_configs[ticker_name]['detect_step_window'],
        'detect_step_threshold': company_configs[ticker_name]['detect_step_threshold'],
        'rolling_size': company_configs[ticker_name]['rolling_size'],
        'verbose': 0
    }

    automl = AutoTS(
            task,
            reader_params={
                "seq_params": seq_params
            },
            rf_params={"default_params": {"criterion": "squared_error"}},
            time_series_trend_params=trend_params,
            time_series_pipeline_params=transformers_params,
            config_path=r"C:\Users\tdall\anaconda3\envs\py39\Lib\site-packages\lightautoml\automl\presets\time_series_config.yml"
        )

    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"

    univariate_train_pred, _ = automl.fit_predict(train, roles, verbose=4)
    forecast, _ = automl.predict(train)

    result = [{
        "ticker": ticker_name,
        "predict_price": str(forecast[-1]),
        "predict_profit": str(forecast[-1] / train.close.values[-1] - 1),
        "timeframe": HORIZON
    }]

    count = 0
    while count <= 5:
        try:
            url = f'http://213.171.14.97:8080//api/v1/leaderboard/RemoveByDateAndTicker?ticker={ticker_name}&date={date_to}'
            response = requests.delete(url)
            if response.status_code == 200:
                print(f"Запрос успешно отправлен")
                break
        except Exception as err:
            print("Ошибка отправка запроса на API:")

        count += 1
        if count == 5:
            print("Ошибка отправка запроса на API:")

    count = 0
    while count <= 5:
        try:
            url = 'http://213.171.14.97:8080/api/v1/leaderboard'
            response = requests.post(url, json=result)
            if response.status_code == 200:
                print(f"Запрос успешно отправлен: {ticker_name}, {forecast[-1] / train.close.values[-1] - 1}")
                break
        except Exception as err:
            print("Ошибка отправка запроса на API:")

        count += 1
        if count == 5:
            print("Ошибка отправка запроса на API:")

