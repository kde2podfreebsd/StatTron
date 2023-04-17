import re

from pydantic import BaseModel

# from datetime import datetime
# from typing import List
# from typing import Optional


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:

        orm_mode = True


class AdvertisingReturnsStatistic(TunedModel):
    advertising_posts_count_all_time: int
    repost_count_all_time: int
    advertising_posts_count_week: int
    repost_count_week: int
    advertising_posts_count_month: int
    repost_count_month: int
    # подборки?


class AdvertisingReturnsStatisticFilter(BaseModel):
    channel_id: int
