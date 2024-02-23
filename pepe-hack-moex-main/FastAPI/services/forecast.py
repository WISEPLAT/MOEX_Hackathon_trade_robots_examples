from sqlalchemy.orm import Session

from models.forecast import Forecast as ForecastBase
from dto.forecast import Forecast as ForecastModel
from dto.forecast import ForecastPeriod


def add_forecast(data: ForecastModel, db: Session):
    forecast = ForecastBase(
        ticker=data.ticker,
        period=data.period.value,
        price=data.price,
        price_increase=data.price_increase
    )

    db.add(forecast)
    db.commit()
    db.refresh(forecast)

    return forecast


def get_all_forecasts(db: Session):
    return db.query(ForecastBase).all()


def insert_forecast(data: ForecastModel, db: Session):
    forecast = (db.query(ForecastBase)
                .filter(ForecastBase.ticker == data.ticker)
                .filter(ForecastBase.period == str(data.period.value))
                .first())

    if not forecast:
        forecast = add_forecast(data, db)

    forecast.price = data.price
    forecast.price_increase = data.price_increase

    db.add(forecast)
    db.commit()
    db.refresh(forecast)

    return forecast


def delete_forecast(db: Session, ticker: str, period: ForecastPeriod = None):
    forecast = db.query(ForecastBase).filter(ForecastBase.ticker == ticker)

    if period:
        forecast = forecast.filter(ForecastBase.period == str(period.value))

    forecast.delete()

    db.commit()

    return forecast
