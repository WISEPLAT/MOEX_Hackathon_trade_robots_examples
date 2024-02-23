from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services import stock as StockService
from dto.stock import StocksType

router = APIRouter()


@router.get("/", tags=["stocks"])
async def get_all_stocks(db: Session = Depends(get_db)):
    return StockService.get_all_stocks(db)


@router.get("/{stocks_type}", tags=["stocks"])
async def get_top_stocks(db: Session = Depends(get_db), stocks_type: StocksType = None, limit: int = None):
    return StockService.get_top_stocks(db, stocks_type, limit)
