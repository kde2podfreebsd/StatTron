from .database import db
import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String(512))
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.today())
    views = db.Column(db.Integer, nullable=False)
    forward_from_chat = db.Column(db.String(128), nullable=False)
    reaction = db.Column(db.Integer, nullable=False)
    media = db.Column(db.PickleType, nullable=False)
    mentions = db.Column(db.PickleType, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
    category = db.relationship('Channel', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return '<Message %r>' % self.message_id