from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from datetime import datetime
from typing import Annotated

from src.containers.candle import ServiceContainer as CandleServiceContainer
from src.containers.prediction import ServiceContainer as PredictionServiceContainer
from src.services.trades.candle import CandleService
from src.services.trades.prediction import PredictionService
from src.models.candle import CandleTS
from src.models.prediction import PredictionTS


router = APIRouter(prefix='/trades', tags=['Trade functions'])


@router.get(path='/ts/candle', name='Candle timeseries', response_model=list[CandleTS])
@inject
async def get_candle_ts(
    secid: str,
    ts: str,
    till_ts: str | None = None,
    interval: Annotated[str, Query(pattern='\d+\s+(?:hour|minute|day)')] = '1 minute',
    candle_service: CandleService = Depends(Provide[CandleServiceContainer.candle_service])
) -> list[CandleTS]:
    
    candles_gen = candle_service.get_time_series(
        secid=secid,
        fields=[
            'secid',
            'median(open) as open',
            'median(close) as close',
            'median(high) as high',
            'median(low) as low',
            'median(volume) as volume',
            'median(value) as value',
            f'toStartOfInterval(begin, INTERVAL {interval}) as begin'
        ],
        ts=datetime.fromisoformat(ts) if ts is not None else None,
        till_ts=datetime.fromisoformat(till_ts) if till_ts is not None else None,
        group_by=['secid', 'begin'],
        order_by={'desc': ['begin']}
    )

    return [candle async for candle in candles_gen]


@router.get(path='/ts/prediction', name='Prediction timeseries', response_model=list[PredictionTS])
@inject
async def get_prediction_ts(
    secid: str,
    ts: str,
    till_ts: str | None = None,
    interval: Annotated[str, Query(pattern='\d+\s+(?:hour|minute|day)')] = '1 minute',
    prediction_service: PredictionService = Depends(Provide[PredictionServiceContainer.prediction_service])
) -> list[PredictionTS]:
    
    prediction_gen = prediction_service.get_time_series(
        secid=secid,
        fields=[
            'secid',
            'algorithm',
            'median(value) as value',
            f'toStartOfInterval(timestamp, INTERVAL {interval}) as timestamp'
        ],
        ts=datetime.fromisoformat(ts) if ts is not None else None,
        till_ts=datetime.fromisoformat(till_ts) if till_ts is not None else None,
        group_by=['secid', 'algorithm', 'timestamp'],
        order_by={'desc': ['timestamp']}
    )

    return [candle async for candle in prediction_gen]
