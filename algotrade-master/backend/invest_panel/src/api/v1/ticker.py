from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.containers.invest import ServiceContainer
from src.services.ticker import TickerService
from src.models.ticker import Ticker, TickerBrief


router = APIRouter(prefix='/ticker', tags=['Ticker info'])


@router.get(path='s', name='Get all tickers', response_model=list[TickerBrief])
@inject
async def get_all_tickers(
    ticker_service: TickerService = Depends(Provide[ServiceContainer.ticker_service])
) -> list[TickerBrief]:

    tickers = await ticker_service.all()
    return [TickerBrief(
        id=ticker.id,
        secid=ticker.secid,
        boardid=ticker.boardid,
        shortname=ticker.shortname,
    ) for ticker in tickers]


@router.get(path='', name='Get one ticker', response_model=Ticker)
@inject
async def get_one_ticker(
    secid: str,
    ticker_service: TickerService = Depends(Provide[ServiceContainer.ticker_service]),
) -> Ticker:  
    ticker = await ticker_service.get(secid=secid)
    
    return Ticker(
        id=ticker.id,
        secid=ticker.secid,
        boardid=ticker.boardid,
        shortname=ticker.shortname,
        prevprice=ticker.prevprice,
        lotsize=ticker.lotsize,
        facevalue=ticker.facevalue,
        status=ticker.status,
        boardname=ticker.boardname,
        decimials=ticker.decimials,
        secname=ticker.secname,
        remarks=ticker.remarks,
        marketcode=ticker.marketcode,
        instrid=ticker.instrid,
        sectorid=ticker.sectorid,
        minstep=ticker.minstep,
        prevwaprice=ticker.prevwaprice,
        faceunit=ticker.faceunit,
        prevdate=ticker.prevdate,
        issuesize=ticker.issuesize,
        isin=ticker.isin,
        latname=ticker.latname,
        regnumber=ticker.regnumber,
        prevlegalcloseprice=ticker.prevlegalcloseprice,
        currencyid=ticker.currencyid,
        sectype=ticker.sectype,
        listlevel=ticker.listlevel,
        settledate=ticker.settledate,
    )
