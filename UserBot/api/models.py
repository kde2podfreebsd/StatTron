# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DATETIME
# from api import metadata
#
#
# channels = Table(
#     "channels",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("username", String, unique=True),
#     Column("uid", Integer, unique = True),
#     Column("title", String, default="None"),
#     Column("members_count", Integer, default=0)
# )
#
#
# members = Table(
#     "members",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("chat_id", Integer),
#     Column("username", String),
#     Column("role", String),
#     Column("joined_date", DATETIME),
#     Column("owner_id", Integer, ForeignKey("channels.id"))
# )

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from database import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, index=True),
    Column("hashed_password", String),
    Column("is_active", Boolean, default=True)
)


items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, index=True),
    Column("description", String),
    Column("owner_id", Integer, ForeignKey("users.id"))
)