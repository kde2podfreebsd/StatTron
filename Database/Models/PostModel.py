from sqlalchemy import Column, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Database.Models.SubPerDayModel import Base


class Post(Base):
    __tablename__ = "post"

    id_post = Column(BigInteger, primary_key=True)
    id_channel = Column(BigInteger, ForeignKey('channel.id_channel'), primary_key=True)
    date = Column(DateTime, nullable=False)
    views = Column(BigInteger, nullable=False)
    id_channel_forward_from = Column(BigInteger, ForeignKey('channel.id_channel'), nullable=False)

    channel = relationship('Channel', backref='posts')
    channelForwardFrom = relationship('Channel', backref='forwardedFrom')