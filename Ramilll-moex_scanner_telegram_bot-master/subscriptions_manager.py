from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import List, Dict
from stocks_prices_manager import StocksPricesManager, StockPrice
import yfinance as yf

Base = declarative_base()

class UserSubscription(Base):
    # Определение таблицы для подписок пользователей
    __tablename__ = 'user_subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    stock_symbol = Column(String, nullable=False)

class SubscriptionsManager:
    def __init__(self, database_url='sqlite:///subscription_data.db'):
        # Инициализация менеджера подписок с указанием базы данных
        self.engine = create_engine(database_url, echo=True, connect_args={'check_same_thread': False})
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()

    def create_tables(self):
        # Создание необходимых таблиц в базе данных
        Base.metadata.create_all(self.engine, checkfirst=True)
        stock_manager = StocksPricesManager()
        stock_manager.create_tables()

    async def subscribe_user_to_stock(self, user_id: int, stock_symbol: str):
        session = self.Session()
        try:
            stock_manager = StocksPricesManager()

            # Проверка, существует ли символ акции в таблице stocks_prices
            if stock_manager.stock_exists(stock_symbol):
                existing_subscription = session.query(UserSubscription).filter_by(
                    user_id=user_id, stock_symbol=stock_symbol).first()

                # Проверка, не подписан ли пользователь уже
                if not existing_subscription:
                    # Добавление подписки в таблицу user_subscriptions
                    subscription = UserSubscription(user_id=user_id, stock_symbol=stock_symbol)
                    session.merge(subscription)
                    session.commit()
            else:
                # Если символ акции не существует, добавляем его в таблицу stocks_prices
                stock_data = yf.download(stock_symbol, period='1d', interval='1m')
                current_price = stock_data['Close'].iloc[-1]
                stock_manager.add_stock_price(symbol=stock_symbol, current_price=current_price)

                # Добавление подписки в таблицу user_subscriptions
                subscription = UserSubscription(user_id=user_id, stock_symbol=stock_symbol)
                session.merge(subscription)
                session.commit()
        finally:
            session.close()

    # Отмена подписки пользователя на акцию
    def unsubscribe_user_from_stock(self, user_id: int, stock_symbol: str):
        session = self.Session()
        try:
            # Отмена подписки пользователя на акцию
            session.query(UserSubscription).filter_by(user_id=user_id, stock_symbol=stock_symbol).delete()
            session.commit()
        finally:
            session.close()

    # Получение списка акций, на которые подписан пользователь
    def get_user_subscriptions(self, user_id: int) -> List[str]:
        session = self.Session()
        try:
            subscriptions = [sub.stock_symbol for sub in
                             session.query(UserSubscription).filter_by(user_id=user_id).all()]
            return [str(symbol) for symbol in subscriptions]
        finally:
              session.close()
