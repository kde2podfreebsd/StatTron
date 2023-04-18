from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from Database.Models import Base


class Channel(Base):
    __tablename__ = "channel"

    id_channel = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    link = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    subs_total = Column(BigInteger, nullable=False)

    subPerDay = relationship("SubPerDay", back_populates="channel", lazy="selectin")

    mentions = relationship(
        "Mention", back_populates="mentionedChannel", lazy="selectin"
    )

    posts = relationship("Post", back_populates="channel", lazy="selectin")

    forwardedFrom = relationship(
        "Post", back_populates="channelForwardFrom", lazy="selectin"
    )
