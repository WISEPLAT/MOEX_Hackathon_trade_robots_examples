from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services import stockchart as StockchartService

router = APIRouter()


@router.get("/{ticker}", tags=["stockchart"])
async def get_stockchart(ticker: str = None, date_from: str = None, date_to: str = None, db: Session = Depends(get_db)):
    return StockchartService.get_stockchart(ticker, db, date_from, date_to)
