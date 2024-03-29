# from datetime import datetime
from logging import getLogger

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Database.session import get_db
from MasterNode.Models.СhannelСatalogModels import ByBaseFilters
from MasterNode.Models.СhannelСatalogModels import ByLinkFilter
from MasterNode.Models.СhannelСatalogModels import ByNameFilter
from MasterNode.Models.СhannelСatalogModels import Channel
from MasterNode.Models.СhannelСatalogModels import ChannelsList

from Database.DAL.ChannelDAL import ChannelDAL

# from typing import Union

logger = getLogger(__name__)

channel_catalog_router = APIRouter()


async def _search_by_link(body: ByLinkFilter, db) -> Channel:
    async with db as session:
        async with session.begin():
            channel = ChannelDAL(session)
            res = await channel.search_channel_by_link(url=body.URL)
            return Channel(
                channel_name=res[0].channel_name,
                channel_id=res[0].channel_id,
                profile_img_url=res[0].profile_img_url,
                description=res[0].description,
                subscribers=res[0].subscribers,
                new_subscribers_today=res[0].new_subscribers_today,
                average_post_views_yesterday=res[0].average_post_views_yesterday,
                er=res[0].er
            )


async def _search_by_name(body: ByNameFilter, db) -> ChannelsList:
    async with db as session:
        async with session.begin():
            channel = ChannelDAL(session)
            # await channel.search_by_username(name=body.channel_name, page=body.page)
            res, pages_count = await channel.search_by_username(name=body.channel_name, page=body.page)
            print(pages_count, res)
            # channels_list = []
            # for item in res:
            #     channels_list.append(Channel(
            #         channel_name=item.channel_name,
            #         channel_id=item.channel_id,
            #         profile_img_url=item.profile_img_url,
            #         description=item.description,
            #         subscribers=item.subscribers,
            #         new_subscribers_today=item.new_subscribers_today,
            #         average_post_views_yesterday=item.average_post_views_yesterday,
            #         er=item.er,
            #     ), pages_count=pages_count)
            # return ChannelsList(
            #     channels_list=channels_list
            # )
            return ChannelsList(
                channels_list=[
                    Channel(
                        channel_name="_search_by_name",
                        channel_id=-239123,
                        profile_img_url="img url",
                        description="description",
                        subscribers=123123,
                        new_subscribers_today=12333,
                        average_post_views_yesterday=123123,
                        er=56.5,
                    )
                ],
                pages_count=2,
            )


async def _search_by_base_filters(body: ByBaseFilters, db) -> ChannelsList:
    async with db as session:
        async with session.begin():
            channel = ChannelDAL(session)
            # res = await channel.
    print(body)
    return ChannelsList(
        channels_list=[
            Channel(
                channel_name="_search_by_base_filters",
                channel_id=-239123,
                profile_img_url="img url",
                description="description",
                subscribers=123123,
                new_subscribers_today=12333,
                average_post_views_yesterday=123123,
                er=56.5,
            )
        ],
        pages_count=3,
    )


@channel_catalog_router.post("/search_by_link", response_model=Channel)
async def search_by_link(
        body: ByLinkFilter, db: AsyncSession = Depends(get_db)
) -> Channel:
    try:
        return await _search_by_link(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@channel_catalog_router.post("/search_by_name", response_model=Channel)
async def search_by_name(
        body: ByNameFilter, db: AsyncSession = Depends(get_db)
) -> Channel:
    try:
        return await _search_by_name(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@channel_catalog_router.post("/search_by_base_filters", response_model=ChannelsList)
async def search_by_base_filters(
        body: ByBaseFilters, db: AsyncSession = Depends(get_db)
) -> ChannelsList:
    try:
        return await _search_by_base_filters(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
