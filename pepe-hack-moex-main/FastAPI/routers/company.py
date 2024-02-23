from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services import company as CompanyService

router = APIRouter()


@router.post("/", tags=["company"])
async def create_company(ticker: str, db: Session = Depends(get_db)):
    return CompanyService.create_company(ticker, db)


@router.get("/", tags=["company"])
async def get_all_companies(db: Session = Depends(get_db)):
    return CompanyService.get_all_companies(db)


@router.get("/{ticker}", tags=["company"])
async def get_company(ticker: str = None, db: Session = Depends(get_db)):
    return CompanyService.get_company(ticker, db)


@router.delete("/{ticker}", tags=["company"])
async def delete_company(ticker: str = None, db: Session = Depends(get_db)):
    return CompanyService.remove_company(ticker, db)
