from datetime import datetime
from logging import getLogger
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Database.DAL.ChannelDAL import ChannelDAL
from Database.session import get_db
from MasterNode.Models.MainPageModels import AdvertisingRecordsByDay
from MasterNode.Models.MainPageModels import AdvertisingRecordsByDayChart
from MasterNode.Models.MainPageModels import AdvertisingRecordsByHours
from MasterNode.Models.MainPageModels import AdvertisingRecordsByHoursChart
from MasterNode.Models.MainPageModels import TopActiveChannel
from MasterNode.Models.MainPageModels import TopActiveChannels
from MasterNode.Models.MainPageModels import TopChannelByNewSubscribers_today
from MasterNode.Models.MainPageModels import TopChannelByNewSubscribers_week
from MasterNode.Models.MainPageModels import TopChannelByNewSubscribers_yesterday
from MasterNode.Models.MainPageModels import TopChannelsByNewSubscribers

logger = getLogger(__name__)

main_page_router = APIRouter()


async def _get_top_active_channels(db) -> Union[TopActiveChannels, None]:
    async with db as session:
        async with session.begin():
            channel = ChannelDAL(session)
            res = await channel.top_active_channel()
            top_active_channels = []
            for item in res:
                top_active_channels.append(
                    TopActiveChannel(
                        channel_name=item.channel_name,
                        profile_img_url=item.profile_img_url,
                        description=item.description,
                        subscribers=item.subscribers,
                        total_views_last_month=item.total_views_last_month,
                        channel_id=item.channel_id,
                    )
                )

            return TopActiveChannels(top_active_channels=top_active_channels)


async def _get_top_channels_by_new_subscribers_today(
    db,
) -> Union[TopChannelsByNewSubscribers, None]:
    async with db as session:
        async with session.begin():
            channel = ChannelDAL(session)
            res = await channel.top_channels_by_new_subscribers_today()
            top_channels_by_new_subscribers = []
            for item in res:
                top_channels_by_new_subscribers.append(
                    TopChannelByNewSubscribers_today(
                        channel_name=item.channel_name,
                        profile_img_url=item.profile_img_url,
                        subscribers=item.subscribers,
                        channel_id=item.channel_id,
                        new_subscribers_today=item.new_subscribers_today,
                    )
                )

            return TopChannelsByNewSubscribers(
                top_channels_by_new_subscribers=top_channels_by_new_subscribers
            )


async def _get_top_channels_by_new_subscribers_yesterday(
    db,
) -> Union[TopChannelsByNewSubscribers, None]:
    async with db as session:
        async with session.begin():
            channel = ChannelDAL(session)
            res = await channel.top_channels_by_new_subscribers_yesterday()
            top_channels_by_new_subscribers = []
            for item in res:
                top_channels_by_new_subscribers.append(
                    TopChannelByNewSubscribers_yesterday(
                        channel_name=item.channel_name,
                        profile_img_url=item.profile_img_url,
                        subscribers=item.subscribers,
                        channel_id=item.channel_id,
                        new_subscribers_yesterday=item.new_subscribers_yesterday,
                    )
                )

            return TopChannelsByNewSubscribers(
                top_channels_by_new_subscribers=top_channels_by_new_subscribers
            )


async def _get_top_channels_by_new_subscribers_week(
    db,
) -> Union[TopChannelsByNewSubscribers, None]:
    async with db as session:
        async with session.begin():
            channel = ChannelDAL(session)
            res = await channel.top_channels_by_new_subscribers_week()
            top_channels_by_new_subscribers = []
            for item in res:
                top_channels_by_new_subscribers.append(
                    TopChannelByNewSubscribers_week(
                        channel_name=item.channel_name,
                        profile_img_url=item.profile_img_url,
                        subscribers=item.subscribers,
                        channel_id=item.channel_id,
                        new_subscribers_week=item.new_subscribers_week,
                    )
                )

            return TopChannelsByNewSubscribers(
                top_channels_by_new_subscribers=top_channels_by_new_subscribers
            )


async def _get_advertising_records_by_day_chart(
    db,
) -> Union[AdvertisingRecordsByDayChart, None]:
    async with db as session:
        async with session.begin():
            channel = ChannelDAL(session)
            res = await channel.advertising_record_by_day_chart()
            advertising_records_by_day_chart = []
            for item in res:
                advertising_records_by_day_chart.append(
                    AdvertisingRecordsByDay(
                        advertising_records_1month=item.advertising_records_1month,
                        day_1month=item.day_1month,
                        advertising_records_3month=item.advertising_records_3month,
                        day_3month=item.day_3month,
                        advertising_records_6month=item.advertising_records_6month,
                        day_6month=item.day_6month,
                    )
                )

            return AdvertisingRecordsByDayChart(
                advertising_records_by_day_chart=advertising_records_by_day_chart
            )


async def _get_advertising_records_by_hours_chart(
    db,
) -> Union[AdvertisingRecordsByHoursChart, None]:
    async with db as session:
        async with session.begin():
            channel = ChannelDAL(session)
            res = await channel.advertising_records_by_hours_chart()
            advertising_records_by_hours_chart = []
            for item in res:
                advertising_records_by_hours_chart.append(
                    AdvertisingRecordsByHours(
                        advertising_records_count=item.advertising_record_count,
                        advertising_records_percentage=item.advertising_record_percentage,
                        hour=item.hour,
                    )
                )

            return AdvertisingRecordsByHoursChart(
                advertising_records_by_hours_chart=advertising_records_by_hours_chart
            )


@main_page_router.get("/top_active_channels", response_model=TopActiveChannels)
async def get_top_active_channels(
    db: AsyncSession = Depends(get_db),
) -> TopActiveChannels:
    top_active_channels = await _get_top_active_channels(db)
    if top_active_channels is None:
        raise HTTPException(status_code=404, detail="Channels database is empty")
    return top_active_channels


@main_page_router.get(
    "/top_channels_by_new_subscribers_today", response_model=TopChannelsByNewSubscribers
)
async def get_top_channels_by_new_subscribers_today(
    db: AsyncSession = Depends(get_db),
) -> TopChannelsByNewSubscribers:
    top_channels_by_new_subscribers = await _get_top_channels_by_new_subscribers_today(
        db
    )
    if top_channels_by_new_subscribers is None:
        raise HTTPException(status_code=404, detail="Channels database is empty")
    return top_channels_by_new_subscribers


@main_page_router.get(
    "/top_channels_by_new_subscribers_yesterday",
    response_model=TopChannelsByNewSubscribers,
)
async def get_top_channels_by_new_subscribers_yesterday(
    db: AsyncSession = Depends(get_db),
) -> TopChannelsByNewSubscribers:
    top_channels_by_new_subscribers = (
        await _get_top_channels_by_new_subscribers_yesterday(db)
    )
    if top_channels_by_new_subscribers is None:
        raise HTTPException(status_code=404, detail="Channels database is empty")
    return top_channels_by_new_subscribers


@main_page_router.get(
    "/top_channels_by_new_subscribers_week", response_model=TopChannelsByNewSubscribers
)
async def get_top_channels_by_new_subscribers_week(
    db: AsyncSession = Depends(get_db),
) -> TopChannelsByNewSubscribers:
    top_channels_by_new_subscribers = await _get_top_channels_by_new_subscribers_week(
        db
    )
    if top_channels_by_new_subscribers is None:
        raise HTTPException(status_code=404, detail="Channels database is empty")
    return top_channels_by_new_subscribers


@main_page_router.get(
    "/advertising_records_by_day_chart", response_model=AdvertisingRecordsByDayChart
)
async def get_advertising_records_by_day_chart(
    db: AsyncSession = Depends(get_db),
) -> AdvertisingRecordsByDayChart:
    advertising_records_by_day_chart = await _get_advertising_records_by_day_chart(db)
    if advertising_records_by_day_chart is None:
        raise HTTPException(status_code=404, detail="Channels database is empty")
    return advertising_records_by_day_chart


@main_page_router.get(
    "/advertising_records_by_hours_chart", response_model=AdvertisingRecordsByHoursChart
)
async def get_advertising_records_by_hours_chart(
    db: AsyncSession = Depends(get_db),
) -> AdvertisingRecordsByHoursChart:
    advertising_records_by_hours_chart = await _get_advertising_records_by_hours_chart(
        db
    )
    if advertising_records_by_hours_chart is None:
        raise HTTPException(status_code=404, detail="Channels database is empty")
    return advertising_records_by_hours_chart
