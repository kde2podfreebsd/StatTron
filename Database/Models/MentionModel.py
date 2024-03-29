from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import relationship

from Database.Models import Base


class Mention(Base):
    __tablename__ = "mention"

    id_mentioned_channel = Column(
        BigInteger, ForeignKey("channel.id_channel"), primary_key=True
    )
    id_post = Column(BigInteger, primary_key=True)
    id_channel = Column(BigInteger, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            [id_post, id_channel], ["post.id_post", "post.id_channel"]
        ),
        {},
    )

    mentionedChannel = relationship(
        "Channel", back_populates="mentions", viewonly=True, lazy="selectin"
    )

    post = relationship(
        "Post", back_populates="mentions", viewonly=True, lazy="selectin"
    )
