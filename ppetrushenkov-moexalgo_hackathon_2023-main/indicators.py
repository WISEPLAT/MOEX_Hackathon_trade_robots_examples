import pandas_ta as pta


def ma(price, period=21):
    return pta.sma(price, period).to_numpy()

def supertrend(data, period, mult):
    st = pta.supertrend(data.High.s, data.Low.s, data.Close.s, length=period, multiplier=mult)
    return st.iloc[:, 0].to_numpy()

def mfi(data, period):
    return pta.mfi(data.High.s, data.Low.s, data.Close.s, data.Volume.s, period).to_numpy()
