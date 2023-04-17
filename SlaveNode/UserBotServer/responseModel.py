from dataclasses import dataclass
from datetime import date


@dataclass
class ChannelObject:
    id_channel: int
    name: str
    link: str
    avatar_url: str
    description: str
    subs_total: int


@dataclass
class ChannelIds:
    channel_ids: list[int]


@dataclass
class Post:
    id_post: int
    id_channel: int
    date: date
    text: str
    views: int
    id_channel_forward_from: int


@dataclass
class Mention:
    id_mentioned_channel: int
    id_post: int
    id_channel: int


@dataclass
class ChatObject:
    posts: list[Post]
    mentions: list[Mention]


@dataclass
class UpdateChannel:
    id_channel: int
    subs_total: int


@dataclass
class UpdatePost:
    id_post: int
    id_channel: int
    views: int
