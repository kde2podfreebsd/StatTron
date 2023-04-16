from datetime import datetime
from logging import getLogger
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Database.session import get_db
from MasterNode.Models.ChannelStatisticsModels import MainStat
from MasterNode.Models.ChannelStatisticsModels import MainStatFilter
from MasterNode.Models.ChannelStatisticsModels import MentionInChannel
from MasterNode.Models.ChannelStatisticsModels import MentionInChannelList
from MasterNode.Models.ChannelStatisticsModels import MentionInChannelsFilter
from MasterNode.Models.ChannelStatisticsModels import SubscribersCountOnDay
from MasterNode.Models.ChannelStatisticsModels import SubscribersCountOnDayChart1month
from MasterNode.Models.ChannelStatisticsModels import (
    SubscribersCountOnDayChart1monthFilter,
)

# from Database.DAL import UserDAL

logger = getLogger(__name__)

channel_statistics_router = APIRouter()


async def _get_main_channel_statistic(
    body: MainStatFilter, db
) -> Union[MainStat, None]:
    # async with db as session:
    print(body)
    return MainStat(
        subscribers_total=123,
        subscribers_today=234,
        subscribers_week=456,
        subscribers_month=678,
        average_views_1month=999,
        average_views_24hours=111,
        er_72hours=12.0,
        er_24hours=456.1,
        mentions_count=12,
    )


async def _get_mention_in_channels_list(
    body: MentionInChannelsFilter, db
) -> MentionInChannelList:
    # async with db as session:
    #     async with session.begin():
    print(body)
    return MentionInChannelList(
        mention_in_channel_list=[
            MentionInChannel(
                profile_img_url="_get_mention_in_channels_list",
                channel_name="_get_mention_in_channels_list",
                channel_id=-123123,
                members_count=123,
                post_date=datetime(2023, 11, 11),
            )
        ]
    )


async def _get_subscribers_count_on_day_chart_1month(
    body: SubscribersCountOnDayChart1monthFilter, db
) -> SubscribersCountOnDayChart1month:
    # async with db as session:
    #     async with session.begin():
    print(body)
    return SubscribersCountOnDayChart1month(
        subscribers_count_on_day_chart_1month=[
            SubscribersCountOnDay(
                subscribers_count=123, datetime=datetime(2023, 11, 11)
            )
        ]
    )


@channel_statistics_router.post("/main_channel_statistic", response_model=MainStat)
async def get_main_channel_statistic(
    body: MainStatFilter, db: AsyncSession = Depends(get_db)
) -> MainStat:
    try:
        return await _get_main_channel_statistic(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@channel_statistics_router.post(
    "/mention_in_channels_list", response_model=MentionInChannelList
)
async def get_mention_in_channels_list(
    body: MentionInChannelsFilter, db: AsyncSession = Depends(get_db)
) -> MentionInChannelList:
    try:
        return await _get_mention_in_channels_list(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@channel_statistics_router.post(
    "/get_subscribers_count_on_day_chart_1month",
    response_model=SubscribersCountOnDayChart1month,
)
async def get_subscribers_count_on_day_chart_1month(
    body: SubscribersCountOnDayChart1monthFilter, db: AsyncSession = Depends(get_db)
) -> SubscribersCountOnDayChart1month:
    try:
        return await _get_subscribers_count_on_day_chart_1month(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
