import time

from database import get_db, engine, Base
from services.stock import update_all_stocks

Base.metadata.create_all(bind=engine)

while True:
    print("Updating stocks...")
    update_all_stocks(get_db().__next__())
    print("Done!")

    time.sleep(60)
