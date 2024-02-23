import yfinance as yf
from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import List, Dict
import asyncio

Base = declarative_base()

class StockPrice(Base):
    __tablename__ = 'stocks_prices'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)
    current_price = Column(Float, default=0.0)

class StocksPricesManager:
    def __init__(self, database_url='sqlite:///stocks_prices.db'):
        self.engine = create_engine(database_url, echo=True, connect_args={'check_same_thread': False})
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()

    def create_tables(self):
        Base.metadata.create_all(self.engine, checkfirst=True)

    # Можно через метод start_update_all_stocks асинхронно обновляет цены тикеров
    def start_update_all_stocks(self, interval_seconds: int = 60):
        asyncio.create_task(self.update_all_stocks(interval_seconds))
        
    # Обновляет цены всех акции на таблице stocks_prices
    async def update_all_stocks(self, interval_seconds: int = 60):
        while True:
            try:
                # Получает все названий тикеров
                symbols = self.get_all_stock_symbols()

                # Обновляет текущие цены на каждую акцию
                for symbol in symbols:
                    try:
                        stock_data = yf.download(symbol, period='1d', interval='1m')
                        current_price = stock_data['Close'].iloc[-1]

                        # Если акция существует, Обновляет ее текущую цену
                        if self.stock_exists(symbol):
                            self.add_stock_price(symbol, current_price)
                        else:
                            # Если акция не существует, добавляет его в таблицу
                            self.add_stock_price(symbol, current_price)

                    except Exception as stock_error:
                        print(f"Error updating stock {symbol} prices: {stock_error}")

            except Exception as e:
                print(f"Error updating stock prices: {e}")

            # Ждет на 60 секунд
            await asyncio.sleep(interval_seconds)

        # Получает все названий тикеров
    def get_all_stock_symbols(self) -> List[str]:
        session = self.Session()
        try:
            stocks = session.query(StockPrice).all()
            symbols = [str(stock.symbol) for stock in stocks]
            return symbols
        finally:
            session.close()

    # Получает цены всех тикеров
    def get_stock_prices(self) -> Dict[str, float]:
        session = self.Session()
        try:
            prices = {stock.symbol: stock.current_price for stock in session.query(StockPrice).all()}
            return prices
        finally:
            session.close()

    # Добавляет цену тикера
    def add_stock_price(self, symbol: str, current_price: float):
        session = self.Session()
        try:
            # Проверить, существует ли уже тикер
            existing_stock = session.query(StockPrice).filter_by(symbol=symbol).first()

            if existing_stock:
                # Если тикер существует, обновите ее текущую цену
                existing_stock.current_price = current_price
            else:
                # Если тикер не существует, добавляет его в таблицу
                stock = StockPrice(symbol=symbol, current_price=current_price)
                session.add(stock)

            session.commit()
        finally:
            session.close()

    # Проверяет, существует ли тикер в бд
    def stock_exists(self, symbol: str) -> bool:
        session = self.Session()
        try:
            existing_stock = session.query(StockPrice).filter_by(symbol=symbol).first()
            return existing_stock is not None
        finally:
            session.close()
