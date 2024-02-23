import random
import string
from fastapi import HTTPException


def get_user_secret(conn, login: str, password: str):
    cur = conn.cursor()
    cur.execute(
        f"SELECT secret FROM users WHERE login = '{login}' AND password = '{password}'"
    )
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"Login {login} Not Found")
    return cur.fetchone()[0]


def _get_user_id_by_secret(conn, secret: str):
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM users WHERE secret = '{secret}'")
    return cur.fetchone()[0]


def post_create_user(conn, login: str, password: str, username: str):
    cur = conn.cursor()
    secret = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(16)
    )
    cur.execute(
        f"INSERT INTO users (login,password,username,secret) VALUES ('{login}','{password}','{username}','{secret}');"
    )
    conn.commit()
    return secret
