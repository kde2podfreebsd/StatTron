from app.config import db, app
from app.logger import Logger
from app.responseModels import DatabaseResponse
from typing import Optional

log = Logger()

class AccountModel(db.Model, object):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.String, nullable=False)
    api_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(128), nullable=False)
    host = db.Column(db.String(32), nullable=True)
    port = db.Column(db.String(32), nullable=True)
    public_key = db.Column(db.String(512), nullable=True)

    def __repr__(self) -> "Username is unique key for account model":
        return '<Account %r>' % self.username

    def __init__(self) -> "pass init builder":
        log.logger.info('Init Account Model')

    def createAccount(
            self,
            api_id: str,
            api_hash: str,
            phone: str,
            username: str,
            host: Optional[str],
            port: Optional[str],
            public_key: Optional[str]
    ):
        with app.app_context():
            if AccountModel.query.filter_by(id is not None).first():
                response = DatabaseResponse(
                    status=False,
                    action="Create new account",
                    message="Account already created in database, unsuccessfully"
                )
                log.logger.warning(response)
                return response
            else:
                self.api_id = api_id
                self.api_hash = api_hash
                self.phone = phone
                self.username = username
                self.host = host
                self.port = port
                self.public_key = public_key

                db.session.add(self)
                db.session.commit()

                response = DatabaseResponse(
                    status=True,
                    action="Create new account",
                    message="Account created in database successfully"
                )

                log.logger.info(response)
                return response

    def updateAccount(
            self,
            api_id: Optional[str] = None,
            api_hash: Optional[str] = None,
            phone: Optional[str] = None,
            username: Optional[str] = None,
            host: Optional[str] = None,
            port: Optional[str] = None,
            public_key: Optional[str] = None
    ):
        with app.app_context():
            account = AccountModel.query.filter_by(username=self.username).first()
            if account is not None:
                account.api_id = api_id if api_id is not None else account.api_id
                account.api_hash = api_hash if api_hash is not None else account.api_hash
                account.phone = phone if phone is not None else account.phone
                account.username = username if username is not None else account.username
                account.host = host if host is not None else account.host
                account.port = port if port is not None else account.port
                account.public_key = public_key if public_key is not None else account.public_key

                account.session.commit()

                response = DatabaseResponse(
                    status=True,
                    action="Update account",
                    message="Account updated, successfully"
                )

                log.logger.info(response)
                return response

            else:
                response = DatabaseResponse(
                    status=False,
                    action="Update account",
                    message="Account doesnt found, update unsuccessfully"
                )

                log.logger.warning(response)
                return response

    def deleteAccount(self):
        with app.app_context():
            if AccountModel.query.filter_by(username=self.username).first():
                AccountModel.query.filter_by(username=self.username).delete()
                db.session.commit()
                response = DatabaseResponse(
                    status=True,
                    action="Delete account",
                    message="Account deleted, successfully"
                )
                log.logger.info(response)
                return response
            else:
                response = DatabaseResponse(
                    status=False,
                    action="Delete account",
                    message="Account doesnt found, deleted unsuccessfully"
                )
                log.logger.warning(response)
                return response
