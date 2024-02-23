from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from datetime import date, datetime

from database import get_db
from services import bot as BotService
from dto.bot import BotState, Bot as BotModel
from dto.bot_stock import BotStocks as BotStocksModel
from dto.bot_action import BotActionType, BotActionColor, BotAction as BotActionModel

router = APIRouter()


@router.post("/start", tags=["bot"])
async def start_bot(user_id: int = 0, date_to: datetime | date = date.today(),
                    risk_level: int = Query(default=3, ge=0, le=5),
                    db: Session = Depends(get_db)):
    data = BotModel(
        user_id=user_id, state=BotState.ON,
        date_to=date_to.isoformat(), risk_level=risk_level
    )

    return BotService.set_bot_state(data, db)


@router.post("/stop", tags=["bot"])
async def stop_bot(user_id: int = 0, db: Session = Depends(get_db)):
    data = BotModel(
        user_id=user_id, state=BotState.OFF
    )

    return BotService.set_bot_state(data, db)


@router.post("/balance", tags=["bot"])
async def update_balance(user_id: int = 0,
                         initial_balance: float = Query(ge=0, default=None),
                         current_balance: float = Query(ge=0, default=None), db: Session = Depends(get_db)):
    return BotService.update_balance(user_id, initial_balance, current_balance, db)


@router.post("/stocks", tags=["bot"])
async def update_stock_info(user_id: int = 0, company_name: str = None,
                            stocks_count: int = None,
                            purchase_price: float = None, current_price: float = None,
                            db: Session = Depends(get_db)):
    data = BotStocksModel(
        user_id=user_id,
        company_name=company_name,
        stocks_count=stocks_count,
        purchase_price=purchase_price,
        current_price=current_price
    )

    return BotService.update_stock_info(data, db)


@router.get("/stocks", tags=["bot"])
async def get_all_stocks_info(user_id: int = 0, db: Session = Depends(get_db)):
    return BotService.get_all_stocks_info(user_id, db)


@router.delete("/stocks", tags=["bot"])
async def delete_stocks(user_id: int = 0, company_name: str = None, db: Session = Depends(get_db)):
    return BotService.delete_stocks(user_id, company_name, db)


@router.get("/", tags=["bot"])
async def get_bot_info(user_id: int = 0, db: Session = Depends(get_db)):
    return BotService.get_bot_info(user_id, db)


@router.post("/history", tags=["bot"])
async def add_bot_action(user_id: int = 0, company_name: str = "Яндекс",
                         stocks_count: int = Query(ge=0, default=0),
                         action: BotActionType = BotActionType.PURCHASE,
                         action_color: BotActionColor = BotActionColor.GREEN,
                         profit: float = 2.28, comment: str = "Комментарий",
                         action_datetime: datetime | date = datetime.now(),
                         db: Session = Depends(get_db)):
    data = BotActionModel(
        user_id=user_id,
        company_name=company_name,
        stocks_count=stocks_count,
        action=action,
        action_color=action_color,
        profit=profit,
        comment=comment,
        datetime=action_datetime
    )

    return BotService.add_bot_action(data, db)


@router.delete("/history", tags=["bot"])
async def delete_bot_history(user_id: int = 0, db: Session = Depends(get_db)):
    return BotService.delete_bot_history(user_id, db)


@router.get("/history", tags=["bot"])
async def get_bot_history(user_id: int = 0, db: Session = Depends(get_db)):
    return BotService.get_bot_history(user_id, db)
