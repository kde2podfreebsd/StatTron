import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../'))
from db import conn
from config import app

from pyrogram import Client
import asyncio

class Account(conn.Model):
    id = conn.Column(conn.Integer, primary_key=True)
    api_id = conn.Column(conn.Integer, nullable=False)
    api_hash = conn.Column(conn.String(128), nullable=False)
    phone = conn.Column(conn.String(128), nullable=False)
    username = conn.Column(conn.String(128), nullable=False)
    host = conn.Column(conn.String(32), nullable=False)
    port = conn.Column(conn.Integer, nullable=False)
    public_key = conn.Column(conn.String(512), nullable=False)

    def __repr__(self):
        return '<Account %r>' % self.username

def create_account(
        api_id: int,
        api_hash: str,
        phone: str,
        username: str,
        host: str,
        port: int,
        public_key: str
):
    try:
        with app.app_context():
            if Account.query.filter_by(phone=phone).first():
                return {
                    "message": 'Account already exist',
                    "status": False
                }
            else:
                account = Account(
                    api_id = api_id,
                    api_hash = api_hash,
                    phone = phone,
                    username = username,
                    host = host,
                    port = port,
                    public_key = public_key
                )
                conn.session.add(account)
                conn.session.commit()

            return {
                "message": 'Account added',
                "status": True
            }

    except Exception as e:
        return e

def get_account(username: str):
    try:
        with app.app_context():
            return {"status": True, "account": Account.query.filter_by(username=username).first()} if Account.query.filter_by(username=username).first() else {"status": False}
    except Exception as e:
        return e

def delete_account(username: str):
    try:
        if Account.query.filter_by(username=username).first():
            Account.query.filter_by(username=username).delete()
            conn.session.commit()
            return {
                "status": True,
                "message": 'Account deleted'
            }
        else:
            return {
                "status": False,
                "message": 'Account doesnt exist'
            }
    except Exception as e:
        return e


#-----------------------------------------------------------------------------------------------------------------------
async def create_session(username: str, api_id: int, api_hash: str):
    try:
        async with Client(f"../sessions/{username}", api_id, api_hash) as app:
            await app.send_message("me", "create session")
            return True
    except Exception as e:
        return e

def init_session(username: str):
    try:
        res = get_account(username = username)
        if res["status"] == True:
            account = res["account"]
            asyncio.run(create_session(username = account.username, api_id = account.api_id, api_hash=account.api_hash))
            return True
        else:
            return {"Account wasnt created"}
    except Exception as e:
        return e

if __name__=="__main__":
    pass


