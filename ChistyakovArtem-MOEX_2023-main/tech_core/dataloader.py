from moexalgo import Ticker, Market
import pandas as pd

def load_ticker(sec, start, end, period, verbose=False):
    ticker = Ticker(sec)
    
    start_date = start
    df_list = []
    while True:
        if verbose == True:
            print(f'Loading {sec} from {start_date} to {end}')

        df = ticker.candles(date=start_date, till_date=end, period=period)
        if len(df) == 0:

            if verbose == True:
                print(f'No data for {sec} from {start_date} to {end}')
            break
        
        df_list.append(df)
        if df.index[-1] == end:
            break
        else:
            start_date = df['end'].tolist()[-1]

    df = pd.concat(df_list).reset_index(drop=True)

    return df
