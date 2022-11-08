from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DATETIME
from database import metadata

Accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("api_id", String, unique=True),
    Column("api_hash", String, unique = True),
    Column("username", String, unique = True),
    Column("host", String),
    Column("port", String, default="443"),
    Column("phone", String, unique = True)
)

Channels = Table(
    "Channels",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("is_scam", Boolean),
    Column("is_private", Boolean),
    Column("title", String),
    Column("username", String),
    Column("members_count", Integer),
    Column("description", String),
    Column("photo_big_file_id", String, unique = True),
    Column("photo_small_file_id", String, unique = True),
    Column("small_photo_path", String, unique = True),
    Column("owner_id", Integer, ForeignKey("accounts.id"))
)


