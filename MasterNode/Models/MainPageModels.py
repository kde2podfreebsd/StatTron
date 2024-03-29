import re
from datetime import datetime
from typing import List, Any

from pydantic import BaseModel

# from typing import Optional

# import uuid


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:

        orm_mode = True


class TopActiveChannel(TunedModel):
    channel_name: str
    profile_img_url: str | None
    description: str | None
    subscribers: int
    total_views_last_month: int | None
    channel_id: int


class TopActiveChannels(TunedModel):
    top_active_channels: List[TopActiveChannel]


class TopChannelByNewSubscribers_today(TunedModel):
    channel_name: str
    profile_img_url: str
    subscribers: int
    channel_id: int
    new_subscribers_today: int


class TopChannelByNewSubscribers_yesterday(TunedModel):
    channel_name: str
    profile_img_url: str
    subscribers: int
    channel_id: int
    new_subscribers_yesterday: int


class TopChannelByNewSubscribers_week(TunedModel):
    channel_name: str
    profile_img_url: str
    subscribers: int
    channel_id: int
    new_subscribers_week: int


class TopChannelsByNewSubscribers(TunedModel):
    top_channels_by_new_subscribers: List[
        TopChannelByNewSubscribers_today
        | TopChannelByNewSubscribers_yesterday
        | TopChannelByNewSubscribers_week
    ]


class AdvertisingRecordsByDay(TunedModel):
    advertising_records_1month: int  # Y axis
    day_1month: datetime | Any  # X axis
    advertising_records_3month: int
    day_3month: datetime | Any
    advertising_records_6month: int
    day_6month: datetime | Any


class AdvertisingRecordsByDayChart(TunedModel):
    advertising_records_by_day_chart: List[AdvertisingRecordsByDay]


class AdvertisingRecordsByHours(TunedModel):
    advertising_records_count: int
    advertising_records_percentage: float
    hour: str


class AdvertisingRecordsByHoursChart(TunedModel):
    advertising_records_by_hours_chart: List[AdvertisingRecordsByHours]
