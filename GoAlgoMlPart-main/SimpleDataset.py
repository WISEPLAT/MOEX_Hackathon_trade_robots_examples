from __future__ import annotations
from typing import Dict, List, Iterable

import pandas as pd
import numpy as np

from datetime import datetime, timedelta

from moexalgo import Ticker


import warnings
warnings.filterwarnings('ignore')

class SimpleDataset:

  @staticmethod
  def create_dataset(features, ticker, timeframe, candles=10000, notebook: bool = False):

    raw_dataset = SimpleDataset.load_dataset(ticker, timeframe, candles=candles, notebook=notebook)
    raw_columns = list(raw_dataset.columns)
    SimpleDataset.make_dataset(raw_dataset, target_col='close')
    if (features['lags']):
        SimpleDataset.create_lags(raw_dataset, features['lags']['features'], features['lags']['period'])
    if (features['cma']):
        SimpleDataset.create_cma(raw_dataset, features['cma']['features'])
    if (features['sma']):
        SimpleDataset.create_sma(raw_dataset, features['sma']['features'], features['sma']['period'])
    if (features['ema']):
        SimpleDataset.create_ema(raw_dataset, features['ema']['features'], features['ema']['period'])
    if (features['green_candles_ratio']):
        SimpleDataset.add_green_ratio(raw_dataset, period=features['green_candles_ratio']['period'])
    if (features['red_candles_ratio']):
        SimpleDataset.add_red_ratio(raw_dataset, period=features['red_candles_ratio']['period'])
    if (features['rsi']):
        SimpleDataset.add_rsi(raw_dataset, period=features['rsi']['period'])
    if (features['macd']):
        SimpleDataset.add_macd(raw_dataset, period=features['macd']['period'])
    if (features['bollinger']):
        SimpleDataset.add_bollinger(raw_dataset,
                                    period=features['bollinger']['period'],
                                    degree_of_lift=features['bollinger']['degree_of_lift'])
    if (features['time_features']):
        SimpleDataset.add_dates(raw_dataset,
                                month=features['time_features']['month'],
                                week=features['time_features']['week'],
                                day_of_month=features['time_features']['day_of_month'],
                                day_of_week=features['time_features']['day_of_week'],
                                hour=features['time_features']['hour'],
                                minute=features['time_features']['minute'])
    new_columns = [col for col in raw_dataset.columns if col not in raw_columns]
    raw_dataset.dropna(subset=new_columns, inplace=True)
    if 'week' in new_columns:
       raw_dataset['week'] = raw_dataset['week'].astype('int64')

    return raw_dataset

  @staticmethod
  def load_dataset(ticker: str, timeframe: str, candles: int = 10000, notebook: bool = False):

    if timeframe in ['1m', '10m']:
      delta = 10
    if timeframe == '1H':
      delta = 30
    if timeframe == '1D':
      delta = 100

    def normalize_row(candle):
        return {
            'open': candle.open,
            'close': candle.close,
            'high': candle.high,
            'low': candle.low,
            'value': candle.value,
            'volume': candle.volume,
            'begin': candle.begin,
            'end': candle.end,
        }

    if not notebook:
      def pandas_frame(candles_it):
          return pd.DataFrame([normalize_row(row) for row in candles_it])
    else:
       def pandas_frame(candles_it):
          return candles_it

    date_r = datetime.today()
    date_l = datetime.today() - timedelta(days=delta)
    tick = Ticker(ticker)
    tradestats = pandas_frame(tick.candles(date=date_l.strftime('%Y-%m-%d'), till_date=date_r.strftime('%Y-%m-%d'), period=timeframe))
    while len(tradestats) < candles:
      date_r = date_l
      date_l = date_l - timedelta(days=delta)
      tmp_tradestats = pandas_frame(tick.candles(date=date_l.strftime('%Y-%m-%d'), till_date=date_r.strftime('%Y-%m-%d'), period=timeframe))
      tradestats = pd.concat([tmp_tradestats, tradestats])
      tradestats.drop_duplicates(inplace=True, ignore_index=True)
    return tradestats.tail(candles)


  @staticmethod
  def make_dataset(tradestats: pd.DataFrame, target_col: str = 'close') -> pd.DataFrame:

    tradestats['date'] = pd.to_datetime(tradestats['end'])
    cols_to_drop = ['begin', 'end']

    target = f'{target_col}_pct'
    tradestats[target] = tradestats[target_col].pct_change()
    tradestats[target] = tradestats[target].shift(-1)
    tradestats.drop(columns=cols_to_drop, inplace=True)
    tradestats.rename(columns={target: 'target'}, inplace=True)
    tradestats.dropna(subset='target', inplace=True)

  @staticmethod
  def create_lags(
      tradestats: pd.DataFrame,
      lags_feats: Iterable[str],
      lags_size: Iterable[int],
  ) -> None:

    for feat in lags_feats:
      for size in lags_size:
        lag_col = f'{feat}_lag_{size}'
        tradestats[lag_col] = tradestats[feat].shift(size)



  @staticmethod
  def create_sma(
      tradestats: pd.DataFrame,
      sma_feats: Iterable[str],
      sma_size: Iterable[int],
  ) -> None:

    for feat in sma_feats:
      for size in sma_size:
        agg_col = f'{feat}_sma_{size}'
        tradestats[agg_col] = tradestats[feat].rolling(size).mean() # среднее арифметическое значение отдельных периодов (минут, часов, дней и так далее) за выбранный промежуток времени


  @staticmethod
  def create_cma(
      tradestats: pd.DataFrame,
      cma_feats: Iterable[str],
  ) -> None:

    for feat in cma_feats:
      agg_col = f'{feat}_cma'
      tradestats[agg_col] = tradestats[feat].expanding().mean()


  @staticmethod
  def create_ema(
      tradestats: pd.DataFrame,
      ema_feats: Iterable[str],
      ema_size: Iterable[int],
  ) -> None:

    for feat in ema_feats:
      for size in ema_size:
        agg_col = f'{feat}_ema_{size}'
        tradestats[agg_col] = tradestats[feat].ewm(span=size).mean() # Экспоненциально взвешенное скользящее среднее


  @staticmethod
  def add_green_ratio(
    tradestats: pd.DataFrame,
    period: Iterable[int] = None):

    if period:
      green_candles = [0] * (len(tradestats) + 1)
      razn = tradestats['close'] - tradestats['open']
      for i in range(1, len(tradestats) + 1):
        green_candles[i] = green_candles[i - 1] if razn.iloc[i - 1] < 0 else green_candles[i - 1] + 1

      for n in period:
        agg_col = f'green_{n}'
        tradestats[agg_col] = [np.nan if i < n else (green_candles[i] - green_candles[i - n]) / n for i in range(len(tradestats))]


  @staticmethod
  def add_red_ratio(
      tradestats: pd.DataFrame,
      period: Iterable[int] = None):


      if period:
        red_candles = [0] * (len(tradestats) + 1)
        razn = tradestats['close'] - tradestats['open']
        for i in range(1, len(tradestats) + 1):
          red_candles[i] = red_candles[i - 1] if razn.iloc[i - 1] > 0 else red_candles[i - 1] + 1

        for n in period:
          agg_col = f'red_{n}'

          tradestats[agg_col] = [np.nan if i < n else (red_candles[i] - red_candles[i - n]) / n for i in range(len(tradestats))]



  @staticmethod
  def add_rsi(
    tradestats: pd.DataFrame,
    period: Iterable[int] = None):

    if period:
      for n in period:
        agg_col = f'rsi_{n}'
        rise = (tradestats['close'] - tradestats['open']).apply(lambda x: x if x > 0 else 0)
        fall = (tradestats['close'] - tradestats['open']).apply(lambda x: np.abs(x) if x < 0 else 0)
        ema_rise = rise.ewm(span = n).mean()
        ema_fall = fall.ewm(span = n).mean()
        RS = ema_rise / ema_fall
        RSI = 100 - (100 / (1 + RS))
        tradestats[agg_col] = RSI

  @staticmethod
  def add_macd(
    tradestats: pd.DataFrame,
    period: Iterable[(int, int)] = None):

    if period:
      for n in period:
        n_fast, n_slow = n[0], n[1]
        agg_col = f'macd_{n_fast}_{n_slow}'
        ema_fast = tradestats['close'].ewm(span = n_fast).mean()
        ema_slow = tradestats['close'].ewm(span = n_slow).mean()
        macd = ema_fast - ema_slow
        tradestats[agg_col] = macd

  @staticmethod
  def add_bollinger(
    tradestats: pd.DataFrame,
    period: int = None,
    degree_of_lift: int = None,
    target_col: str = 'close'):


    if period and degree_of_lift:
      tradestats['center_line'] = tradestats['close'].rolling(period).mean()
      std_dev = [np.nan if i <= period else np.std(tradestats.iloc[i - period : i]['center_line']) for i in range(len(tradestats))]
      tradestats['up_line'] = [tradestats.iloc[i]['center_line'] + degree_of_lift * std_dev[i] for i in range(len(tradestats))]
      tradestats['down_line'] = [tradestats.iloc[i]['center_line'] - degree_of_lift * std_dev[i] for i in range(len(tradestats))]


  @staticmethod
  def add_dates(
      tradestats: pd.DataFrame,
      date_col='date',
      month=False,
      week=False,
      day_of_month=False,
      day_of_week=False,
      hour=False,
      minute=False
  ) -> None:

    if (month):
        tradestats['month'] = tradestats[date_col].dt.month
    if (week):
        tradestats['week'] = tradestats[date_col].dt.isocalendar().week
    if (day_of_month):
        tradestats['day_of_month'] = tradestats[date_col].dt.day
    if (day_of_week):
        tradestats['day_of_week'] = tradestats[date_col].dt.day_of_week
    if (hour):
        tradestats['hour'] = tradestats[date_col].dt.hour
    if (minute):
        tradestats['minute'] = tradestats[date_col].dt.minute


  def __init__():
    pass

