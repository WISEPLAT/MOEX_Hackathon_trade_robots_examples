from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services import stocks_catalog as StocksCatalogService

router = APIRouter()


@router.get("/", tags=["stocks-catalog"])
async def get_stocks_catalog_page(db: Session = Depends(get_db),
                                  limit: int = None, page: int = None, search_value: str = None):
    return StocksCatalogService.get_stocks_catalog_page(db, limit, page, search_value)
