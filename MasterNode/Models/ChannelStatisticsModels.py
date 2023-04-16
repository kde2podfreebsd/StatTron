import re
from datetime import datetime
# from typing import List

from pydantic import BaseModel

# from typing import Optional


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


class ChannelMentions(TunedModel):
    pass


