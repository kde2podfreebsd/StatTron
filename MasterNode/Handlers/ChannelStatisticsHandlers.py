from datetime import datetime
from logging import getLogger
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Database.session import get_db
from MasterNode.Models.ChannelStatisticsModels import MainStat

# from Database.DAL import UserDAL

logger = getLogger(__name__)

channel_statistics_router = APIRouter()


async def _get_main_channel_statistic(db) -> Union[MainStat, None]:
    # async with db as session:
    return MainStat(
        subscribers_total=123,
        subscribers_today=234,
        subscribers_week=456,
        subscribers_month=678,
        average_views_1month=999,
        average_views_24hours=111,
        er_72hours=12.0,
        er_24hours=456.1,
        mentions_count=12
    )


@channel_statistics_router.get("/get_main_channel_statistic", response_model=MainStat)
async def get_main_channel_statistic(
        db: AsyncSession = Depends(get_db),
) -> MainStat:
    main_channel_statistic = await _get_main_channel_statistic(db)
    if main_channel_statistic is None:
        raise HTTPException(status_code=404, detail="Channels database is empty")
    return main_channel_statistic
