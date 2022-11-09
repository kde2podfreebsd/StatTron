import os
import sys
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.app_context().push()

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'userbot.sqlite')

db = SQLAlchemy(app)




# py = Account(api_id=18305484, api_hash="010148f5fb4a1fa9006c73363eb8612e", username="donqhomo", host = "host", port = 443, public_key = "123123123")
# db.session.add(py)
# db.session.commit()
# accounts = Account.query.filter(Account.id != None).all()
# ch = Channel(title=123, link='test123')
# accounts[0].channels.append(ch)
# m = Message(message_id=1234, link="link1234")
# accounts[0].channels[0].messages.append(m)
# db.session.add(accounts[0])
# db.session.commit()

