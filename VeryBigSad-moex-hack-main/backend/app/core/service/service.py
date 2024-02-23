import datetime
import logging

import pandas as pd
from moexalgo import Market

logger = logging.getLogger(__name__)

stocks = Market("stocks")
corr_stats = None


def get_ticker_corr(
        ticker: str,
        days: int = 10,
        corr_ratio: float = 0.3,
        start_date: datetime.datetime = datetime.date(2023, 10, 1),
):
    global corr_stats
    if corr_stats is None:
        dates = [start_date + datetime.timedelta(days=x) for x in range(days)]
        stocks_info = pd.concat([pd.DataFrame(stocks.tradestats(date=i)) for i in dates])
        stocks_info['tradedate'] = stocks_info['ts'].dt.date
        stocks_info['tradetime'] = stocks_info['ts'].dt.time
        # for all stocks info,
        stats = stocks_info.pivot_table(index='tradedate', columns='secid', values='pr_vwap_s', aggfunc='mean')
        corr_stats = stats.corr()

    spl = corr_stats.loc[:, [ticker]]
    l_list = list(spl[(spl[ticker] < corr_ratio) & (spl[ticker] > -corr_ratio)].index)
    r_list = list(spl[(spl[ticker] < corr_ratio) & (spl[ticker] > -corr_ratio)][ticker])

    result_list = [(l_list[i], r_list[i]) for i in range(min(len(l_list), len(r_list)))]
    return result_list


def get_is_ticker_good(ticker: str) -> bool:
    """Offline calculated


# pr_open_avg

def get_all_info(days=30, start_day=date(2023, 10, 1)):

    base_prices = {}
    trade_store = []
    obstats_store = []
    orderstats_store = []

    for i in range(0, days):

        print(start_day + timedelta(days=i))

        trade = stocks.tradestats(date=(start_day + timedelta(days=i)))
        if not trade.empty:
            df = trade.groupby(['tradedate', 'ticker']).agg(pr_open_avg=('pr_open', 'mean'), # средняя цена открытия
                                                       pr_close_avg=('pr_close', 'mean'), # средняя цена закрытия
                                                       pr_std_avg=('pr_std', 'mean'), # среднее отклонение
                                                       vol_sum=('vol', 'sum'), # объем торгов
                                                       pr_vwap_avg=('pr_vwap', 'mean'), # средневзвешенная цена
                                                       pr_change_max=('pr_change', 'max'), # изменение к прошлому дню
                                                       trades_b_sum=('trades_b', 'sum'), # количество покупок
                                                       trades_s_sum=('trades_s', 'sum'), # количество продаж
                                                       disb_avg=('disb', 'mean'), # я хуй знает что это))
                                                       pr_vwap_b_max=('pr_vwap_b', 'max'), # максимальная средвзвешенная цена покупок
                                                       pr_vwap_b_min=('pr_vwap_b', 'min'), # минимальная средвзвешенная цена покупок
                                                       pr_vwap_s_max=('pr_vwap_s', 'max'), # максимальная средвзвешенная цена продаж
                                                       pr_vwap_s_min=('pr_vwap_s', 'min'), # минимальная средвзвешенная цена продаж
                                                       )
            trade_store.append(df)

        obstats = stocks.obstats(date=(start_day + timedelta(days=i)))
        if not obstats.empty:
            df = obstats.groupby(['tradedate', 'ticker']).agg(spread_bbo_avg=('spread_bbo', 'mean'), # средняя цена открытия
                                                       spread_lv10_avg=('spread_lv10', 'mean'), # средняя цена закрытия
                                                       spread_1mio_avg=('spread_1mio', 'mean'), # среднее отклонение
                                                       levels_b_avg=('levels_b', 'mean'), # объем торгов
                                                       levels_s_avg=('levels_s', 'mean'), # средневзвешенная цена
                                                       imbalance_vol_bbo_avg=('imbalance_vol_bbo', 'mean'), # изменение к прошлому дню
                                                       imbalance_val_bbo_avg=('imbalance_val_bbo', 'mean'), # количество покупок
                                                       )
            obstats_store.append(df)



    trade_info = pd.concat(trade_store).reset_index()
    obstats_info = pd.concat(obstats_store).reset_index()

    result = pd.merge(trade_info, obstats_info, on=['tradedate', 'ticker'])
    return result

res = get_all_info(days=30, start_day=date(2023, 10, 1))


res_agg = res.groupby(['ticker']).agg(pr_open_avg=('pr_open_avg', 'mean'), # средняя цена открытия
                                                       pr_close_avg=('pr_close_avg', 'mean'), # средняя цена закрытия
                                                       pr_std_avg=('pr_std_avg', 'mean'), # среднее отклонение
                                                       vol_sum=('vol_sum', 'sum'), # объем торгов
                                                       pr_vwap_avg=('pr_vwap_avg', 'mean'), # средневзвешенная цена
                                                       pr_change_max=('pr_change_max', 'max'), # изменение к прошлому дню
                                                       trades_b_sum=('trades_b_sum', 'sum'), # количество покупок
                                                       trades_s_sum=('trades_s_sum', 'sum'), # количество продаж
                                                       disb_avg=('disb_avg', 'mean'), # я хуй знает что это))
                                                       pr_vwap_b_max=('pr_vwap_b_max', 'max'), # максимальная средвзвешенная цена покупок
                                                       pr_vwap_b_min=('pr_vwap_b_min', 'min'), # минимальная средвзвешенная цена покупок
                                                       pr_vwap_s_max=('pr_vwap_s_max', 'max'), # максимальная средвзвешенная цена продаж
                                                       pr_vwap_s_min=('pr_vwap_s_min', 'min'), # минимальная средвзвешенная цена продаж
                                                       spread_bbo_avg=('spread_bbo_avg', 'mean'), # средняя цена открытия
                                                       spread_lv10_avg=('spread_lv10_avg', 'mean'), # средняя цена закрытия
                                                       spread_1mio_avg=('spread_1mio_avg', 'mean'), # среднее отклонение
                                                       levels_b_avg=('levels_b_avg', 'mean'), # объем торгов
                                                       levels_s_avg=('levels_s_avg', 'mean'), # средневзвешенная цена
                                                       imbalance_vol_bbo_avg=('imbalance_vol_bbo_avg', 'mean'), # изменение к прошлому дню
                                                       imbalance_val_bbo_avg=('imbalance_val_bbo_avg', 'mean'), # количество покупок
                                                       )

res_agg = res_agg.reset_index()
res_predict = get_all_info(days=30, start_day=date(2023, 11, 1))


res_predict_agg = res_predict.groupby(['ticker']).agg(pr_open_avg=('pr_open_avg', 'mean'), # средняя цена открытия
                                                       pr_close_avg=('pr_close_avg', 'mean'), # средняя цена закрытия
                                                       pr_std_avg=('pr_std_avg', 'mean'), # среднее отклонение
                                                       vol_sum=('vol_sum', 'sum'), # объем торгов
                                                       pr_vwap_avg=('pr_vwap_avg', 'mean'), # средневзвешенная цена
                                                       pr_change_max=('pr_change_max', 'max'), # изменение к прошлому дню
                                                       trades_b_sum=('trades_b_sum', 'sum'), # количество покупок
                                                       trades_s_sum=('trades_s_sum', 'sum'), # количество продаж
                                                       disb_avg=('disb_avg', 'mean'), # я хуй знает что это))
                                                       pr_vwap_b_max=('pr_vwap_b_max', 'max'), # максимальная средвзвешенная цена покупок
                                                       pr_vwap_b_min=('pr_vwap_b_min', 'min'), # минимальная средвзвешенная цена покупок
                                                       pr_vwap_s_max=('pr_vwap_s_max', 'max'), # максимальная средвзвешенная цена продаж
                                                       pr_vwap_s_min=('pr_vwap_s_min', 'min'), # минимальная средвзвешенная цена продаж
                                                       spread_bbo_avg=('spread_bbo_avg', 'mean'), # средняя цена открытия
                                                       spread_lv10_avg=('spread_lv10_avg', 'mean'), # средняя цена закрытия
                                                       spread_1mio_avg=('spread_1mio_avg', 'mean'), # среднее отклонение
                                                       levels_b_avg=('levels_b_avg', 'mean'), # объем торгов
                                                       levels_s_avg=('levels_s_avg', 'mean'), # средневзвешенная цена
                                                       imbalance_vol_bbo_avg=('imbalance_vol_bbo_avg', 'mean'), # изменение к прошлому дню
                                                       imbalance_val_bbo_avg=('imbalance_val_bbo_avg', 'mean'), # количество покупок
                                                       )

res_predict_agg = res_predict_agg.reset_index()

res_predict_agg.head()
feature = res_predict_agg[['ticker', 'pr_open_avg']]
feature.rename(columns={'pr_open_avg': 'pr_open_avg_future'}, inplace=True)

res_train_data = res_agg.merge(feature, on=['ticker'], how='inner')
res_train_data['direction'] = (res_train_data['pr_open_avg_future'] - res_train_data['pr_open_avg'] > 0).astype(int)

from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=4)
clf.fit(res_train_data.drop(['ticker','pr_open_avg_future','direction'], axis=1), res_train_data['direction'])

y_pred = clf.predict(res_predict_agg.drop(['ticker', 'result'], axis=1))

res_predict_agg['result'] = y_pred

res_predict_agg[res_predict_agg['result'] == 1]['ticker'].unique()

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

store = res_train_data.drop(['ticker','pr_open_avg_future','direction'], axis=1)


plt.figure(figsize=(20,10))
plot_tree(clf, filled=True, feature_names=store.columns, rounded=True)
plt.show()

    """
    tickers_positive = ['AFKS', 'AQUA', 'ASSB', 'BANE', 'CBOM', 'ENPG', 'GAZP', 'GAZT',
                        'HHRU', 'INGR', 'JNOS', 'KBSB', 'KGKC', 'KRKOP', 'KZOSP', 'LKOH',
                        'MGTS', 'MOEX', 'MRKZ', 'MSNG', 'MTLR', 'MVID', 'NKNCP', 'OZON',
                        'PIKK', 'RASP', 'RDRB', 'ROSN', 'ROST', 'SAGO', 'SBER', 'SFIN',
                        'SGZH', 'SIBN', 'SMLT', 'SNGSP', 'SVET', 'TORS', 'TRNFP', 'UKUZ',
                        'WTCM', 'WTCMP', 'YNDX']
    return ticker in tickers_positive
