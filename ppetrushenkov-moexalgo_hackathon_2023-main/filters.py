import pandas_ta as ta
import pandas as pd
# import talib


def buy_cross(a: pd.Series, b: pd.Series):
    prev_a = a.shift(1)
    prev_b = b.shift(1)
    crossing = (a > b) & (prev_a < prev_b)
    return crossing


def squeeze(prices: pd.DataFrame, period: int = 21):
    squeeze = ta.squeeze(prices['high'], prices['low'], prices['close'], period, lazybear=True)

    if squeeze is None:
        return False

    sqz_on = squeeze['SQZ_ON']
    last_vals = list(sqz_on.values[-2:])
    if any(last_vals) == 1:
        return True
    else:
        return False


def mean_reversion(prices: pd.DataFrame, period=50, mult=3):
    # ma = talib.SMA(prices['close'], period)
    # std = talib.STDDEV(prices['close'], period)
    # ma = prices['close'].ta.sma(period)
    ma = ta.sma(prices["close"], length=period, talib=False)
    std = ta.stdev(prices["close"], length=period, talib=False)

    if ma is None or std is None:
        return False

    lower = ma - mult * std

    if any(prices['close'].values[-5:] < lower.values[-5:]):
        return True
    return False


def sma_crosses(prices: pd.DataFrame, short_period: int = 50, long_period: int = 200):
    prices = prices.iloc[-long_period-10:, :]
    # short_ma = talib.SMA(prices['close'], short_period)
    # long_ma = talib.SMA(prices['close'], long_period)
    short_ma = ta.sma(prices["close"], length=short_period, talib=False)
    long_ma = ta.sma(prices["close"], length=long_period, talib=False)
    
    if short_ma is None or long_ma is None:
        return False

    crosses = buy_cross(short_ma, long_ma)

    last_n = list(crosses.values[-10:])
    if any(last_n):
        return True
    return False


def supertrend_sma_breakout(prices: pd.DataFrame, ma_period: int = 200, atr_period : int = 21, mult: int = 2):
    prices = prices.iloc[-ma_period-atr_period:, :]
    # ma = talib.SMA(prices['close'], ma_period)
    ma = ta.sma(prices["close"], length=ma_period, talib=False)
    st = ta.supertrend(prices['high'], prices['low'], prices['close'], length=atr_period, multiplier=mult)

    if st is None or ma is None:
        return False

    crosses = buy_cross(prices['close'], st['SUPERT_21_2.0'])

    last_closes = prices['close'].values[-5:]
    last_crosses = list(crosses.values[-5:])
    last_ma = ma.values[-5:]

    if any(last_crosses) == True and any(last_closes > last_ma):
        return True
    return False


def no_trend(prices: pd.DataFrame, period: int = 21, thresh: int = 15):
    """Return 1 if ADX lower thresh else 0"""
    prices = prices.iloc[-2*period:, :]
    h = prices['high']
    l = prices['low']
    c = prices['close']
    # adx = talib.ADX(h, l, c, timeperiod=period)
    adx = ta.adx(h, l, c, timeperiod=period)
    
    if adx is None:
        return False

    if adx.iloc[-1, 0] <= thresh:
        return True
    else:
        return False


def breakout(prices: pd.DataFrame, period: int = 21):
    squeeze = ta.squeeze(prices['high'], prices['low'], prices['close'], period, lazybear=True)
    prices['SQZ_ON'] = squeeze['SQZ_ON']
    on = prices['SQZ_ON'].values[-5:]

    channel = ta.donchian(prices['high'], prices['low'], period, period)
    prices['upper'] = channel[f'DCU_{period}_{period}']
    prices['lower'] = channel[f'DCL_{period}_{period}']

    if channel is None or squeeze is None:
        return False

    if any(on) == 1 and prices['close'].values[-1] > prices['upper'].values[-2]:
        return True
    elif any(on) == 1 and prices['close'].values[-1] < prices['lower'].values[-2]:
        return True
    return False