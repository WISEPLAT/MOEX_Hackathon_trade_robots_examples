import datetime
import logging
import random
from typing import List

from fastapi import APIRouter
from moexalgo import Market, Ticker
from starlette import status

from config.constants import get_sphere, get_name
from core.exceptions import BadRequest
from core.schemas.tickers import TickerResponse, TickerCandleResponse, RelevantTickerResponse, Period
from core.service.service import get_ticker_corr, get_is_ticker_good

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/",
    response_model=List[TickerResponse],
    status_code=status.HTTP_200_OK,
)
async def get_tickers():
    """Get a list of all MOEX tickers"""
    # TODO: cache this list via nginx or redis
    stocks = Market('stocks')
    tickers = stocks.tickers()

    data = [
        {
            "ticker": ticker["SECID"],
            "price": ticker["PREVLEGALCLOSEPRICE"],
            "name": get_name(ticker["SECID"]) if get_name(ticker["SECID"]) else ticker["SECNAME"],
            "sphere": get_sphere(ticker["SECID"]),
            "is_positive_forecast": get_is_ticker_good(ticker["SECID"])
        }
        for ticker in tickers
    ]
    return data


@router.get(
    "/{ticker}/relevant/",
    response_model=List[RelevantTickerResponse],
    status_code=status.HTTP_200_OK
)
async def get_relevant_tickers(ticker: str):
    """Get a list of relevant tickers for the specified ticker"""
    stocks = Market('stocks')
    tickers = stocks.tickers()
    tickers = {
        ticker["SECID"]: ticker
        for ticker in tickers
    }
    small_corr_tickers = get_ticker_corr(ticker.upper())
    data = [
        {
            "ticker": ticker_name,
            "price": tickers[ticker_name]["PREVLEGALCLOSEPRICE"],
            "name": get_name(ticker_name) if get_name(ticker_name) else tickers[ticker_name]["SECNAME"],
            "sphere": get_sphere(ticker_name),
            "is_positive_forecast": get_is_ticker_good(ticker_name),
            "correlation_score": corr,
        }
        for ticker_name, corr in small_corr_tickers
        if ticker_name in tickers
    ]
    return data


@router.get(
    "/{ticker}/",
    response_model=List[TickerCandleResponse],
    status_code=status.HTTP_200_OK,
)
async def get_price_for_ticker(ticker: str, date_start: datetime.date, date_end: datetime.date, period: Period):
    """Get price for ticker over time with specified frequency"""
    try:
        ticker = Ticker(ticker.upper())
    except LookupError:
        raise BadRequest(detail={"error": f"Ticker {ticker.upper()} not found"})

    candles = list(ticker.candles(date=date_start, till_date=date_end, period=period))
    return candles
