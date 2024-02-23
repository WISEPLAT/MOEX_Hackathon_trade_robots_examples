import logging
import random
from typing import List

from fastapi import APIRouter, status
from tortoise.exceptions import DoesNotExist

from core.exceptions import NotFound
from core.models import Strategy, Backtest
from core.schemas.strategy import StrategyProgressResponse, BacktestRequest

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/backtest",
    status_code=status.HTTP_200_OK,
    response_model=int
)
async def start_backtesting(data: BacktestRequest):
    """Start backtesting"""
    ids = []
    backtest = await Backtest.create(date_start=data.date_start, date_end=data.date_end)
    for i in data.files:
        await Strategy.create(backtest=backtest, name=i.name, source=i.content)
    return backtest.pk


@router.get(
    "/{backtest_id}/progress",
    status_code=status.HTTP_200_OK,
    response_model=List[StrategyProgressResponse]
)
async def get_progress(backtest_id: int):
    """Progress bar by backtest id"""
    try:
        backtest = await Backtest.get(id=backtest_id)
    except DoesNotExist:
        raise NotFound()

    # get all strategies by backtest id
    strategies = await Strategy.filter(backtest=backtest)
    res = []
    for i in strategies:
        if random.randint(0, 1):
            res.append(StrategyProgressResponse(id=i.pk, status="done", profit=100500))
        res.append(StrategyProgressResponse(id=i.pk, status="progress", progress=random.random()))
    return res


