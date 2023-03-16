from typing import Optional, BinaryIO, List
from dataclasses import dataclass
from pyrogram.types import User, ChatPhoto, Dialog, Chat
from pyrogram.enums import UserStatus, ChatType
from datetime import datetime

@dataclass
class DownloadFilePWD:
    pwd: str | None | BinaryIO

@dataclass
class ChannelIds:
    chat_ids: List[Dialog]

@dataclass
class GetMeUser:
    id: int
    is_self: bool
    is_contact: bool
    is_mutual_contact: bool
    is_deleted: bool
    is_bot: bool
    is_verified: bool
    is_restricted: bool
    is_scam: bool
    is_fake: bool
    is_support: bool
    is_premium: bool
    first_name: str
    last_name: str
    status: UserStatus
    last_online_date: datetime
    username: str
    dc_id: int
    phone_number: str
    photo: ChatPhoto

@dataclass
class ChatObject:
    id: int
    is_verified: bool
    is_restricted: bool
    is_creator: bool
    is_scam: bool
    is_fake: bool
    title: str
    username: str
    photo: ChatPhoto
    small_file_id: str | None
    dc_id: Optional[int] = None
    type: Optional[ChatType] = None
    description: Optional[str] = None
    members_count: Optional[int] = None
    has_protected_content: Optional[bool] = None

@dataclass
class MessageChatObject:
    sender_chat_id: int | str
    sender_username: str
    sender_chat: Chat
    date: datetime

