from sqlalchemy import Column, BigInteger, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from Database.Models.PostModel import Base


class Mention(Base):
    __tablename__ = "mention"

    id_mentioned_channel = Column(BigInteger, ForeignKey('channel.id_channel'), primary_key=True)
    id_post = Column(BigInteger, primary_key=True)
    id_channel = Column(BigInteger, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            [id_post, id_channel],
            ['post.id_post', 'post.id_channel']),
        {}
    )

    mentionedChannel = relationship('Channel', backref='mentions')
    post = relationship('Post', backref='mentions')
