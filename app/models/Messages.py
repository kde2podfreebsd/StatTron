import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from db import conn
from config import app

import datetime
from typing import Optional, List
from sqlalchemy.dialects.mysql import BIGINT

from .Accounts import Account


class Message(conn.Model):
    id = conn.Column(conn.Integer, primary_key=True)
    message_id = conn.Column(conn.Integer, nullable=True)
    link = conn.Column(conn.String(512))
    text = conn.Column(conn.Text, nullable=True)
    date = conn.Column(conn.DateTime, nullable=True)
    views = conn.Column(conn.Integer, nullable=True)
    forward_from_chat = conn.Column(conn.String(128), nullable=True)
    reaction = conn.Column(conn.Integer, nullable=True)
    media = conn.Column(conn.PickleType, nullable=True)
    mentions = conn.Column(conn.PickleType, nullable=True)
    category_id = conn.Column(conn.Integer, conn.ForeignKey('channel.id'), nullable=True)
    category = conn.relationship('Channel', backref=conn.backref('messages', lazy=True))

    def __repr__(self):
        return '<Message %r>' % self.message_id

    def create_message(self,
                       account,
                       channel,
                       message_id: int,
                       link: str,
                       text: str,
                       date: datetime.datetime,
                       views: int,
                       forward_from_chat: str,
                       reaction: int,
                       media: List[str] = None,
                       mentions: List[str] = list()
                       ):
        with app.app_context():
            if Message.query.filter_by(message_id=message_id).first():
                message = Message.query.filter_by(message_id=message_id).first()

                message.message_id = message_id
                message.link = link
                message.text = text
                message.date = date
                message.views = views
                message.forward_from_chat = forward_from_chat
                message.reaction = reaction
                message.media = media
                message.mentions = mentions

                conn.session.commit()
                return {"status": True, "msg": "Message updated", "message": Message.query.filter_by(message_id=message_id).first()}
            else:
                message = Message()

                self.message_id = message_id,
                self.link = link,
                self.text = text,
                self.date = date,
                self.views = views,
                self.forward_from_chat = forward_from_chat,
                self.reaction = reaction,
                self.media = media,
                self.mentions = mentions

                i = 0
                for ch in account.channels:
                    if channel.channel_id == ch.channel_id:
                        break
                    i += 1

                account.channels[i].messages.append(self)
                current_db_sessions = conn.object_session(account)
                current_db_sessions.add(account)
                current_db_sessions.commit()

                return {"status": True, "msg": "Message created", "message": self}
