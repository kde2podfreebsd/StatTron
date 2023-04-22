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
