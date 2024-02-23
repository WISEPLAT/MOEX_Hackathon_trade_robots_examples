import os

import numpy as np
import pandas as pd

import requests
from io import StringIO
import matplotlib.pyplot as plt

from datetime import datetime
from dateutil.relativedelta import relativedelta
from tech_core.dataloader import load_ticker
import pickle

class Alpha:
    def __init__(self, trading_mode, neutralization, alpha_class):
        assert trading_mode in ['overnight']
        assert neutralization in [None, 'sector', 'board', 'market']

        self.trading_mode = trading_mode
        self.neutralization = neutralization
        self.alpha_class = alpha_class

class Memory:
    def __init__(self, window=None):
        self.memory_dict = {}
        self.window = window

    def update(self, ticker, row):
        if ticker in self.memory_dict:
            self.memory_dict[ticker] = pd.concat([self.memory_dict[ticker], pd.DataFrame([row])])
        else:
            self.memory_dict[ticker] = pd.DataFrame([row])
        
        if self.window is not None:
            self.memory_dict[ticker] = self.memory_dict[ticker].iloc[-self.window:]
        
        return self.memory_dict[ticker]
        

class AlphaManager:
    def load_intraday_data(self, sectors_df):
        intraday_data = {}
        for i in sectors_df['SECID']:
            date_now = datetime.now().date()
            date_prev = date_now - relativedelta(days=1)
            date_5yrs_ago = date_now - relativedelta(years=5)
            
            tmp = load_ticker(i, date_5yrs_ago, date_prev, '1D')
            tmp['next_open'] = tmp['open'].shift(-1)
            tmp = tmp.set_index('begin').sort_index().drop(columns=['end'])

            intraday_data[i] = tmp
        return intraday_data

    def transform_to_alpha_data(self, intraday_data):
        all_dates = set()
        for i in intraday_data.values():
            all_dates.update(i.index)
        all_dates = sorted(all_dates)

        new_data = {}
        for i in all_dates:
            day_data = {}
            for ticker, data in intraday_data.items():
                if i in data.index:
                    day_data[ticker] = data.loc[i]
                else:
                    day_data[ticker] = None
            new_data[i] = day_data
        return new_data

    @staticmethod
    def load_sectors_from_drive():
        url = 'https://drive.google.com/uc?export=download&id=1_WctZcCA-oeT9mJLcQ1EdalzXB3rxKxx'
        response = requests.get(url)
        
        assert response.status_code == 200, 'Error while downloading: {}, try manually download: {}'.format(response.status_code, url)
        data = StringIO(response.text)
        df = pd.read_csv(data)
        
        return df

    def __init__(self, fees=0.0004, inflation=0.15, sectors_df=None, verbose=True, alphas_folder='alphas'):

        if sectors_df is None:
            if verbose:
                print('Downloading the sectors_df from the cloud')
            sectors_df = AlphaManager.load_sectors_from_drive()
    
        if verbose:
            print(f'Loading Data. This code will take ~{round(2/74 * len(sectors_df), 2)} minutes to run')
        
        intraday_data = self.load_intraday_data(sectors_df)
        self.data = self.transform_to_alpha_data(intraday_data)

        self.fees = fees
        self.inflation = inflation
        self.verbose = verbose
        if not os.path.exists(alphas_folder):
            # Create the directory
            os.mkdir(alphas_folder)

        self.sector_dict = dict(zip(sectors_df['SECID'], sectors_df['sector']))
        self.board_dict = dict(zip(sectors_df['SECID'], sectors_df['BOARDID']))

    def compute_pnl_and_amount(self, logs):

        pnl_logs = []
        used_amount_logs = []

        for data, output in zip(self.data.values(), logs):
            #display(data)
            
            amount_used_in_day = 0
            pnl_day = 0
            for ticker, resp_output in zip(output['ticker'], output['output_scaled']):
                if data[ticker] is None:
                    continue

                if np.isnan(data[ticker]['next_open']):
                    break

                if resp_output > 0:
                    buy_price = data[ticker]['close'] * (1 + self.fees)
                    sell_price = data[ticker]['next_open'] * (1 - self.fees)
                    amount = resp_output / buy_price

                    pnl_day += (sell_price - buy_price) * amount
                    amount_used_in_day += buy_price * abs(amount)

                elif resp_output < 0:
                    sell_price = data[ticker]['close'] * (1 - self.fees)
                    buy_price = data[ticker]['next_open'] * (1 + self.fees)
                    amount = resp_output / sell_price

                    pnl_day += (sell_price - buy_price) * abs(amount)
                    amount_used_in_day += sell_price * abs(amount)
                else:
                    pnl_day += 0
                    amount_used_in_day += 0
            
            pnl_logs.append(pnl_day)
            used_amount_logs.append(amount_used_in_day)
        
        return pnl_logs, used_amount_logs
    
    def compute_metrics(self, pnl_logs, used_amount_logs):

        def calculate_sharpe_ratio(pnl, used_amount_logs, annual_risk_free_rate=0.0):

            def annual_to_daily_rate(annual_rate):
                return (1 + annual_rate) ** (1/252) - 1
            
            daily_risk_free_rate = annual_to_daily_rate(annual_risk_free_rate)

            alternative = used_amount_logs * daily_risk_free_rate

            std_deviation = np.std(pnl)

            sharpe_ratio = np.mean(pnl - alternative)*np.sqrt(252) / std_deviation if std_deviation != 0 else np.nan

            return sharpe_ratio

        pnl_logs = np.array(pnl_logs)
        used_amount_logs = np.array(used_amount_logs)
        
        sharpe_casual = calculate_sharpe_ratio(pnl_logs, used_amount_logs, annual_risk_free_rate=0)
        sharpe = calculate_sharpe_ratio(pnl_logs, used_amount_logs, annual_risk_free_rate=self.inflation)
        max_drawdown = (pnl_logs.cumsum() - np.maximum.accumulate(pnl_logs.cumsum())).min()

        return_to_drawdown = np.sum(pnl_logs) / abs(max_drawdown)
        
        return sharpe_casual, sharpe, return_to_drawdown

    @staticmethod
    def plot_pnl(pnl_logs, day_logs):
        plt.figure(figsize=(15, 10))
        plt.plot(day_logs, np.cumsum(pnl_logs))
        plt.title('PnL')
        plt.xlabel('Date')
        plt.ylabel('PnL')
        plt.grid()
        plt.show()

    def execute(self, alpha, verbose=True):
        def neutralize(data, neutralization):
            def dict_neutralize(data, dict_,):
                data['column_name'] = data['ticker'].map(dict_)
                mean = data.groupby('column_name')['output'].mean()
                data['mean'] = data['column_name'].map(mean)
                data['output_scaled'] = data['output'] - data['mean']
                return data[['ticker', 'output_scaled']]
            
            data = data.copy()
            if neutralization is None:
                data['output_scaled'] = data['output']
                return data[['ticker', 'output_scaled']]
            elif neutralization == 'sector':    
                return dict_neutralize(data, self.sector_dict)
            elif neutralization == 'board':
                return dict_neutralize(data, self.board_dict)
            elif neutralization == 'market':
                data['output_scaled'] = data['output'] - data['output'].mean()
                return data[['ticker', 'output_scaled']]
            else:
                raise ValueError('Unknown neutralization method')
    
        day_logs = []
        logs = []
        for day, data in self.data.items():
            delta_position = {}
            for ticker, row in data.items():
                if row is None:
                    delta_position[ticker] = 0
                else:
                    row_ = row.copy()
                    row_['next_open'] = np.nan
                    delta_position[ticker] = alpha.alpha_class(ticker, row)
            
            delta_position = pd.DataFrame({
                'ticker': delta_position.keys(),
                'output': delta_position.values()
            })
            delta_position = neutralize(delta_position, alpha.neutralization)
            day_logs.append(day)
            logs.append(delta_position)
        
        if not verbose:
            return 

        pnl_logs, used_amount_logs = self.compute_pnl_and_amount(logs)
        sharpe_casual, sharpe, return_to_drawdown = self.compute_metrics(pnl_logs, used_amount_logs)
        print(f'Sharpe (no inflation): {sharpe_casual}')
        print(f'Sharpe (normal): {sharpe}')
        print(f'Return to Drawdown: {return_to_drawdown}')
        
        print()

        print('Feedback')
        if sharpe_casual < 0:
            print('This strategy is losing money, try to improve it, Sharpe(no inflation) is negative')
        elif sharpe_casual > 0 and sharpe < 0:
            print('This strategy earns money, but less that you can earn on risk-free rate, try to improve it')
        elif 0 < sharpe < 1:
            print(f'This strategy earn money even more than risk-free rate, but still not enough, try to improve it, your Sharpe is {sharpe}, need to be more than 1')
        elif sharpe > 1:
            if return_to_drawdown < 1.5:
                print(f'Your strategy is good, but it is too risky, try to improve it, your return to drawdown is {return_to_drawdown}, need to be more than 1.5')
            else:
                print('Your strategy is good, you can try to improve it, but it is not necessary, now you can use it in real trading')
                
                while True:
                    response = input('Do you want to deploy it? (y/n)')
                    if response == 'y':
                        path = input('Enter the path to the file, you want to save the strategy (without extension):')
                        path = path + '.pkl'
                        with open(path, 'wb') as file:
                            pickle.dump(alpha, file)
                        print(f'Your strategy was saved to the file {path}')

                        print(f'Watch for news about deployment, it will be added soon')
                        break
                    elif response == 'n':
                        print('Ok, you can try to improve it')
                        break
                    else:
                        print('Unknown command, try again')
        else:
            print('Unknown error, try again')

        AlphaManager.plot_pnl(pnl_logs, day_logs)
