from datetime import datetime, timedelta
from support.database import get_date_stActual, get_date_endActual
from support.date_format import convertStr, convertDate, sravDate
import pandas as pd

def date_range(instrument, param_date):
    dates = []
    dat_dateAct = get_date_stActual(instrument)
    dat_dateEndAct   = get_date_endActual(instrument)
    if dat_dateAct == '' :
        s_startDate = param_date[0]
    else:
        st_dateAct = convertStr(dat_dateAct)
        s_startDate = st_dateAct
    if dat_dateEndAct == '' :
        s_endDate = param_date[1]
    else:
        st_dateEndAct = convertStr(dat_dateEndAct)
        s_endDate = st_dateEndAct


    d_startDate = convertDate(s_startDate)
    d_endDate = convertDate(s_endDate)

    d_toDate = d_startDate
    while sravDate(d_toDate, d_endDate):
        s_toDate = convertStr(d_toDate)
        dates.append(s_toDate)
        d_toDate += timedelta(days=1)

    return dates

def processed_data(section, dates):
    try:
        if section is None:
            return

        #Date
        if section[0]['Date'] == dates:
            df = pd.DataFrame.from_records([
                {
                    "date": pd.to_datetime(dates.replace('.', '-'),  dayfirst=True), #utc=True,
                    "JurL": section[0]['JuridicalLong'].replace('\xa0', ''),
                    "JurS": section[0]['JuridicalShort'].replace('\xa0', ''),
                    "PhyL": section[0]['PhysicalLong'].replace('\xa0', ''),
                    "PhyS": section[0]['PhysicalShort'].replace('\xa0', ''),
                    "Summary": section[0]['Summary'].replace('\xa0', '')
                }
            ])
        else:
            df = pd.DataFrame.from_records([
                {
                    "date": pd.to_datetime(dates.replace('.', '-'),  dayfirst=True), #utc=True,
                    "JurL": 0,
                    "JurS": 0,
                    "PhyL": 0,
                    "PhyS": 0,
                    "Summary": 0
                }
            ])

        return df
    except Exception as ex:
        return ex

def create_empty_df() -> pd.DataFrame:

    df = pd.DataFrame(columns=["date","JurL", "JurS", "PhyL", "PhyS", "Summary"])
    df.date = pd.to_datetime(df.date, unit="ms")
    df.JurL = pd.to_numeric(df.JurL)
    df.JurS = pd.to_numeric(df.JurS)
    df.PhyL = pd.to_numeric(df.PhyL)
    df.PhyS = pd.to_numeric(df.PhyS)
    df.Summary = pd.to_numeric(df.Summary)
    return df


