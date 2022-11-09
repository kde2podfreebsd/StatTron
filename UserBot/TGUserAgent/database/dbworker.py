import sys
import os
from .database import db, app

from Accounts import Account
from Channels import Channel
from Messages import Message

if __name__ == "__main__":
    match sys.argv[1]:
        case 'init':
            with app.app_context():
                db.create_all()

        case 'drop':
            with app.app_context():
                os.system("rm userbot.sqlite")

        case 'rebuild':
            with app.app_context():
                os.system("rm userbot.sqlite")
                db.create_all()
        case _:
            pass