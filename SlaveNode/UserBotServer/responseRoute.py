from dataclasses import dataclass
from datetime import date


@dataclass
class MainPageTopChannelsER:
    channel_name: str
    profile_img_url: str
    description: str
    subscribers: int
    total_views_last_month: int
    channel_id: int


@dataclass
class MainPageTopChannelsUpSubsToday:
    channel_name: str
    profile_img_url: str
    subscribers: int
    channel_id: int
    new_subscribers_today: int


@dataclass
class MainPageTopChannelsUpSubsYesterday:
    channel_name: str
    profile_img_url: str
    subscribers: int
    channel_id: int
    new_subscribers_yesterday: int


@dataclass
class MainPageTopChannelsUpSubsWeek:
    channel_name: str
    profile_img_url: str
    subscribers: int
    channel_id: int
    new_subscribers_week: int


@dataclass
class MainPageGraphicMentionPerHour:
    advertising_record_count: int
    advertising_record_percentage: int
    hour: str


@dataclass
class SearchChannelByLinkAndByName:
    channel_name: str | None
    channel_id: int | None
    profile_img_url: str | None
    description: str | None
    subscribers: int | None
    new_subscribers_today: int | None
    average_post_views_yesterday: int | None
    er: int | None


@dataclass
class TripleCharts:
    advertising_records_1month: int
    day_1month: date
    advertising_records_3month: int
    day_3month: date
    advertising_records_6month: int
    day_6month: date


@dataclass
class TopActiveChannelByER72hours:
    channel_name: str
    profile_img_url: str
    subscribers: int
    channel_id: int
    er_72_hours: int