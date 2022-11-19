import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from db import conn
from config import app

from typing import Optional


class Account(conn.Model):
    id = conn.Column(conn.Integer, primary_key=True)
    api_id = conn.Column(conn.Integer, nullable=False)
    api_hash = conn.Column(conn.String(128), nullable=False)
    phone = conn.Column(conn.String(128), nullable=False)
    username = conn.Column(conn.String(128), nullable=False)
    host = conn.Column(conn.String(32), nullable=True)
    port = conn.Column(conn.Integer, nullable=True)
    public_key = conn.Column(conn.String(512), nullable=True)

    def __repr__(self):
        return '<Account %r>' % self.username

    def create(self,
               api_id: int,
               api_hash: str,
               phone: str,
               username: str,
               host: Optional[str],
               port: Optional[int],
               public_key: Optional[str]
               ):

        with app.app_context():
            if Account.query.filter_by(username=username).first():
                return {"status": False, "msg": "Account already exist"}
            else:
                self.api_id = api_id,
                self.api_hash = api_hash,
                self.phone = phone,
                self.username = username,
                self.host = host if host is not None else None,
                self.port = port if host is not None else None,
                self.public_key = public_key if host is not None else None

                conn.session.add(self)
                conn.session.commit()

                return {"status": True, "msg": "Account created"}

    def update(self):
        """
        update account
        """
        with app.app_context():
            if Account.query.filter_by(username=self.username).first():
                conn.session.commit()
                return {"status": True, "msg": "Account updated"}
            else:
                return {"status": False, "msg": "Account doesnt found"}

    def delete(self):
        """
        delete account
        """
        with app.app_context():
            if Account.query.filter_by(username=self.username).first():
                Account.query.filter_by(username=self.username).delete()
                conn.session.commit()
                return {"status": True, "msg": "Account deleted"}
            else:
                return {"status": False, "msg": "Account doesnt found"}


if __name__ == "__main__":
    pass
