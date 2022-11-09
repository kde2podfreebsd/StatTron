from .database import db, app
import datetime
from typing import List

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, nullable=True)
    link = db.Column(db.String(512))
    text = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=True, default=datetime.datetime.today())
    views = db.Column(db.Integer, nullable=False)
    forward_from_chat = db.Column(db.String(128), nullable=True)
    reaction = db.Column(db.Integer, nullable=True)
    media = db.Column(db.PickleType, nullable=True)
    mentions = db.Column(db.PickleType, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=True)
    category = db.relationship('Channel', backref=db.backref('messages', lazy=True))

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
                db.session.commit()
                return {"status": False, "message": Message.query.filter_by(message_id=message_id).first()}
            else:
                message = Message(
                    message_id = message_id,
                    link = link,
                    text = text,
                    date = date,
                    views = views,
                    forward_from_chat = forward_from_chat,
                    reaction = reaction,
                    media = media,
                    mentions = mentions
                )
                return {"status": True, "message": message}

    except Exception as e:
        return e