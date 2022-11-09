from .database import db, app

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, unique=True)
    is_scam = db.Column(db.Boolean, nullable=False)
    is_private = db.Column(db.Boolean, nullable=False)
    title = db.Column(db.String(256), nullable=True)
    username = db.Column(db.String(64), nullable=True)
    members_count = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(128), nullable=True, default="No category selected")
    photo_big_file_id = db.Column(db.String(512), nullable=True)
    photo_small_file_id = db.Column(db.String(512), nullable=True)
    small_photo_path = db.Column(db.String(512), nullable=True)
    average_views = db.Column(db.Float, nullable=True, default = 0)
    er_all = db.Column(db.Float, nullable=True, default = 0)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref=db.backref('channels', lazy=True))

    def __repr__(self):
        return '<Channel %r>' % self.channel_id

def create_channel(
        channel_id: int,
        is_scam: bool,
        is_private: bool,
        title: str,
        username: str,
        members_count: int,
        description: str,
        category: str,
        photo_big_file_id: str,
        photo_small_file_id: str,
        small_photo_path: str,
        average_views: float,
        er_all: float
):
    try:
        with app.app_context():
            if Channel.query.filter_by(channel_id=channel_id).first():
                channel = Channel.query.filter_by(channel_id=channel_id).first()
                channel.channel_id = channel_id
                channel.is_scam = is_scam
                channel.is_private = is_private
                channel.title = title
                channel.username = username
                channel.members_count = members_count
                channel.description = description
                channel.category = category
                channel.photo_big_file_id = photo_big_file_id
                channel.photo_small_file_id = photo_small_file_id
                channel.small_photo_path = small_photo_path
                channel.average_views = average_views
                channel.er_all = er_all
                db.session.commit()
                return {"status": False, "channel": Channel.query.filter_by(channel_id=channel_id).first()}
            else:
                channel = Channel(
                    channel_id = channel_id,
                    is_scam = is_scam,
                    is_private = is_private,
                    title = title,
                    username = username,
                    members_count = members_count,
                    description = description,
                    category = category,
                    photo_big_file_id = photo_big_file_id,
                    photo_small_file_id = photo_small_file_id,
                    small_photo_path = small_photo_path,
                    average_views = average_views,
                    er_all= er_all
                )

                return {"status": True, "channel": channel}

    except Exception as e:
        return e

def get_channel(channel_id: int):
    try:
        with app.app_context():
            return {"status": True, "channel": Channel.query.filter_by(channel_id=channel_id).first()} if Channel.query.filter_by(channel_id=channel_id).first() else {"status": False}
    except Exception as e:
        return e

def delete_channel(channel_id: int):
    try:
        with app.app_context():
            if Channel.query.filter_by(channel_id=channel_id).first():
                Channel.query.filter_by(channel_id=channel_id).delete()
                db.session.commit()
                return {
                    "status": True,
                    "message": 'Channel deleted'
                }
            else:
                return {
                    "status": False,
                    "message": 'Channel doesnt exist'
                }
    except Exception as e:
        return e

def update_members_count(channel_id: int, members_count: int):
    try:
        with app.app_context():
            if Channel.query.filter_by(channel_id=channel_id).first():
                channel = Channel.query.filter_by(channel_id=channel_id).first()
                channel.members_count = members_count
                db.session.commit()
                return {
                    "status": True,
                    "message": 'Channel updated'
                }
            else:
                return {
                    "status": False,
                    "message": 'Channel doesnt exist'
                }
    except Exception as e:
        return e

# if __name__ == "__main__":
#     channel_id = 123,
#     is_scam = False,
#     is_private = False,
#     title = "title",
#     username = "username",
#     members_count = "members_count",
#     description: str,
#     category: str,
#     photo_big_file_id: str,
#     photo_small_file_id: str,
#     small_photo_path: str,
#     average_views: float,
#     er_all: float



