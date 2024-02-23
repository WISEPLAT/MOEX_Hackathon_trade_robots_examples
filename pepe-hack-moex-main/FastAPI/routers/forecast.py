from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services import forecast as ForecastService
from dto.forecast import Forecast as ForecastModel
from dto.forecast import ForecastPeriod

router = APIRouter()


@router.get("/", tags=["forecast"])
async def get_all_forecasts(db: Session = Depends(get_db)):
    return ForecastService.get_all_forecasts(db)


@router.post("/{ticker}", tags=["forecast"])
async def insert_forecast(data: ForecastModel = None, db: Session = Depends(get_db)):
    return ForecastService.insert_forecast(data, db)


@router.delete("/{ticker}", tags=["forecast"])
async def delete_forecast(ticker: str = None, period: ForecastPeriod = None, db: Session = Depends(get_db)):
    return ForecastService.delete_forecast(db, ticker, period)
