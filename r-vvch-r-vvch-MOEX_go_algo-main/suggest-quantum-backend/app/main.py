import telebot
import uvicorn
from fastapi import FastAPI
import psycopg2

from services.user import get_user_secret, post_create_user
from services.portfolio import post_portfolio_create, get_user_portfolios, get_portfolio, count_portfolio

app = FastAPI()

try:
    conn = psycopg2.connect("dbname=suggest_quantum user=postgres password=pass")
except psycopg2.errors.OperationalError as e:
    print(e)

# bot = telebot.TeleBot('TOKEN')


@app.get("/user/{login}")
async def _get_user_secret(login: str, password: str):
    return get_user_secret(conn, login, password)


@app.post("/user/create")
async def _post_create_user(login: str, password: str, username: str):
    return post_create_user(conn, login, password, username)


@app.post("/portfolio/create")
async def _post_create_portfolio(secret: str, portfolio_name: str, balance: int):
    return post_portfolio_create(conn, secret, portfolio_name, balance)


@app.get("/portfolio/get_user_portfolios")
async def _get_user_portfolios(secret: str):
    return get_user_portfolios(conn, secret)


@app.get("/portfolio/get_portfolio/{portfolio_id}")
async def _get_portfolio(secret: str, portfolio_id: int):
    return get_portfolio(conn, secret, portfolio_id)


@app.post("/portfolio/count_portfolio/{portfolio_id}")
async def _count_portfolio(secret: str, portfolio_id: int):
    # bot.send_message()
    return count_portfolio(conn, bot, secret, portfolio_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
