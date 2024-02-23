import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import desc
from moexalgo import Ticker
from datetime import datetime, date, timedelta

from services.company import get_all_companies, get_company

from models.stock import Stock as StockBase
from models.forecast import Forecast as ForecastBase
from models.company import Company as CompanyBase
from dto.stock import Stock as StockModel
from dto.stock import StocksType
from dto.forecast import ForecastPeriod

from random import randint


def get_all_stocks(db: Session):
    return db.query(StockBase).all()


def get_stock(ticker: str, db: Session):
    return db.query(StockBase).filter(StockBase.ticker == ticker).first()


def add_stock(data: StockModel, db: Session):
    stock = StockBase(ticker=data.ticker, price=data.price, price_increase=data.price_increase)

    db.add(stock)
    db.commit()
    db.refresh(stock)

    return stock


def update_stock(data: StockModel, db: Session):
    stock = db.query(StockBase).filter(StockBase.ticker == data.ticker).first()

    if not stock:
        stock = add_stock(data, db)
    else:
        stock.price = data.price
        stock.price_increase = data.price_increase

        db.add(stock)
        db.commit()
        db.refresh(stock)

    return stock


def get_stock_data_by_ticker(ticker: str):
    ticker_data = Ticker(ticker)

    datetime_now = datetime.now()

    if datetime_now.weekday() > 4:
        sub_days = datetime_now.weekday() - 4
    elif datetime_now.hour < 10:
        sub_days = 1
    else:
        sub_days = 0

    date_iso = (date.today() - timedelta(days=sub_days)).isoformat()

    candles = ticker_data.candles(date=date_iso, period='D')

    if not isinstance(candles, pd.DataFrame):
        candles = pd.DataFrame(candles)

    price = 0
    price_increase = 0

    if not candles.empty:
        candles = candles.iloc[0]

        price = candles.close
        price_increase = (candles.close - candles.open) / candles.open

    return price, price_increase


def update_all_stocks(db: Session):
    for company_data in get_all_companies(db):
        price, price_increase = get_stock_data_by_ticker(company_data.ticker)

        update_stock(StockModel(**{
                "ticker": company_data.ticker,
                "price": price,
                "price_increase": price_increase
            }), db)


def get_top_stocks(db: Session, stocks_type: StocksType, limit: int = None):
    joined_result = []

    if stocks_type == StocksType.RISING:
        joined_result = (
            db.query(StockBase, CompanyBase)
            .select_from(StockBase)
            .filter(StockBase.price_increase > 0)
            .order_by(desc(StockBase.price_increase))
            .join(CompanyBase)
            .limit(limit)
            .all()
        )

    elif stocks_type == StocksType.FALLING:
        joined_result = (
            db.query(StockBase, CompanyBase)
            .select_from(StockBase)
            .filter(StockBase.price_increase < 0)
            .order_by(StockBase.price_increase)
            .join(CompanyBase)
            .limit(limit)
            .all()
        )

    result = []

    for stock, company in joined_result:
        result.append({
            "price": stock.price,
            "pricePercentage": round(stock.price_increase * 100, 1),
            "companyName": company.name,
            "companyIcon": company.icon,
            "id": company.ticker
        })

    return result


def get_stock_with_forecasts(ticker: str, db: Session):
    company = get_company(ticker, db)

    if company is None:
        return

    forecasts = db.query(ForecastBase).filter(ForecastBase.ticker == ticker).all()

    forecast_dict = {}

    # БАЗИРОВАННЫЕ ПРОГНОЗЫ
    # for period in ForecastPeriod:
    #     forecast_dict[period] = {
    #         "price": randint(1, 2000),
    #         "changePercentage": randint(0, 100)
    #     }

    for forecast in forecasts:
        forecast_dict[forecast.period] = {
            "price": forecast.price,
            "changePercentage": forecast.price_increase
        }

    result = {
        "id": ticker,
        "description": company.description,
        "forecast": forecast_dict,
        "companyName": company.name,
        "companyIcon": company.icon,
        "background": company.background.split(": ")[-1],
        "textColor": company.text_color.split(": ")[-1]
    }

    return result
