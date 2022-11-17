from typing import List
from pydantic import BaseModel

class ChannelBase(BaseModel):
    is_scam: bool
    is_private: bool
    title: str
    username: str
    members_count: int
    description: str
    photo_big_file_id: str
    photo_small_file_id: str
    small_photo_path: str

class ChannelCreate(ChannelBase):

    class Config:
        orm_mode = True

class Channel(ChannelBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    api_id: str
    api_hash: str
    username: str
    host: str
    port: str
    phone: str

class AccountCreate(AccountBase):

    class Config:
        orm_mode = True


class AccountInDB(AccountBase):
    id: int
    class Config:
        orm_mode = True


class Account(AccountBase):
    id: int
    items: List[Channel] = []
    class Config:
        orm_mode = True


class ChannelAccount(ChannelBase):
    id: int
    owner: AccountInDB
    class Config:
        orm_mode = True