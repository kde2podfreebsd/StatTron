from sqlalchemy import Column, BigInteger, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SubPerDay(Base):
    __tablename__ = "sub_per_day"

    id_sub_per_day = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    subs = Column(BigInteger, nullable=False)
    id_channel = Column(BigInteger, ForeignKey('channel.id_channel'), nullable=False)

    channel = relationship('Channel', backref='SubsPerDay')
