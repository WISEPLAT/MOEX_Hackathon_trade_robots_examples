import pandas as pd
import numpy as np
import time
from backtesting import Strategy
from backtesting.lib import dateutils

class SimpleStrategy(Strategy):
   def __init__(self):
       super().__init__()
       self.tradestats = None

   def init(self, tradestats_path):
       # Load the pre-downloaded trade statistics data from the provided path
       self.tradestats = pd.read_csv(tradestats_path)
       # Perform any necessary data preprocessing or initialization

   def next(self, tradestats):
       # Calculate indicators based on the trade statistics data
       if len(self.tradestats) > 0:
           # Example 1: Calculate simple moving average (SMA) of closing prices
           window = 20
           if len(self.tradestats) >= window:
               self.tradestats['SMA'] = self.tradestats['pr_close'].rolling(window=window).mean()
       
           # Example 2: Calculate the relative strength index (RSI) of the price data
           delta = self.tradestats['pr_close'].diff()
           gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
           loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
           RS = gain / loss
           self.tradestats['RSI'] = 100 - (100 / (1 + RS))

   def stop(self, tradestats, order):
       # Define exit conditions based on the calculated indicators or other criteria
       if len(self.tradestats) > 0:
           last_entry = self.tradestats.iloc[-1]
           # Example 1: Exit condition based on the SMA crossover
           if last_entry['pr_close'] < last_entry['SMA']:
               self.sell()

           # Example 2: Condition based on the RSI crossing over 70 from above
           if last_entry['RSI'] > 70:
               self.sell()

# Download and store trade statistics data
dates = ['2023-11-20', '2023-11-21', '2023-11-22', '2023-11-23', '2023-11-24']
tradestats = pd.DataFrame()
for date in dates:
   print(date)
   # Request returns no more than 1000 records, to get all records using a cursor
   for cursor in range(25):
       url = f'https://iss.moex.com/iss/datashop/algopack/eq/tradestats.csv?date={date}&start={cursor*1000}&iss.only=data'
       df = pd.read_csv(url, sep=';', skiprows=2)
       tradestats = pd.concat([tradestats, df])
       if df.shape[0] < 1000:
           break
       time.sleep(0.5)

# Save the downloaded trade statistics data to a CSV file
tradestats.to_csv('tradestats.csv', index=None)

# Create an instance of the strategy and run backtesting
if __name__ == "__main__":
   strategy = SimpleStrategy()
   tradestats_path = 'tradestats.csv'  # Path where the trade statistics data is saved
   strategy.init(tradestats_path)  # Initialize the strategy with the trade statistics data
   strategy.next(tradestats)  # Calculate indicators based on the trade statistics data
   strategy.stop(tradestats, order)  # Define exit conditions and run backtesting
