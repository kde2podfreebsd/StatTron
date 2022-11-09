from .database import db, app
from pyrogram import Client
import asyncio

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, nullable=False)
    api_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), nullable=False)
    host = db.Column(db.String(32), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    public_key = db.Column(db.String(512), nullable=False)

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
                db.session.add(account)
                db.session.commit()

            return {
                "message": 'Account added',
                "status": True
            }

    except Exception as e:
        return e

def get_account(username: str):
    try:
        return {"status": True, "account": Account.query.filter_by(username=username).first()} if Account.query.filter_by(username=username).first() else {"status": False}
    except Exception as e:
        return e

def delete_account(username: str):
    try:
        if Account.query.filter_by(username=username).first():
            Account.query.filter_by(username=username).delete()
            db.session.commit()
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
    # res1 = create_account(
    #     api_id = 18305484,
    #     api_hash = "010148f5fb4a1fa9006c73363eb8612e",
    #     phone = "89162107493",
    #     username= "donqhomo",
    #     host= "149.154.167.50",
    #     port = 443,
    #     public_key = "-----BEGIN RSA PUBLIC KEY-----MIIBCgKCAQEA6LszBcC1LGzyr992NzE0ieY+BSaOW622Aa9Bd4ZHLl+TuFQ4lo4g5nKaMBwK/BIb9xUfg0Q29/2mgIR6Zr9krM7HjuIcCzFvDtr+L0GQjae9H0pRB2OO62cECs5HKhT5DZ98K33vmWiLowc621dQuwKWSQKjWf50XYFw42h21P2KXUGyp2y/+aEyZ+uVgLLQbRA1dEjSDZ2iGRy12Mk5gpYc397aYp438fsJoHIgJ2lgMv5h7WY9t6N/byY9Nw9p21Og3AoXSL2q/2IJ1WRUhebgAdGVMlV1fkuOQoEzR7EdpqtQD9Cs5+bfo3Nhmcyvk5ftB0WkJ9z6bNZ7yxrP8wIDAQAB-----END RSA PUBLIC KEY-----"
    # )
    # print(res1)

    # res2 = get_account(username="donqhomo")
    # print(res2)

    # res3 = init_session(username="donqhomo")
    # print(res3)

    # res4 = delete_account(username="donqhomo")
    # print(res4)


