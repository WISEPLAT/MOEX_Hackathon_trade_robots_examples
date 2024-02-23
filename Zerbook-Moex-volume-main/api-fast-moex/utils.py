import pandas as pd
from date_format import convertStr

def create_empty_df() -> pd.DataFrame:
    df = pd.DataFrame(columns=["instrument", "date", "jurl", "jurs", "phyl", "phys", "summary"])
    # df.date = pd.to_datetime(df.date)
    # df.time = pd.to_datetime(df.time, unit="ms")
    # df.price = pd.to_numeric(df.price)
    # df.quantity = pd.to_numeric(df.quantity)

    #pd.to_datetime
    return df

def processed_data(result):
    try:
        # if trade is None:
        #     return


        data = pd.DataFrame.from_records([     # создается фрейм
            {
                "instrument": result[0],
                "date": convertStr(result[1]),
                "jurl": result[2],
                "jurs": result[3],
                "phyl": result[4],
                "phys": result[5],
                "summary": result[6]
            }
        ])

        return data
    except Exception as ex:
        return ex