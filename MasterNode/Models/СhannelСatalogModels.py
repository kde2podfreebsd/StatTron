import re
from typing import List
from typing import Optional

from pydantic import BaseModel

# from datetime import datetime


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:

        orm_mode = True


class Channel(TunedModel):
    channel_name: str
    channel_id: int
    profile_img_url: str
    description: str
    subscribers: int
    new_subscribers_today: int
    average_post_views_yesterday: int
    er: float


class ChannelsList(TunedModel):
    channels_list: List[Channel]
    pages_count: int


class ByLinkFilter(BaseModel):
    URL: str


class ByNameFilter(BaseModel):
    channel_name: str
    page: int


class ByBaseFilters(BaseModel):
    page: int
    description: Optional[str] = None
    subscribers_from: Optional[int] = None
    subscribers_to: Optional[int] = None
    post_average_views_from: Optional[int] = None
    post_average_views_to: Optional[int] = None
    mentions_by_week_from: Optional[int] = None
    mentions_by_week_to: Optional[int] = None
    channel_type: Optional[str] = None
    category: Optional[str] = None
    er72h_from: Optional[int] = None
    er72h_to: Optional[int] = None
