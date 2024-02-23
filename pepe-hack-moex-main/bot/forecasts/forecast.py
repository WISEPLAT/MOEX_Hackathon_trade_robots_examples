from moexalgo import Ticker
from datetime import datetime, timedelta
import pickle as pkl
import pandas as pd
import requests
from catboost import CatBoostRegressor


# backtest
############################################################

def start_forecast_backtest(backtest):
    tickers = ['AFLT', 'BANE', 'DSKY', 'FEES', 'GAZP', 'PHOR', 'POSI', 'SBER', 'YNDX', 'MTLR']
    preds = pd.read_csv('./forecasts/preds.csv', index_col=0)
    preds['dt'] = preds['dt'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

    while True:
        if backtest.get_new_data_was_adedd():
            data = load_data_for_forecast_backtest(backtest)
            do_forecast_backtest(data, preds, backtest)
            backtest.set_new_data_was_adedd(False)
            backtest.set_forecast_was_adedd(True)

def do_forecast_backtest(data, preds, backtest):
    cur_dt = data.ts.max()
    cur_data = data[data.ts == cur_dt]
    cur_pred = preds[preds.dt == cur_dt]
    cur_pred.reset_index(drop=True, inplace=True)
    for i, r in cur_pred.iterrows():
        cur_pred.loc[i, 'price_increase'] = cur_data[cur_data.secid == r.ticker].pr_close.values[0] - r.pred

    cur_pred.rename(columns={'pred': "price"}, inplace=True)
    backtest.set_forecast(cur_pred[['ticker', 'period', 'price', 'price_increase']])


def load_data_for_forecast_backtest(backtest):
    tradestats = backtest.get_tradestats()[['pr_close', 'ts', 'secid']]
    return tradestats
    tradestats = tradestats[tradestats.secid == ticker_name]
    tradestats.drop(columns='secid', inplace=True)

    orderstats = backtest.get_orderbook()
    orderstats = orderstats[orderstats.secid == ticker_name].tail(1)
    orderstats.drop(columns='secid', inplace=True)

    obstats = backtest.get_obstats()
    obstats = obstats[obstats.secid == ticker_name].tail(1)
    obstats.drop(columns=['secid', 'val_b', 'val_s', 'vol_b', 'vol_s'], inplace=True)

    df = tradestats.merge(orderstats, on=['ts'], how='left')
    df = df.merge(obstats, on=['ts'], how='left')

    return df



############################################################




def start_forecast():
    tickers = ['AFLT', 'BANE', 'DSKY', 'FEES', 'GAZP', 'PHOR', 'POSI', 'SBER', 'YNDX', 'MTLR']
    is_start = {ticker: True for ticker in tickers}

    while True:
        for ticker in tickers:
            if is_start[ticker]:
                cur_datetime = datetime.now()
                prev_datetime = do_forecat(ticker, cur_datetime)
                is_start[ticker] = False

            elif new_data_was_added(ticker, prev_datetime):
                cur_datetime = datetime.now()
                prev_datetime = do_forecat(ticker, cur_datetime)


def new_data_was_added(ticker_name, prev_datetime):
    ticker = Ticker(ticker_name)
    prev_datetime = pd.Timestamp(prev_datetime).to_pydatetime()
    last_record = pd.DataFrame(ticker.tradestats(date=prev_datetime.date(), latest=True))
    last_record_time = pd.Timestamp(last_record.ts.values[0]).to_pydatetime().time()

    return last_record_time != prev_datetime.time()


def do_forecat(ticker_name, cur_datetime=None, data=None):
    if data is not None:
        df = data
    else:
        df = load_data_for_forecast(ticker_name, cur_datetime.date())

    cur_datetime = df.ts.values[-1]
    df = add_features(df)

    pred_h, pred_d, pred_w = get_forecast(df.values[-1], ticker_name)
    save_forecast(ticker_name, [pred_h, pred_d, pred_w], df.pr_close.values[-1])

    return cur_datetime


def load_data_for_forecast(ticker_name, date):
    ticker = Ticker(ticker_name)
    till_date = date - timedelta(weeks=3)

    tradestats = pd.DataFrame(ticker.tradestats(date=till_date, till_date=date))
    tradestats.drop(columns='secid', inplace=True)

    orderstats = pd.DataFrame(ticker.orderstats(date=date, latest=True))
    orderstats.drop(columns='secid', inplace=True)

    obstats = pd.DataFrame(ticker.obstats(date=date, latest=True))
    obstats.drop(columns=['secid', 'val_b', 'val_s', 'vol_b', 'vol_s'], inplace=True)

    df = tradestats.merge(orderstats, on=['ts'], how='left')
    df = df.merge(obstats, on=['ts'], how='left')

    return df


def add_features(df):
    to_drop = ['cancel_val_b', 'cancel_val_s', 'cancel_vol_b', 'cancel_vol_s', 'cancel_vwap_b', 'cancel_vwap_s',
               'cancel_vol', 'cancel_val', 'cancel_orders']
    df.drop(columns=to_drop, inplace=True)

    # минимумы и макимумы за прошлый час
    df['max_prev_hour'] = df['pr_close'].rolling(window=12 + 1).max()
    df['min_prev_hour'] = df['pr_close'].rolling(window=12 + 1).min()

    # минимумы и макимумы за прошлый день
    df['max_prev_day'] = df['pr_close'].rolling(window=104 + 1).max()
    df['min_prev_day'] = df['pr_close'].rolling(window=104 + 1).min()

    # минимумы и макимумы за прошлую неделю
    df['max_prev_weak'] = df['pr_close'].rolling(window=104 * 5 + 1).max()
    df['min_prev_weak'] = df['pr_close'].rolling(window=104 * 5 + 1).min()

    # минимумы и макимумы за второй прошлый час
    df['max_prev_2_hour'] = df['pr_close'].rolling(window=12 * 2 + 1).max()
    df['min_prev_2_hour'] = df['pr_close'].rolling(window=12 * 2 + 1).min()

    # минимумы и макимумы за второй прошлый день
    df['max_prev_2_day'] = df['pr_close'].rolling(window=104 * 2 + 1).max()
    df['min_prev_2_day'] = df['pr_close'].rolling(window=104 * 2 + 1).min()

    # минимумы и макимумы за вторую прошлую неделию
    df['max_prev_2_weak'] = df['pr_close'].rolling(window=104 * 5 * 2 + 1).max()
    df['min_prev_2_weak'] = df['pr_close'].rolling(window=104 * 5 * 2 + 1).min()

    # минимумы и макимумы за третий прошлый час
    df['max_prev_3_hour'] = df['pr_close'].rolling(window=12 * 3 + 1).max()
    df['min_prev_3_hour'] = df['pr_close'].rolling(window=12 * 3 + 1).min()

    # минимумы и макимумы за третий прошлый день
    df['max_prev_3_day'] = df['pr_close'].rolling(window=104 * 3 + 1).max()
    df['min_prev_3_day'] = df['pr_close'].rolling(window=104 * 3 + 1).min()

    # минимумы и макимумы за третию прошлую неделию
    df['max_prev_3_weak'] = df['pr_close'].rolling(window=104 * 5 * 31).max()
    df['min_prev_3_weak'] = df['pr_close'].rolling(window=104 * 5 * 31).min()

    # предыдущие цена закрытия за час, день, неделю, (месяц)
    df['prev_pr_close'] = df.pr_close.shift(1)
    df['prev_pr_close_2'] = df.pr_close.shift(2)
    df['prev_pr_close_3'] = df.pr_close.shift(3)
    df['prev_pr_close_hour'] = df.pr_close.shift(12)
    df['prev_pr_close_hour'] = df.pr_close.shift(12 * 2)
    df['prev_pr_close_hour'] = df.pr_close.shift(12 * 3)
    df['prev_pr_close_day'] = df.pr_close.shift(104)
    df['prev_pr_close_weak'] = df.pr_close.shift(104 * 5)

    # разность между ценой открытия и закрытия за прошлый час, день, месяц
    df['prev_pr_diff_hour'] = df.pr_close.shift(1) - df.pr_open.shift(12)
    df['prev_pr_diff_1'] = df.pr_close.shift(1) - df.pr_open.shift(1)
    df['prev_pr_diff_2'] = df.pr_close.shift(1) - df.pr_open.shift(2)
    df['prev_pr_diff_3'] = df.pr_close.shift(1) - df.pr_open.shift(3)

    # временные признаки
    # дней до выходных
    # 5 минутных свечей до закрытия торгов
    df["day_of_week"] = df.ts.dt.dayofweek
    df["day_of_year"] = df.ts.dt.dayofyear
    df["month"] = df.ts.dt.month
    df["week"] = df.ts.dt.day_of_year // 7
    df["day"] = df.ts.dt.day
    df["hour"] = df.ts.dt.hour
    df["minute"] = df.ts.dt.minute

    df.drop(columns='ts', inplace=True)

    df['candels_befor_day_end'] = 104 - ((df['hour'] - 10) * 12 + (df['minute'] / 5))
    df['days_before_hollydays'] = 5 - df['day_of_week']

    df.fillna(-1, inplace=True)

    return df


def get_forecast(df, ticker_name):

    with open(f"./models/hourly_models/model_{ticker_name}.pkl", 'rb') as file:
        model = pkl.load(file)
    pred_h = model.predict(df)

    with open(f"./models/daily_models/model_{ticker_name}.pkl", 'rb') as file:
        model = pkl.load(file)
    pred_d = model.predict(df)

    with open(f"./models/weekly_models/model_{ticker_name}.pkl", 'rb') as file:
        model = pkl.load(file)
    pred_w = model.predict(df)



    # model = CatBoostRegressor().load_model(f"./models/hourly_models/model_{ticker_name}.kek")
    # pred_h = model.predict(df)
    #
    # model = CatBoostRegressor().load_model(f"./models/daily_models/model_{ticker_name}.kek")
    # pred_d = model.predict(df)
    #
    # model = CatBoostRegressor().load_model(f"./models/weekly_models/model_{ticker_name}.kek")
    # pred_w = model.predict(df)

    return pred_h, pred_d, pred_w


def save_forecast(ticker_name, preds, cur_pris):
    periods = ['hour', 'day', 'week']

    for period, pred in zip(periods, preds):
        json_data = {
            "ticker": ticker_name,
            "period": period,
            "price": round(pred, 2),
            "price_increase": round(cur_pris - pred, 2)
        }

        requests.post(f'http://127.0.0.1:8000/forecast/{ticker_name}', json=json_data)


# if __name__ == "__main__":
#     df_with_forecast = pd.DataFrame(columns=['ticker', 'period', 'dt', 'pred'])
#
#     path = 'C:/Users/Илья/Desktop/ALGo/git/pepe-hack-moex/bot/backtest_data'
#     tradestats_data = pd.read_csv(f'{path}/backtest_tradestats.csv', index_col=0)
#     tradestats_data['ts'] = tradestats_data['ts'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
#     obstats_data = pd.read_csv(f'{path}/backtest_obstats.csv', index_col=0)
#     obstats_data['ts'] = obstats_data['ts'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
#     orderbook_data = pd.read_csv(f'{path}/backtest_orderbook.csv', index_col=0)
#     orderbook_data['ts'] = orderbook_data['ts'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
#
#     tradestats = pd.read_csv(f'{path}/backtest_tradestats_2023-10-01_2023-10-31.csv', index_col=0)
#     tradestats['ts'] = tradestats['ts'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
#
#     tradestats_data = pd.concat([tradestats, tradestats_data])
#
#
#     for ticker_name in ['AFLT', 'BANE', 'DSKY', 'FEES', 'GAZP', 'PHOR', 'POSI', 'SBER', 'YNDX', 'MTLR']:
#         tradestats_data_cur = tradestats_data[tradestats_data.secid == ticker_name]
#         tradestats_data_cur.drop(columns='secid', inplace=True)
#
#         obstats_data_cur = obstats_data[obstats_data.secid == ticker_name]
#         obstats_data_cur.drop(columns=['secid', 'val_b', 'val_s', 'vol_b', 'vol_s'], inplace=True)
#
#         orderbook_data_cur = orderbook_data[orderbook_data.secid == ticker_name]
#         orderbook_data_cur.drop(columns=['secid'], inplace=True)
#
#         df = tradestats_data_cur.merge(obstats_data_cur, on=['ts'], how='left')
#         df = df.merge(orderbook_data_cur, on=['ts'], how='left')
#
#         datetime_stop = datetime.strptime('2023-10-31 18:40:00', "%Y-%m-%d %H:%M:%S")
#
#
#         a = df[df.ts <= datetime_stop]
#
#         ind_end = a.index[-1]
#
#         dt_cur = df[ind_end+1:].ts
#
#         df = add_features(df)
#         df = df[ind_end + 1:]
#         pred_h, pred_d, pred_w = get_forecast(df, ticker_name)
#
#         preds = [pred_h, pred_d, pred_w]
#         periods = ['hour', 'day', 'week']
#
#         for period, pred in zip(periods, preds):
#
#             cur_df = pd.DataFrame()
#             cur_df['ticker'] = [ticker_name]*len(df)
#             cur_df['period'] = [period]*len(df)
#             cur_df['dt'] = list(dt_cur)
#             cur_df['pred'] = list(pred)
#
#             df_with_forecast = pd.concat([df_with_forecast, cur_df])
#
#     df_with_forecast.to_csv('preds.csv')



    # start_forecast()


