from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship

from Database.Models import Base


class Post(Base):
    __tablename__ = "post"

    id_post = Column(BigInteger, primary_key=True)
    id_channel = Column(BigInteger, ForeignKey("channel.id_channel"), primary_key=True)
    date = Column(DateTime, nullable=False)
    views = Column(BigInteger, nullable=False)
    text = Column(String, nullable=True)

    id_channel_forward_from = Column(
        BigInteger, ForeignKey("channel.id_channel"), nullable=True
    )

    # channelForwardFrom = relationship(
    #     "Channel",
    #     foreign_keys="Post.id_channel_forward_from",
    #     backref="forwardedFrom",
    #     viewonly=True,
    #     lazy="selectin",
    # )

    # channel = relationship(
    #     "Channel",
    #     foreign_keys="Post.id_channel",
    #     backref="posts",
    #     viewonly=True,
    #     lazy="selectin",
    # )

    mentions = relationship("Mention", back_populates="post", lazy="selectin")
