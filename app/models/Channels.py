import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from db import conn
from config import app

from typing import Optional

class Channel(conn.Model):
    id = conn.Column(conn.Integer, primary_key=True)
    channel_id = conn.Column(conn.Integer, unique=True, nullable=False)
    is_scam = conn.Column(conn.Boolean, nullable=False)
    is_private = conn.Column(conn.Boolean, nullable=False)
    title = conn.Column(conn.String(256), nullable=True)
    username = conn.Column(conn.String(64), nullable=True)
    members_count = conn.Column(conn.Integer, nullable=False)
    description = conn.Column(conn.Text, nullable=True)
    category = conn.Column(conn.String(128), nullable=True)
    photo_big_file_id = conn.Column(conn.String(512), nullable=True)
    photo_small_file_id = conn.Column(conn.String(512), nullable=True)
    small_photo_path = conn.Column(conn.String(512), nullable=True)
    average_views = conn.Column(conn.Float, nullable=True)
    er_all = conn.Column(conn.Float, nullable=True)
    account_id = conn.Column(conn.Integer, conn.ForeignKey('account.id'), nullable=False)
    account = conn.relationship('Account', backref=conn.backref('channels', lazy=True))

    def __repr__(self):
        return '<Channel %r>' % self.channel_id

    def create_and_update(self,
            channel_id: int,
            is_scam: bool,
            is_private: bool,
            title: Optional[str],
            username: Optional[str],
            members_count: int,
            description: Optional[str],
            category: Optional[str],
            photo_big_file_id: Optional[str],
            photo_small_file_id: Optional[str],
            small_photo_path: Optional[str],
            average_views: Optional[float],
            er_all: Optional[float]
    ):
        with app.app_context():
            if Channel.query.filter_by(channel_id=channel_id).first():
                channel = Channel.query.filter_by(channel_id=channel_id).first()

                channel.channel_id = channel_id,
                channel.is_scam = is_scam,
                channel.is_private = is_private,
                channel.title = title if title is not None else None,
                channel.username = username if username is not None else None,
                channel.members_count = members_count
                channel.description = description if description is not None else None
                channel.category = category if category is not None else None
                channel.photo_big_file_id = photo_big_file_id if photo_big_file_id is not None else None
                channel.photo_small_file_id = photo_small_file_id if photo_small_file_id is not None else None
                channel.small_photo_path = small_photo_path if small_photo_path is not None else None
                channel.average_views = average_views if average_views is not None else None
                channel.er_all = er_all if er_all is not None else None

                conn.session.commit()
                return {"status": True, "msg": "Channel updated"}
            else:
                self.channel_id = channel_id,
                self.is_scam = is_scam,
                self.is_private = is_private,
                self.title = title if title is not None else None,
                self.username = username if username is not None else None,
                self.members_count = members_count
                self.description = description if description is not None else None
                self.category = category if category is not None else None
                self.photo_big_file_id = photo_big_file_id if photo_big_file_id is not None else None
                self.photo_small_file_id = photo_small_file_id if photo_small_file_id is not None else None
                self.small_photo_path = small_photo_path if small_photo_path is not None else None
                self.average_views = average_views if average_views is not None else None
                self.er_all = er_all if er_all is not None else None

                conn.session.add(self)
                conn.session.commit()

                return {"status": True, "msg": "Channel created"}




if __name__ == "__main__":
    pass



