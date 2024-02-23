from datetime import datetime, timedelta
import time


def convertDate(strDate):
    try:
        d_Date = datetime.strptime(strDate, "%Y-%m-%d")
    except Exception as ex:
        print(ex)
    return d_Date

def sravDate(d_dateTo, d_dateEnd):
    keyBol = True
    if ((d_dateEnd - d_dateTo).days) < 0:
        keyBol = False
    return keyBol
def sravDateNot(s_dateStart, s_dateEnd):
    d_dateStart = convertDate(s_dateStart)
    d_dateEnd = convertDate(s_dateEnd)
    keyBol = True
    if d_dateStart == d_dateEnd:
        keyBol = False
    return keyBol

def sravBothDate(s_dateOne, s_dateTwo):
    d_dateOne = convertDate(s_dateOne)
    d_dateTwo = convertDate(s_dateTwo)
    keyBol = False
    if d_dateOne > d_dateTwo:
        keyBol = True
    return keyBol

def sravRealTime(pm_dateEnd):

    keyBol = False
    now = datetime.now()
    # now_date = now.strftime('%Y-%m-%d')
    pm_dateEnd_2 =  data_AddOneDay(pm_dateEnd)

    s_porog_time = f"{pm_dateEnd_2} 22:11:00"
    d_porog_time = datetime.strptime(s_porog_time, '%Y-%m-%d %H:%M:%S')

    if now >= d_porog_time:
        keyBol = True
    return keyBol
def convertStr(d_Date):
    s_Date = d_Date.strftime("%Y-%m-%d")
    return s_Date

def convForRequest(strDate):
    d_Date = datetime.strptime(strDate, "%Y-%m-%d")
    strDate2 = d_Date.strftime("%d.%m.%Y")
    return strDate2
def convertTimestampDate(timestamp):
    strDate = str(timestamp)
    d_Date = datetime.strptime(strDate, '%Y-%m-%d %H:%M:%S')
    s_Date2 = d_Date.strftime("%Y-%m-%d")
    return s_Date2

def check_correct(row_series):
    key = True

    b_JurL = str(row_series['JurL'])
    b_JurS = str(row_series['JurS'])
    b_PhyL = str(row_series['PhyL'])
    b_PhyS = str(row_series['PhyS'])

    if b_JurL.find(",") >= 0 :
        key = False
    if b_JurS.find(",") >= 0 :
        key = False
    if b_PhyL.find(",") >= 0 :
        key = False
    if b_PhyS.find(",") >= 0 :
        key = False
    return key

def data_AddOneDay(strDate):
    s_Date = ''
    try:
        d_Date = datetime.strptime(strDate, "%Y-%m-%d")
        new_date = d_Date + timedelta(days=1)
        s_Date = new_date.strftime("%Y-%m-%d")

    except Exception as ex:
        print(ex)
    return s_Date
def data_MinusOneDay(strDate):
    s_Date = ''
    try:
        d_Date = datetime.strptime(strDate, "%Y-%m-%d")
        new_date = d_Date - timedelta(days=1)
        s_Date = new_date.strftime("%Y-%m-%d")

    except Exception as ex:
        print(ex)
    return s_Date