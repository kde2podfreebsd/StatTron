from db import conn

class Channel(conn.Model):
    id = conn.Column(conn.Integer, primary_key=True)
    channel_id = conn.Column(conn.Integer, unique=True)
    is_scam = conn.Column(conn.Boolean, nullable=False)
    is_private = conn.Column(conn.Boolean, nullable=False)
    title = conn.Column(conn.String(256), nullable=True)
    username = conn.Column(conn.String(64), nullable=True)
    members_count = conn.Column(conn.Integer, nullable=False)
    description = conn.Column(conn.Text, nullable=True)
    category = conn.Column(conn.String(128), nullable=True, default="No category selected")
    photo_big_file_id = conn.Column(conn.String(512), nullable=True)
    photo_small_file_id = conn.Column(conn.String(512), nullable=True)
    small_photo_path = conn.Column(conn.String(512), nullable=True)
    average_views = conn.Column(conn.Float, nullable=True, default = 0)
    er_all = conn.Column(conn.Float, nullable=True, default = 0)
    account_id = conn.Column(conn.Integer, conn.ForeignKey('account.id'), nullable=False)
    account = conn.relationship('Account', backref=conn.backref('channels', lazy=True))

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
            conn.session.commit()
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
        return {"status": True, "channel": Channel.query.filter_by(channel_id=channel_id).first()} if Channel.query.filter_by(channel_id=channel_id).first() else {"status": False}
    except Exception as e:
        return e

def delete_channel(channel_id: int):
    try:
        if Channel.query.filter_by(channel_id=channel_id).first():
            Channel.query.filter_by(channel_id=channel_id).delete()
            conn.session.commit()
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
        if Channel.query.filter_by(channel_id=channel_id).first():
            channel = Channel.query.filter_by(channel_id=channel_id).first()
            channel.members_count = members_count
            conn.session.commit()
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

def update_average_views(channel_id: int, average_views: float):
    try:
        if Channel.query.filter_by(channel_id=channel_id).first():
            channel = Channel.query.filter_by(channel_id=channel_id).first()
            channel.average_views = average_views
            conn.session.commit()
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

def update_er_all(channel_id: int, er_all: float):
    try:
        if Channel.query.filter_by(channel_id=channel_id).first():
            channel = Channel.query.filter_by(channel_id=channel_id).first()
            channel.er_all = er_all
            conn.session.commit()
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


if __name__ == "__main__":
    pass



