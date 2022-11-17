from db import conn

import datetime
from typing import List

class Message(conn.Model):
    id = conn.Column(conn.Integer, primary_key=True)
    message_id = conn.Column(conn.Integer, nullable=True)
    link = conn.Column(conn.String(512))
    text = conn.Column(conn.Text, nullable=True)
    date = conn.Column(conn.DateTime, nullable=True, default=datetime.datetime.today())
    views = conn.Column(conn.Integer, nullable=False)
    forward_from_chat = conn.Column(conn.String(128), nullable=True)
    reaction = conn.Column(conn.Integer, nullable=True)
    media = conn.Column(conn.PickleType, nullable=True)
    mentions = conn.Column(conn.PickleType, nullable=True)
    category_id = conn.Column(conn.Integer, conn.ForeignKey('channel.id'), nullable=True)
    category = conn.relationship('Channel', backref=conn.backref('messages', lazy=True))

    def __repr__(self):
        return '<Message %r>' % self.message_id

def create_message(
        message_id: int,
        link: str,
        text: str,
        date: datetime.datetime,
        views: int,
        forward_from_chat: str,
        reaction: int,
        media: List[str] = None,
        mentions: List[str] = []
):
    try:
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
            return {"status": False, "message": Message.query.filter_by(message_id=message_id).first()}
        else:
            message = Message(
                message_id=message_id,
                link=link,
                text=text,
                date=date,
                views=views,
                forward_from_chat=forward_from_chat,
                reaction=reaction,
                media=media,
                mentions=mentions
            )
            return {"status": True, "message": message}

    except Exception as e:
        return e