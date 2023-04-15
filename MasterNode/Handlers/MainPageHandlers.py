from datetime import datetime
from logging import getLogger
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Database.session import get_db
from MasterNode.Models.MainPageModels import AdvertisingRecordsByDay
from MasterNode.Models.MainPageModels import AdvertisingRecordsByDayChart
from MasterNode.Models.MainPageModels import AdvertisingRecordsByHours
from MasterNode.Models.MainPageModels import AdvertisingRecordsByHoursChart
from MasterNode.Models.MainPageModels import TopActiveChannel
from MasterNode.Models.MainPageModels import TopActiveChannels
from MasterNode.Models.MainPageModels import TopChannelBy72hER
from MasterNode.Models.MainPageModels import TopChannelByNewSubscribers_today
from MasterNode.Models.MainPageModels import TopChannelByNewSubscribers_week
from MasterNode.Models.MainPageModels import TopChannelByNewSubscribers_yesterday
from MasterNode.Models.MainPageModels import TopChannelsBy72hER
from MasterNode.Models.MainPageModels import TopChannelsByNewSubscribers

# from Database.DAL import UserDAL

logger = getLogger(__name__)

main_page_router = APIRouter()


async def _get_top_active_channels(db) -> Union[TopActiveChannels, None]:
    # async with db as session:
    return TopActiveChannels(
        top_active_channels=[
            TopActiveChannel(
                channel_name="ch1",
                profile_img_url="abc",
                description="qwe",
                subscribers=100,
                total_views_last_month=5000,
                channel_id=-123498765,
            ),
            TopActiveChannel(
                channel_name="ch2",
                profile_img_url="abc",
                description="qwe",
                subscribers=100,
                total_views_last_month=5000,
                channel_id=-123498765,
            ),
        ]
    )


async def _get_top_channels_by_new_subscribers_today(
    db,
) -> Union[TopChannelsByNewSubscribers, None]:
    # async with db as session:
    #     async with session.begin():

    return TopChannelsByNewSubscribers(
        top_channels_by_new_subscribers=[
            TopChannelByNewSubscribers_today(
                channel_name="TopChannelByNewSubscribers_today",
                profile_img_url="123",
                subscribers=123,
                channel_id=-123,
                new_subscribers_today=111,
            ),
            TopChannelByNewSubscribers_today(
                channel_name="TopChannelByNewSubscribers_today",
                profile_img_url="1233",
                subscribers=123,
                channel_id=-1235,
                new_subscribers_today=111,
            ),
        ]
    )


async def _get_top_channels_by_new_subscribers_yesterday(
    db,
) -> Union[TopChannelsByNewSubscribers, None]:
    # async with db as session:
    #     async with session.begin():

    return TopChannelsByNewSubscribers(
        top_channels_by_new_subscribers=[
            TopChannelByNewSubscribers_yesterday(
                channel_name="TopChannelByNewSubscribers_yesterday",
                profile_img_url="123",
                subscribers=123,
                channel_id=-123,
                new_subscribers_yesterday=111,
            ),
            TopChannelByNewSubscribers_yesterday(
                channel_name="TopChannelByNewSubscribers_yesterday",
                profile_img_url="1233",
                subscribers=123,
                channel_id=-1235,
                new_subscribers_yesterday=111,
            ),
        ]
    )


async def _get_top_channels_by_new_subscribers_week(
    db,
) -> Union[TopChannelsByNewSubscribers, None]:
    # async with db as session:
    #     async with session.begin():

    return TopChannelsByNewSubscribers(
        top_channels_by_new_subscribers=[
            TopChannelByNewSubscribers_week(
                channel_name="TopChannelByNewSubscribers_week",
                profile_img_url="123",
                subscribers=123,
                channel_id=-123,
                new_subscribers_week=111,
            ),
            TopChannelByNewSubscribers_week(
                channel_name="TopChannelByNewSubscribers_week",
                profile_img_url="1233",
                subscribers=123,
                channel_id=-1235,
                new_subscribers_week=111,
            ),
        ]
    )


async def _get_top_channels_by_72hours_er(db) -> Union[TopChannelsBy72hER, None]:
    # async with db as session:
    #     async with session.begin():

    return TopChannelsBy72hER(
        top_channels_by_72hours_er=[
            TopChannelBy72hER(
                channel_name="123",
                profile_img_url="abc",
                subscribers=123,
                channel_id=-10001,
                er_72hours=20.52,
            ),
            TopChannelBy72hER(
                channel_name="1234",
                profile_img_url="abc1",
                subscribers=1243,
                channel_id=-1000221,
                er_72hours=24.00,
            ),
        ]
    )


async def _get_advertising_records_by_day_chart(
    db,
) -> Union[AdvertisingRecordsByDayChart, None]:
    # async with db as session:
    #     async with session.begin():

    return AdvertisingRecordsByDayChart(
        advertising_records_by_day_chart=[
            AdvertisingRecordsByDay(
                advertising_records_1month=10,
                day_1month=datetime(2022, 12, 1),
                advertising_records_3month=30,
                day_3month=datetime(2022, 11, 1),
                advertising_records_6month=60,
                day_6month=datetime(2022, 10, 1),
            )
        ]
    )


async def _get_advertising_records_by_hours_chart(
    db,
) -> Union[AdvertisingRecordsByHoursChart, None]:

    return AdvertisingRecordsByHoursChart(
        advertising_records_by_hours_chart=[
            AdvertisingRecordsByHours(
                advertising_records_count=10,
                advertising_records_percentage=20.12,
                hour="13:00",
            )
        ]
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


@main_page_router.get("/top_channels_by_72hours_er", response_model=TopChannelsBy72hER)
async def get_top_channels_by_72hours_er(
    db: AsyncSession = Depends(get_db),
) -> TopChannelsBy72hER:
    top_channels_by_72hours_er = await _get_top_channels_by_72hours_er(db)
    if top_channels_by_72hours_er is None:
        raise HTTPException(status_code=404, detail="Channels database is empty")
    return top_channels_by_72hours_er


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
