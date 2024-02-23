import smtplib
import ssl

import telebot
from fastapi import HTTPException

from app.services.user import _get_user_id_by_secret


def get_user_portfolios(conn, secret: str):
    cur = conn.cursor()
    user_id = _get_user_id_by_secret(conn, secret)
    cur.execute(f"SELECT id, portfolio_name FROM portfolios WHERE owner = '{user_id}'")
    response = cur.fetchall()
    return [
        {"portfolio_id": portfolio[0], "portfolio_name": portfolio[1]}
        for portfolio in response
    ]


def post_portfolio_create(conn, secret: str, portfolio_name: str, balance: int):
    cur = conn.cursor()
    user_id = _get_user_id_by_secret(conn, secret)
    cur.execute(
        f"INSERT INTO portfolios (portfolio_name, owner, balance) VALUES ('{portfolio_name}','{user_id}','{balance}')"
    )
    conn.commit()
    return {"portfolio_name": portfolio_name}


def get_portfolio(conn, secret: str, portfolio_id: int):
    cur = conn.cursor()
    user_id = _get_user_id_by_secret(conn, secret)
    cur.execute(
        f"SELECT portfolio_name, balance, chart_path FROM portfolios WHERE id = '{portfolio_id}' AND owner = '{user_id}'"
    )
    return cur.fetchall()[0]


def count_portfolio(conn, bot, secret: str, portfolio_id: int):
    cur = conn.cursor()
    user_id = _get_user_id_by_secret(conn, secret)
    cur.execute(f"SELECT count_status FROM portfolios WHERE owner = '{user_id}'")
    if cur.fetchone()[0] == 'not_requested':
        # bot.sendmessage()
        return {'response': 'request_sended'}
    else:
        raise HTTPException(status_code=400, detail='Already requested')
