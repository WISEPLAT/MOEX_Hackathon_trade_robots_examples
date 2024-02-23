from tqdm import tqdm
import pandas as pd
import os
from backtesting import Backtest, Strategy


def load_ticker_data(path2data: str):
    data = pd.read_csv(path2data)
    data = data[['begin', 'open', 'high', 'low', 'close', 'volume']]
    data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    return data


def backtest_strategy(CustomStrategy, strategy_name: str) -> pd.DataFrame:
    processed_tickers = []
    tickers_stats = []
    tickers = os.listdir('data/d1/')
    for ticker in tqdm(tickers):
        try:
            ticker_name = ticker.split('.')[0]
            data = load_ticker_data(f'data/d1/{ticker}')
            bt = Backtest(data, CustomStrategy, commission=.002, exclusive_orders=True)
            ticker_result = bt.run()
            tickers_stats.append(ticker_result)
            processed_tickers.append(ticker_name)
        except Exception as e:
            print(ticker)
            print(e)
    
    tickers_stats = pd.DataFrame(tickers_stats)
    # tickers_stats['ticker'] = processed_tickers
    tickers_stats.insert(0, 'ticker', processed_tickers)

    tickers_stats.to_csv(f'strategies/{strategy_name}.csv', index=False)
    return tickers_stats


def check_strategy(path2stat: str):
    stat = pd.read_csv(path2stat)
    # print(stat[['# Trades', 'Duration', 'Return [%]', 'Win Rate [%]', 'Max. Drawdown [%]', 'Sharpe Ratio']].describe())
    return stat[['# Trades', 'Duration', 'Return [%]', 'Win Rate [%]', 'Max. Drawdown [%]', 'Sharpe Ratio']].describe()