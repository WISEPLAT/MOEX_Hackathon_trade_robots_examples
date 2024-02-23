from fastapi import APIRouter

from .tickers import router as router_tickers
from .backtest import router as router_backtest
from .news import router as router_news

router = APIRouter()
router.include_router(router_tickers, prefix="/tickers", tags=["tickers"])
router.include_router(router_backtest, prefix="/backtest", tags=["backtest"])
router.include_router(router_news, prefix="/news", tags=["news"])

