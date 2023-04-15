from sqlalchemy import Column, BigInteger, String
from Database.Models.MentionModel import Base


class Channel(Base):
    __tablename__ = "channel"

    id_channel = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    link = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    subs_total = Column(BigInteger, nullable=False)
