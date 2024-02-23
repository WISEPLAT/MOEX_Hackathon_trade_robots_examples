from sqlalchemy.orm import Session

from models.bot import Bot as BotBase
from dto.bot import Bot as BotModel

from models.bot_stock import BotStocks as BotStocksBase
from dto.bot_stock import BotStocks as BotStocksModel
from models.bot_action import BotAction as BotActionBase
from dto.bot_action import BotAction as BotActionModel

from fastapi import HTTPException


def add_bot(data: BotModel, db: Session):
    bot = BotBase(
        user_id=data.user_id, state=data.state,
        date_to=data.date_to, risk_level=data.risk_level,
        initial_balance=data.initial_balance, current_balance=data.current_balance
    )

    db.add(bot)
    db.commit()
    db.refresh(bot)

    return bot


def get_bot_state(user_id: int, db: Session):
    bot = db.query(BotBase).filter(BotBase.user_id == user_id).first()

    if not bot:
        bot = add_bot(BotModel(user_id=user_id), db)

    return bot


def set_bot_state(data: BotModel, db: Session):
    bot = db.query(BotBase).filter(BotBase.user_id == data.user_id).first()

    if not bot:
        bot = add_bot(data, db)
    else:
        bot.state = data.state
        if data.date_to:
            bot.date_to = data.date_to
        if data.risk_level:
            bot.risk_level = data.risk_level
        if data.initial_balance:
            bot.initial_balance = data.initial_balance
        if data.current_balance:
            bot.current_balance = data.current_balance

        db.add(bot)
        db.commit()
        db.refresh(bot)

    return bot


def add_stock_info(data: BotStocksModel, db: Session):
    bot_stocks = BotStocksBase(
        user_id=data.user_id, company_name=data.company_name,
        stocks_count=data.stocks_count, purchase_price=data.purchase_price,
        current_price=data.current_price
    )

    db.add(bot_stocks)
    db.commit()
    db.refresh(bot_stocks)

    return bot_stocks


def update_stock_info(data: BotStocksModel, db: Session):
    bot_stocks = (db.query(BotStocksBase)
                  .filter(BotStocksBase.user_id == data.user_id)
                  .filter(BotStocksBase.company_name == data.company_name)
                  .first())

    if not bot_stocks:
        bot_stocks = add_stock_info(data, db)
    else:
        if data.stocks_count:
            bot_stocks.stocks_count = data.stocks_count
        if data.purchase_price:
            bot_stocks.purchase_price = data.purchase_price
        if data.current_price:
            bot_stocks.current_price = data.current_price

        db.add(bot_stocks)
        db.commit()
        db.refresh(bot_stocks)

    return bot_stocks


def get_all_stocks_info(user_id: int, db: Session):
    return db.query(BotStocksBase).filter(BotStocksBase.user_id == user_id).all()


def delete_stocks(user_id: int, company_name: str, db: Session):
    if company_name:
        stocks = (db.query(BotStocksBase)
                  .filter(BotStocksBase.user_id == user_id)
                  .filter(BotStocksBase.company_name == company_name)
                  .delete())
    else:
        stocks = (db.query(BotStocksBase)
                  .filter(BotStocksBase.user_id == user_id)
                  .delete())

    db.commit()

    return stocks


def get_bot_info(user_id: int, db: Session):
    bot = get_bot_state(user_id, db)

    bot_stocks = db.query(BotStocksBase).filter(BotStocksBase.user_id == user_id).all()

    result = {
        "initialBalance": bot.initial_balance,
        "currentBalance": bot.current_balance,
        "state": bot.state,
        "dateTo": bot.date_to,
        "riskLevel": bot.risk_level
    }

    stocks = []

    for stock in bot_stocks:
        stocks.append({
            "companyName": stock.company_name,
            "stocksCount": stock.stocks_count,
            "purchasePrice": stock.purchase_price,
            "currentPrice": stock.current_price
        })

    result["stocks"] = stocks

    return result


def update_balance(user_id: int, initial_balance: float, current_balance: float, db: Session):
    bot = db.query(BotBase).filter(BotBase.user_id == user_id).first()

    if not bot:
        bot = add_bot(BotModel(user_id=user_id, initial_balance=initial_balance, current_balance=current_balance), db)

    if initial_balance:
        bot.initial_balance = initial_balance
    if current_balance:
        bot.current_balance = current_balance

    db.add(bot)
    db.commit()
    db.refresh(bot)

    return bot


def add_bot_action(data: BotActionModel, db: Session):
    bot_action = BotActionBase(
        user_id=data.user_id,
        company_name=data.company_name,
        stocks_count=data.stocks_count,
        action=data.action.value,
        action_color=data.action_color.value,
        profit=data.profit,
        comment=data.comment,
        datetime=data.datetime
    )

    db.add(bot_action)
    db.commit()
    db.refresh(bot_action)

    return bot_action


def delete_bot_history(user_id: int, db: Session):
    bot_history = db.query(BotActionBase).filter(BotActionBase.user_id == user_id).delete()

    db.commit()

    return bot_history


def get_bot_history(user_id: int, db: Session):
    return db.query(BotActionBase).filter(BotActionBase.user_id == user_id).all()
