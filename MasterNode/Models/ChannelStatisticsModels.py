import re
from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:

        orm_mode = True


class MainStat(TunedModel):
    subscribers_total: int
    subscribers_today: int
    subscribers_week: int
    subscribers_month: int
    average_views_1month: int
    average_views_24hours: int
    er_72hours: float
    er_24hours: float
    mentions_count: int


class MainStatFilter(BaseModel):
    channel_id: int


class MentionInChannel(TunedModel):
    profile_img_url: str
    channel_name: str
    channel_id: int
    members_count: int
    post_date: datetime


class MentionInChannelList(TunedModel):
    mention_in_channel_list: List[MentionInChannel]


class MentionInChannelsFilter(BaseModel):
    with_forward: Optional[bool] = False
    mentioned_channel_id: Optional[int] = None
    text_to_find: Optional[str] = None


class SubscribersCountOnDay(TunedModel):
    subscribers_count: int
    datetime: datetime


class SubscribersCountOnDayChart1month(TunedModel):
    subscribers_count_on_day_chart_1month: List[SubscribersCountOnDay]


class SubscribersCountOnDayChart1monthFilter(BaseModel):
    channel_id: int
