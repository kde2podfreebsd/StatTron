import re
from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:

        orm_mode = True


class AdvertisingPost(TunedModel):
    channel_name: str
    post_id: int


class AdvertisingPostsList(TunedModel):
    advertising_posts_list: List[AdvertisingPost]
    pages_count: int


class Filters(BaseModel):
    page: int
    mentioned_channel: Optional[str] = None
    phrase_in_text: Optional[str] = None
    search_channel: Optional[str] = None
    datetime_from: Optional[datetime] = None
    datetime_to: Optional[datetime] = None
    sort_type: Optional[str] = None
    search_type: Optional[str] = None
    views_on_post_from: Optional[int] = None
    views_on_post_to: Optional[int] = None
