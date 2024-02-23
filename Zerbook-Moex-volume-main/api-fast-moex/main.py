import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from date_format import convertStr
from datetime import datetime, timedelta

from database import get_dateAllInstr, get_deltaJur



api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#@api.get('/{interval}&{interval2}')
@api.get('/root')
async def root():
    dicts = {}

    end_d = datetime.now()
    start_d = end_d - timedelta(days=30)
    start_date = convertStr(start_d)
    end_date = convertStr(end_d)

    deltaJur = get_deltaJur('RTS', start_date, end_date)

    obj1 = json.dumps({'idx': 'RuTeSu'})
    dict1 = json.loads(obj1)

    dict2 = json.loads(deltaJur)

    dicts['name'] = dict1
    dicts['data'] = dict2

    json_data = json.dumps(dicts)
    return json_data
    # return {"user_name": index}


@api.get("/deltajur")
def get_jsondjur(index, bars):
    # bars = int(bars)
    # bars = bars + 33
    bars = int(bars)
    end_d = datetime.now()
    start_d = end_d - timedelta(days=bars)
    start_date = convertStr(start_d)
    end_date = convertStr(end_d)
    deltaJur = get_deltaJur(index, start_date, end_date)
    return deltaJur



    # return {"name_index": index, "Бары": bars}