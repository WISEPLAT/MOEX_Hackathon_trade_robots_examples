import os
from pathlib import Path
import warnings
import numpy as np
import matplotlib.pyplot as plt
from time import time
from datetime import datetime, timedelta
import dateutil.relativedelta
import pandas_datareader.moex as pdr_moex
from scipy.optimize import curve_fit
import csv
from tqdm import tqdm
import copy
from moexalgo import Ticker
import pandas as pd
from prophet import Prophet


""" list of MOEX companies """
moex = [
    'ABRD', 'AFKS', 'AFLT', 'AKRN', 'ALRS', 'AMEZ', 'APTK', 'AQUA', 'ARSA', 'ASSB', 'AVAN', 'BANE', 'BANEP', 'BELU',
    'BISV', 'BISVP', 'BLNG', 'BRZL', 'BSPB', 'BSPBP', 'CBOM', 'CHGZ', 'CHKZ', 'CHMF', 'CHMK', 'CNTL', 'CNTLP', 'DASB',
    'DERZP', 'DIOD', 'DSKY', 'DVEC', 'DZRD', 'DZRDP', 'EELT', 'ELTZ', 'ENPG', 'ENRU', 'FEES', 'FESH', 'FLOT', 'GAZA',
    'GAZAP', 'GAZC', 'GAZP', 'GAZS', 'GAZT', 'GCHE', 'GEMA', 'GMKN', 'GRNT', 'GTRK', 'HIMC', 'HIMCP', 'HYDR', 'IDVP',
    'IGST', 'IGSTP', 'INGR', 'IRAO', 'IRKT', 'ISKJ', 'JNOS', 'JNOSP', 'KAZT', 'KAZTP', 'KBSB', 'KCHE', 'KCHEP', 'KGKC',
    'KGKCP', 'KLSB', 'KMAZ', 'KMEZ', 'KMTZ', 'KOGK', 'KRKN', 'KRKNP', 'KRKO', 'KRKOP', 'KROT', 'KROTP', 'KRSB', 'KRSBP',
    'KTSB', 'KTSBP', 'KUBE', 'KUZB', 'KZMS', 'KZOS', 'KZOSP', 'LENT', 'LIFE', 'LKOH', 'LNZL', 'LNZLP', 'LPSB', 'LSNG',
    'LSNGP', 'LSRG', 'LVHK', 'MAGE', 'MAGEP', 'MAGN', 'MERF', 'MFGS', 'MFGSP', 'MGNT', 'MGNZ', 'MGTS', 'MGTSP', 'MISB',
    'MISBP', 'MOEX', 'MORI', 'MRKC', 'MRKK', 'MRKP', 'MRKS', 'MRKU', 'MRKV', 'MRKY', 'MRKZ', 'MRSB', 'MSNG', 'MSRS',
    'MSTT', 'MTLR', 'MTLRP', 'MTSS', 'MVID', 'NAUK', 'NFAZ', 'NKHP', 'NKNC', 'NKNCP', 'NKSH', 'NLMK', 'NMTP', 'NNSB',
    'NNSBP', 'NPOF', 'NSVZ', 'NVTK', 'ODVA', 'OGKB', 'OMZZP', 'ORUP', 'PAZA', 'PHOR', 'PIKK', 'PLZL', 'PMSB', 'PMSBP',
    'POLY', 'POSI', 'PRFN', 'PRMB', 'RASP', 'RBCM', 'RDRB', 'RENI', 'RGSS', 'RKKE', 'RNFT', 'ROLO', 'ROSB', 'ROSN',
    'ROST', 'RSTI', 'RSTIP', 'RTGZ', 'RTKM', 'RTKMP', 'RTSB', 'RTSBP', 'RUAL', 'RUGR', 'RUSI', 'RZSB', 'SAGO', 'SAGOP',
    'SARE', 'SAREP', 'SBER', 'SBERP', 'SELG', 'SFIN', 'SGZH', 'SIBG', 'SIBN', 'SLEN', 'SMLT', 'SNGS', 'SNGSP', 'SPBE',
    'STSB', 'STSBP', 'SVAV', 'SVET', 'TASB', 'TASBP', 'TATN', 'TATNP', 'TGKA', 'TGKB', 'TGKBP', 'TGKN', 'TNSE', 'TORS',
    'TORSP', 'TRFM', 'TRMK', 'TRNFP', 'TTLK', 'TUZA', 'UCSS', 'UKUZ', 'UNAC', 'UNKL', 'UPRO', 'URKZ', 'USBN', 'UTAR',
    'UWGN', 'VEON-RX', 'VGSB', 'VGSBP', 'VJGZ', 'VJGZP', 'VLHZ', 'VRSB', 'VRSBP', 'VSMO', 'VSYD', 'VSYDP', 'VTBR',
    'WTCM', 'WTCMP', 'YAKG', 'YKEN', 'YKENP', 'YNDX', 'YRSB', 'YRSBP', 'ZILL', 'ZVEZ'
]

stocks10 = ['ASSB', 'CBOM', 'DVEC', 'FEES', 'HYDR', 'IRAO', 'KCHE', 'KCHEP', 'KTSB', 'KTSBP', 'KUZB', 'LIFE', 'MAGE',
            'MAGEP', 'MRKC', 'MRKP', 'MRKS', 'MRKU', 'MRKV', 'MRKY', 'MRKZ', 'MRSB', 'MSNG', 'MSRS', 'OGKB', 'PRFN',
            'RBCM', 'RGSS', 'ROLO', 'RTSB', 'RTSBP', 'SAGO', 'SAGOP', 'SARE', 'SAREP', 'SLEN', 'STSB', 'STSBP', 'TASB',
            'TASBP', 'TGKA', 'TGKB', 'TGKBP', 'TGKN', 'TORS', 'TORSP', 'TTLK', 'UNAC', 'UPRO', 'USBN', 'VTBR', 'WTCMP',
            'YKEN', 'YKENP']

stocks10_100 = ['AFKS', 'AFLT', 'ALRS', 'AMEZ', 'APTK', 'ARSA', 'BISVP', 'BLNG', 'CHGZ', 'CNTL', 'CNTLP', 'DIOD',
                'DSKY', 'HIMCP', 'IRKT', 'JNOS', 'JNOSP', 'KGKC', 'KGKCP', 'KLSB', 'KRKOP', 'KRSB', 'KRSBP', 'KZOSP',
                'LSNG', 'LVHK', 'MAGN', 'MRKK', 'NKNCP', 'NKSH', 'NMTP', 'RTKM', 'RTKMP', 'RUGR', 'RUSI', 'RZSB',
                'SELG', 'SNGS', 'SNGSP', 'UTAR', 'VGSB', 'VGSBP', 'WTCM', 'ZVEZ']

stocks100_200 = ['FESH', 'GAZP', 'KZOS', 'MISB', 'MISBP', 'MOEX', 'NKNC', 'NLMK', 'ROSB', 'ROST', 'TUZA', 'YAKG']

stocks200_1000 = ['ABRD', 'AQUA', 'BSPB', 'ELTZ', 'GAZAP', 'KAZT', 'KAZTP', 'KBSB', 'KMAZ', 'KMTZ', 'KROTP', 'KUBE',
                  'LSNGP', 'LSRG', 'MFGS', 'MFGSP', 'MSTT', 'MTLR', 'MTLRP', 'MTSS', 'MVID', 'NAUK', 'NFAZ', 'NSVZ',
                  'PIKK', 'PMSB', 'PMSBP', 'RASP', 'RDRB', 'ROSN', 'SBER', 'SBERP', 'SIBN', 'SVAV', 'TATN', 'TATNP',
                  'TRMK', 'UCSS', 'UWGN', 'VJGZP', 'VLHZ', 'VRSB', 'VRSBP', 'YRSBP']

stocks1000_10000 = ['BANE', 'BANEP', 'BELU', 'BRZL', 'CHMF', 'DZRD', 'DZRDP', 'GAZA', 'GCHE', 'IGST', 'IGSTP', 'INGR',
                    'KMEZ', 'KROT', 'LKOH', 'LNZLP', 'MGNT', 'MGTS', 'MGTSP', 'NNSB', 'NNSBP', 'NVTK', 'PHOR', 'TNSE',
                    'UKUZ', 'VJGZ', 'YNDX', 'YRSB', 'ZILL']

stocks10000 = ['AKRN', 'CHKZ', 'CHMK', 'GMKN', 'KOGK', 'KRKN', 'KRKNP', 'LNZL', 'OMZZP', 'PAZA', 'PLZL', 'PRMB', 'RKKE',
               'RTGZ', 'TRNFP', 'UNKL', 'URKZ', 'VSMO', 'VSYD', 'VSYDP']


dirpath = os.path.join(Path().resolve(), 'MOEX')
Path(dirpath).mkdir(parents=True, exist_ok=True)
warnings.filterwarnings("ignore", category=FutureWarning)


def random_tickers(N, stocks):
    """
    Obtaining random list of stocks for optimization

    Parameters
    ----------
    N : int
        Number of stocks for consideration
    stocks : list of str
        List of stocks to choose from 

    Returns
    -------
    tickers : list
        List of strings - names of stocks

    """
    numb = np.max([len(stocks), N])
    if numb == N:
        tickers = stocks
    else:
        params = np.random.choice(numb, N, replace='True')
        tickers = []
        for i in params:
            tickers.append(stocks[i])
    return tickers


def download_data(tickers):
    """
    Downloads data for all tickers at 1 year before - current time.
    Needs to be updated every day.
    Discarding stocks, which are bad - don't have enough data of even don't load at all
    Unoptimized, needs Roman's touch

    Parameters
    ----------
    tickers : list
        list of strings - names of stocks

    Returns
    -------
    bad_names : list
        list of strings - list of bad (ignored) stocks

    """

    mode = 'window'

    now = datetime.now()
    end_time = now - timedelta(days=1)
    start_time = end_time - timedelta(days=366)
    bad_names = []

    if mode == 'console':
        with tqdm(total=len(tickers)) as pbar:
            for i, stock in enumerate(tickers):
                try:
                    stock_df = pdr_moex.MoexReader(stock, start_time, end_time).read()
                    stock_df['Name'] = stock
                    stock_df['Diff'] = stock_df['CLOSE'] - stock_df['OPEN']
                    stock_df.drop(['ACCINT', 'ADMITTEDQUOTE', 'ADMITTEDVALUE', 'BEICLOSE', 'BID',
                                   'BOARDID', 'BOARDNAME', 'BUYBACKDATE', 'CBRCLOSE',
                                   'CLOSEAUCTIONPRICE', 'CLOSEPERIOD', 'CLOSEVAL', 'COUPONPERCENT',
                                   'COUPONVALUE', 'CURRENCYID', 'DAILYCAPITALIZATION', 'DECIMALS',
                                   'DURATION', 'FACEUNIT', 'FACEVALUE', 'HIGH', 'HIGHBID', 'IRICPICLOSE',
                                   'ISIN', 'ISSUESIZE', 'LASTPRICE', 'LASTTRADEDATE', 'LEGALCLOSEPRICE',
                                   'LEGALOPENPRICE', 'LISTNAME', 'LOW', 'LOWOFFER', 'MARKETPRICE',
                                   'MARKETPRICE2', 'MARKETPRICE3', 'MARKETPRICE3CUR',
                                   'MARKETPRICE3TRADESVALUE', 'MARKETPRICE3TRADESVALUECUR', 'MATDATE',
                                   'MONTHLYCAPITALIZATION', 'MP2VALTRD', 'MPVALTRD', 'NUMBID', 'NUMOFFER',
                                   'NUMTRADES', 'OFFER', 'OFFERDATE', 'OPEN', 'OPENPERIOD', 'OPENVAL',
                                   'PREV', 'PREVLEGALCLOSEPRICE', 'REGNUMBER', 'SECID', 'SHORTNAME',
                                   'TRADINGSESSION', 'TRENDCLOSE', 'TRENDCLSPR', 'TRENDWAP', 'TRENDWAPPR',
                                   'TYPE', 'VALUE', 'VOLUME', 'WAPRICE', 'WAVAL', 'YIELDATWAP',
                                   'YIELDCLOSE', 'YIELDLASTCOUPON', 'YIELDTOOFFER'], axis=1, inplace=True)
                    stock_df.rename(columns={'CLOSE': 'Close'}, inplace=True)
                    cols = stock_df.columns.tolist()
                    cols = [cols[0], cols[2]]
                    stock_df = stock_df[cols]
                    output_name = os.path.join(dirpath, stock + '.csv')
                    stock_df.to_csv(output_name)
                except:
                    bad_names.append(stock)
                pbar.update(1)
    else:
        for i, stock in enumerate(tickers):
            try:
                stock_df = pdr_moex.MoexReader(stock, start_time, end_time).read()
                stock_df['Name'] = stock
                stock_df['Diff'] = stock_df['CLOSE'] - stock_df['OPEN']
                stock_df.drop(['ACCINT', 'ADMITTEDQUOTE', 'ADMITTEDVALUE', 'BEICLOSE', 'BID',
                               'BOARDID', 'BOARDNAME', 'BUYBACKDATE', 'CBRCLOSE',
                               'CLOSEAUCTIONPRICE', 'CLOSEPERIOD', 'CLOSEVAL', 'COUPONPERCENT',
                               'COUPONVALUE', 'CURRENCYID', 'DAILYCAPITALIZATION', 'DECIMALS',
                               'DURATION', 'FACEUNIT', 'FACEVALUE', 'HIGH', 'HIGHBID', 'IRICPICLOSE',
                               'ISIN', 'ISSUESIZE', 'LASTPRICE', 'LASTTRADEDATE', 'LEGALCLOSEPRICE',
                               'LEGALOPENPRICE', 'LISTNAME', 'LOW', 'LOWOFFER', 'MARKETPRICE',
                               'MARKETPRICE2', 'MARKETPRICE3', 'MARKETPRICE3CUR',
                               'MARKETPRICE3TRADESVALUE', 'MARKETPRICE3TRADESVALUECUR', 'MATDATE',
                               'MONTHLYCAPITALIZATION', 'MP2VALTRD', 'MPVALTRD', 'NUMBID', 'NUMOFFER',
                               'NUMTRADES', 'OFFER', 'OFFERDATE', 'OPEN', 'OPENPERIOD', 'OPENVAL',
                               'PREV', 'PREVLEGALCLOSEPRICE', 'REGNUMBER', 'SECID', 'SHORTNAME',
                               'TRADINGSESSION', 'TRENDCLOSE', 'TRENDCLSPR', 'TRENDWAP', 'TRENDWAPPR',
                               'TYPE', 'VALUE', 'VOLUME', 'WAPRICE', 'WAVAL', 'YIELDATWAP',
                               'YIELDCLOSE', 'YIELDLASTCOUPON', 'YIELDTOOFFER'], axis=1, inplace=True)
                stock_df.rename(columns={'CLOSE': 'Close'}, inplace=True)
                cols = stock_df.columns.tolist()
                cols = [cols[0], cols[2]]
                stock_df = stock_df[cols]
                output_name = os.path.join(dirpath, stock + '.csv')
                stock_df.to_csv(output_name)
            except:
                bad_names.append(stock)

    return bad_names


def get_data(tickers, start_time, end_time):
    """
    Obtaining data for the provided tickers, between two desired dates. 
    Discarding stocks, which are bad - don't have enough data of even don't load at all
    Unoptimized, needs Roman's touch

    Parameters
    ----------
    tickers : list
        list of strings - names of stocks
    start_time : list shape (3)
        (year/month/day)
    end_time : list shape (3)
        (year/month/day)

    Returns
    -------
    data : np.ndarray shape (Number of good stocks, Number of days + 1, 3)
        price and return of the stock at each market day between two dates
        plus nans from string elements, which need to be discarded
    good_names : list
        list of strings - list of good (selected) stocks
    bad_names : list
        list of strings - list of bad (ignored) stocks

    """
    start_time = datetime(start_time[0], start_time[1], start_time[2])
    end_time = datetime(end_time[0], end_time[1], end_time[2])
    bad_names = []
    data = []
    raw_data = []
    good_names = []
    bounds = np.zeros(len(tickers))
    for i, stock in enumerate(tickers):
        try:
            output_name = os.path.join(dirpath, stock + '.csv')
            with open(output_name, newline='') as f:
                reader = csv.reader(f)
                stock_data = list(reader)
            stocks = [el[0] for el in stock_data]
            try:
                start = stocks.index(str(start_time)[0:10])
            except:
                try:
                    start = stocks.index(str(start_time - timedelta(days=1))[0:10])
                except:
                    start = stocks.index(str(start_time + timedelta(days=1))[0:10])
            try:
                end = stocks.index(str(end_time)[0:10])
            except:
                try:
                    end = stocks.index(str(end_time - timedelta(days=1))[0:10])
                except:
                    try:
                        end = stocks.index(str(end_time + timedelta(days=1))[0:10])
                    except:
                        end = stocks.index(str(end_time - timedelta(days=2))[0:10])
            stock_data = np.array(stock_data[start:end + 1][:])[:, 1:3]
            stock_data = np.asarray(stock_data, dtype=float)
            raw_data.append(stock_data)
            bounds[i] = stock_data.shape[0]
        except:
            bad_names.append(stock)
            raw_data.append(np.array([0]))
    duration = np.max(bounds)

    for i, stock in enumerate(raw_data):
        if stock.shape[0] == duration:
            data.append(stock)
            good_names.append(tickers[i])
        else:
            bad_names.append(tickers[i])

    data = np.array(data)

    return data, good_names, bad_names

def predict_price(ticker, date_start, date_end, period_forecast = 14, freq_train='10min', freq_forecast='D'):
    """
    Функция для предсказания цен акции в будущем

    ...
    
    Параметры
    ----------
    ticker : str
        название тикета, для которого нужно предсказать цены
    date_start : str
        дата начала периода, на котором обучаемся, в формате 'YYYY-MM-DD'
    date_end : str
        дата конца пероида, на котором обучаемся, в формате 'YYYY-MM-DD'
    period_forecast: int
        количество предсказаний (по умолчанию 31)
    freq_train: str
        периодичность данных, на которых обучаемся, в формате pandas (по умолчанию '1h', то есть часовая)
    freq_forecast: str
        частота, с которым нужно предсказывать цену в формате pandas (по умолчанию 'D')
        
    """
    
    data_train = Ticker(ticker).candles(date=date_start, till_date=date_end, period=freq_train)
    data_train = data_train[['close', 'end']].rename(columns = {'close': 'y', 'end': 'ds'})
    
    m = Prophet(weekly_seasonality=False,daily_seasonality=False,yearly_seasonality=False)
    m.fit(data_train)
    future = m.make_future_dataframe(period_forecast, freq=freq_forecast, include_history=False)
    fcst = m.predict(future)
                     
    return fcst

def date_diff(date, diff_month):
    date = datetime.strptime(date, '%Y-%m-%d').date()
    res = date - dateutil.relativedelta.relativedelta(months=diff_month)
    
    return str(res)

def coeff(df_input):
    """
    Функция для расчёта метрики h_i

    ...
    
    Параметры
    ----------
    df : pd.DataFrame
        DataFrame с полями ds - датой, y - реальной ценой акции, yhat - предсказанием цены
        
    """
    df = copy.deepcopy(df_input)
    df['yhat_delta'] =  df['yhat'].pct_change()
    df['yhat_delta_rel'] = df['yhat_delta']/df['yhat']

    return df['yhat_delta_rel'].mean()


def training_data_average(data, training_period=-1):
    """
    Reshapes data to the coefficients of MPT problem:
        Maximize: [ \sum J_{i,j} s_i s_j - \sum h_i s_i;  s_i = +-1   ]

    Parameters
    ----------
    data : np.ndarray shape (Number of good stocks, Number of days + 1, 3)
        price and return of the stock at each market day between two dates
    training_period : int, optional
        number of days since the start, along which are used for training.
        The default is -1, meaning all days are used for training (typical for final product)

    Returns
    -------
    J : np.ndarray shape (number of good stocks, number of good stocks)
        first coefficient
    h : np.array shape (number of good stocks)
        second coefficient
    MPT_prices : np.ndarray(number of good stocks, number of market days)
        Prices of each stock at every market day

    """
    MPT = np.zeros((data.shape[0], data[0].shape[0]))
    MPT_prices = np.zeros((data.shape[0], data[0].shape[0]))
    for p in range(data.shape[0]):
        for j in range(data[0].shape[0]):
            MPT[p, j] = (data[p][j][1]) / data[p][j][0]
            MPT_prices[p, j] = data[p][j][0]
    MPT_train = MPT[:, :training_period]
    MPT_train = np.nan_to_num(MPT_train)
    R = MPT_train.mean(axis=1)
    C = np.cov(MPT_train)

    h_s = C.sum(axis=1)
    h = (h_s - R) / 2
    J = np.array(C) / 4

    h = -1000 * np.array(h)
    J = -1000 * np.array(J)

    return J, h, MPT_prices

def training_data_predict(data,tickers,date_start, date_end, training_period=-1):
    """
    Reshapes data to the coefficients of MPT problem:
        Maximize: [ \sum J_{i,j} s_i s_j - \sum h_i s_i;  s_i = +-1   ]

    Parameters
    ----------
    data : np.ndarray shape (Number of good stocks, Number of days + 1, 3)
        price and return of the stock at each market day between two dates
    training_period : int, optional
        number of days since the start, along which are used for training.
        The default is -1, meaning all days are used for training (typical for final product)

    Returns
    -------
    J : np.ndarray shape (number of good stocks, number of good stocks)
        first coefficient
    h : np.array shape (number of good stocks)
        second coefficient
    MPT_prices : np.ndarray(number of good stocks, number of market days)
        Prices of each stock at every market day

    """
    MPT = np.zeros((data.shape[0], data[0].shape[0]))
    MPT_prices = np.zeros((data.shape[0], data[0].shape[0]))
    for p in range(data.shape[0]):
        for j in range(data[0].shape[0]):
            MPT[p, j] = (data[p][j][1]) / data[p][j][0]
            MPT_prices[p, j] = data[p][j][0]
    MPT_train = MPT[:, :training_period]
    MPT_train = np.nan_to_num(MPT_train)
    #R = MPT_train.mean(axis=1)
    R = []
    for ticker in tickers:
        res = predict_price(ticker, date_start, date_end)
        R.append(coeff(res))
    R = np.array(R)
    C = np.cov(MPT_train)

    h_s = C.sum(axis=1)
    h = (h_s - R) / 2
    J = np.array(C) / 4

    h = -1000 * np.array(h)
    J = -1000 * np.array(J)

    return J, h, MPT_prices


def portfolio_optimization(J, h, risk_level, O=0.3155, S=3, D=0.251, ksi=0.1, sigma=0.15, N_rounds=100):
    """
    The main function for portfolio optimization, performing it with npalgorithm

    Parameters
    ----------
    J : np.ndarray shape (number of good stocks, number of good stocks)
        first coefficient
    h : np.array shape (number of good stocks)
        second coefficient
    risk_level : float
        parameter, determining the risk of the portfolio (chosen from client test)
    O : float, optional
        hyperparameter for the final temperature. The default is 0.3155.
    S : float, optional
        hyperparameter for the tanh slope for temperature line. The default is 3.
    D : float, optional
        hyperparameter for initial temperature. The default is 0.251.
    ksi : float, optional
        learning rate. The default is 0.1.
    sigma : foat, optional
        probabilistic kick amplitude. The default is 0.15.
    N_rounds : int, optional
        Number of repetitions for the probabilistic algorithm 
        = N_rounds*Number of stocks^2. The default is 50.

    Returns
    -------
    m : float
        the value of optimal (maximal) energy
    x : np.array shape(number of stocks)
        solution of portfolio selection problem. +1 - take stocks, -1 - ignore
    success_rate : float
        number of successful algorithm outcomes to full number of rounds
    """
    N = len(h)
    S = S * N / 50
    sat = 1
    t = np.arange(-20, 80, 1)

    nu = O * np.tanh(S * (t / N - 0.5)) - D
    N_rounds = N_rounds * N ** 2
    H = [h for i in range(N_rounds)]
    H = np.array(H).T
    en = np.zeros(N_rounds)
    x = np.zeros([N, N_rounds])

    for nut in nu:
        f = np.random.normal(0, sigma, [N, N_rounds])
        x = x + nut * x + ksi * (risk_level * np.dot(J, x) - H) + f
        x = np.where(np.abs(x) < sat, x, sat * np.sign(x))
    x = np.sign(x).T
    el = np.arange(0, N_rounds, 1)
    for i in el:
        en[i] = np.dot(x[i], np.dot(J, x[i])) - np.dot(h, x[i])
    m = np.max(en)

    return m, x[np.argmax(en)], len(en[en == m]) / N_rounds


def portfolio_balancing(portfolio, fortune, ave):
    """
    Returns the final price of the portfolio, and the quantities of each stock, which you
    need to buy for the appropriate result.

    Parameters
    ----------
    portfolio : list of str
        list of stocks in optimized portfolio
    fortune : float
        Our budget

    Returns
    -------
    my_portfolio : float
        Resulting budget (after rebalancing with quantized stock prices)
    port : np.ndarray shape(len(portfolio))
        Quantities of each stock in the portfolio
        
    """
    now = datetime.now()
    start = now - timedelta(days=3)
    data, names, bad_names = get_data(portfolio, [start.year, start.month, start.day],
                                      [now.year, now.month, now.day])
    if ave == '0':    
        J, h, MPT_prices = training_data_average(data)
    if ave == '1':    
        J, h, MPT_prices = training_data_average(data,portfolio,str(start)[0:10], str(now)[0:10])
    scale = fortune / len(portfolio)
    port = np.zeros(len(portfolio))
    for i in range(len(portfolio)):
        port[i] = int(scale / MPT_prices[i, -1])
    my_portfolio = port[0] * MPT_prices[0, -1]
    for p in range(1, len(portfolio)):
        my_portfolio = my_portfolio + port[p] * MPT_prices[p, -1]
    return int(my_portfolio), port


def portfolio_properties(x, MPT_prices, good_names, fortune):
    """
    Returns the resulting portfolio - stocks, that needed to be purchased in 
    equal amounts. As wee as expected return and risk of the portfolio.

    Parameters
    ----------
    x : np.array shape (number of stocks)
        solution for the MPT problem
    MPT_prices : np.ndarray shape (number of stocks, number of days)
        prices of each stock at each market day
    good_names : list
        list of all stocks, considered in the MPT solution
    fortune : float
        Our budget

    Returns
    -------
    portfolio : list
        list of names of each stock in resulting portfolio
    retur : float
        expected return of the portfolio according to the historic data
        slope of the linear fit on the prices of the portfolio
    risk : float
        expected risk of the portfolio - 3 * standard deviation
        of the expected return
        
    Creates txt file with portfolio, called 
    date2023-12-23_volume100000_len45.txt for example

    """
    portfolio = []
    for i, el in enumerate(x):
        if el == 1:
            portfolio.append(good_names[i])

    scale = fortune / len(portfolio)
    port = np.zeros(len(portfolio))
    for i in range(len(portfolio)):
        port[i] = int(scale / MPT_prices[i, 0])

    my_portfolio = port[0] * MPT_prices[0, :]
    for p in range(1, len(portfolio)):
        my_portfolio = my_portfolio + port[p] * MPT_prices[p, :]
    my_portfolio = np.nan_to_num(my_portfolio)
    for i, el in enumerate(my_portfolio):
        if el == 0:
            my_portfolio[i] = my_portfolio[i - 1]

    def linear(x, a, b):
        return a * x + b

    popt, pcov = curve_fit(linear, np.arange(len(my_portfolio)), my_portfolio)

    retur = (linear(len(my_portfolio), *popt) - linear(0, *popt)) / linear(0, *popt) * 7 / 5
    risk = 3 * np.sqrt(pcov[0, 0]) / popt[0]

    return portfolio, retur, risk


def portfolio_plot(portfolio, start_date, end_date, fortune, ave):
    """
    Creates the plot of evenly distributed portfolio from start date to now, 
    and indicates the position when the client calculated this portfolio

    Parameters
    ----------
    portfolio : list of str
        list of stocks, which are selected for the portfolio
    start_date : list shape (3)
        (year, month, day) - starting date used for portfolio calculation
    end_date : list shape (3)
        (year, month, day) - final date used for portfolio calculation
    fortune : float
        Our budget

    Returns
    -------
    None.
    Creates plot png file called
    date2023-12-13_volume100000_len45.png for example

    """
    now = datetime.now()
    data, names, bad_names = get_data(portfolio, start_date, [now.year, now.month, now.day])
    portfolio = names
    start = datetime(start_date[0], start_date[1], start_date[2])
    end = datetime(end_date[0], end_date[1], end_date[2])
    period = np.busday_count(start.date(), end.date())
    if ave == '0':    
        J, h, MPT_prices = training_data_average(data)
    if ave == '1':    
        J, h, MPT_prices = training_data_average(data,portfolio,str(start)[0:10], str(end)[0:10])
    
    
    scale = fortune / len(portfolio)
    port = np.zeros(len(portfolio))
    for i in range(len(portfolio)):
        port[i] = int(scale / MPT_prices[i, -1])
    predicted = []
    for ticker in portfolio:
        predicted.append(predict_price(ticker, str(start), str(now))['yhat'])
    predicted = np.array(predicted)
    prices = pd.concat(MPT_prices,predicted)
    
    my_portfolio = port[0] * prices[0, :]
    for p in range(1, len(portfolio)):
        my_portfolio = my_portfolio + port[p] * prices[p, :]
    my_portfolio = np.nan_to_num(my_portfolio)
    for i, el in enumerate(my_portfolio):
        if el == 0:
            my_portfolio[i] = my_portfolio[i - 1]
    duration = np.busday_count(start.date(), now.date())
    tick = duration // 5
    tickes = []
    ticke = np.arange(6) * tick
    for i in range(6):
        tickes.append(str(start + timedelta(days=i * int(tick * 7 / 5)))[0:10])
    plt.figure(dpi=300)
    plt.plot(my_portfolio, color=(51 / 256, 161 / 256, 142 / 256), label='Мой портфель')
    plt.axvline(period, c='r', ls='--', label='Предыдущий расчет')
    plt.xticks(ticke, tickes, rotation=45)
    plt.ylabel('Стоимость портфеля, рубли', fontsize=11)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    string = 'date' + str(now)[0:10] + "_volume" + str(int(my_portfolio[-1])) + "_len" + str(len(portfolio)) + ".png"
    plt.savefig(string, dpi=300)
    # plt.show()

    return string


def filewriter(portfolio, my_portfolio, port):
    """

    Parameters
    ----------
    portfolio : list of str
        list of stocks, which are selected for the portfolio
    my_portfolio : float
        Resulting budget (after rebalancing with quantized stock prices)
    port : np.ndarray shape(len(portfolio))
        Quantities of each stock in the portfolio

    Returns
    -------
    Creates txt file with portfolio, called 
    date2023-12-23_volume100000_len45.txt for example
    
    """
    now = datetime.now()
    string = 'date' + str(now)[0:10] + "_volume" + str(int(my_portfolio)) + "_len" + str(len(portfolio)) + ".txt"
    with open(string, 'wb') as f:
        f.write(f"Ваш Портфель стоимостью {my_portfolio} рублей:\n".encode('utf8'))
        for i, line in enumerate(portfolio):
            pr = int(port[i])
            f.write(f"{i + 1}. Купите {line} в количестве {pr} штук\n".encode('utf8'))

    return string


def full_realization(fortune, number, risk, ave):
    """
    Full realization of the setup. For now, we need to choose fortune as:
    budget less than 10 000 : fortune = 10000
    budget less than 50 000 : fortune = 50000
    budget less than 150 000 : fortune = 150000
    budget unlimited : fortune = 1e7
    number is chosen between (50, 100, 150), but can be arbitrary in principle.
    risk is chosen from (1,2,3) for now.

    Parameters
    ----------
    fortune : float
        Our budget
    number : int
        Number of stocks from which we choose portfolio
    risk : float
        The desired value of risk: (high, mid, low) == risk = (1, 2, 3)

    Returns
    -------
    my_portfolio : float
        Resulting budget (after rebalancing with quantized stock prices)
    retur : float
        Expected level of return (in %)
    risker : float
        Expected level of risk (in %)
    success_rate : float (in %)
        Success rate of algorithm. Could be cool to show to client that we 
        chose from 1 000 000 variants, and only 3 of them were good (0.0003%)
    
    Plus creates txt file with portfolio and png file for the initial plot
        
    """
    stocks = []

    if fortune == 10000:
        stocks.extend(stocks10)
        stocks.extend(stocks10_100)
        stocks = random_tickers(number, stocks)

    if fortune == 50000:
        stocks.extend(stocks10)
        stocks.extend(stocks10_100)
        stocks.extend(stocks100_200)
        stocks = random_tickers(number, stocks)

    if fortune == 150000:
        stocks.extend(stocks10)
        stocks.extend(stocks10_100)
        stocks.extend(stocks100_200)
        stocks.extend(stocks200_1000)
        stocks = random_tickers(number, stocks)

    if fortune == 1e7:
        stocks = random_tickers(number, moex)

    nrounds = 100
    if number == 50:
        nrounds = 120
    elif number == 100:
        nrounds = 100
    elif number == 150:
        nrounds = 80

    now = datetime.now()
    start = now - timedelta(days=120)
    data, good_names, bad_names = get_data(stocks, [start.year, start.month, start.day], [now.year, now.month, now.day])
    if ave == '0':    
        J, h, MPT_prices = training_data_average(data)
    if ave == '1':    
        J, h, MPT_prices = training_data_average(data,stocks,str(start)[0:10], str(now)[0:10])
    m, solution, success_rate = portfolio_optimization(J, h, risk, N_rounds=nrounds)
    portfolio, retur, risker = portfolio_properties(solution, MPT_prices, good_names, fortune)
    plot_name = portfolio_plot(portfolio, [start.year, start.month, start.day], [now.year, now.month, now.day], fortune)
    my_portfolio, port = portfolio_balancing(portfolio, fortune)
    txt_file_name = filewriter(portfolio, my_portfolio, port)

    return my_portfolio, retur * 100, risker * 100, success_rate * 100, (txt_file_name, plot_name)


def full_realization_run(fortune, num_stocks, risk, ave):

    now = time()

    if os.path.exists('MOEX'):
        if os.listdir('MOEX'):
            datediff = 0
            for root, i, j in os.walk('MOEX'):
                times = []
                for k in j:
                    times.append(os.path.getmtime('MOEX\\' + k))
                datediff = (datetime.today() - datetime.fromtimestamp(max(times))).days
            if datediff > 0:
                print('Downloading stocks data')
                bad_names = download_data(moex)
        else:
            print('Downloading stocks data')
            bad_names = download_data(moex)
    else:
        print('Downloading stocks data')
        bad_names = download_data(moex)

    print('Calculating the portfolio')
    my_portfolio, retur, risker, success_rate, names = full_realization(fortune, num_stocks, risk, ave)

    print(names)
    print('Time consumed:', timedelta(seconds=(time() - now)))
    print("Success rate:", success_rate, "%")
    print("Expected return:", retur, "%")
    print("Expected risk:", risker, "%")

    return names


if __name__ == '__main__':

    full_realization_run(10000, 100, 3, 1)
