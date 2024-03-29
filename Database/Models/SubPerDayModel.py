from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Database.Models import Base

# from sqlalchemy.orm import declarative_base

# from Database.Models.PostModel import Post
# from Database.Models.MentionModel import Mention
# from Database.Models.ChannelModel import Channel

# Base = declarative_base()


class SubPerDay(Base):
    __tablename__ = "sub_per_day"

    id_sub_per_day = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    subs = Column(BigInteger, nullable=False)
    id_channel = Column(BigInteger, ForeignKey("channel.id_channel"), nullable=False)

    channel = relationship(
        "Channel", back_populates="subPerDay", viewonly=True, lazy="selectin"
    )
