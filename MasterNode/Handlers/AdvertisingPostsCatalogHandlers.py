from logging import getLogger

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Database.session import get_db
from MasterNode.Models.AdvertisingPostsCatalogModels import AdvertisingPost
from MasterNode.Models.AdvertisingPostsCatalogModels import AdvertisingPostsList
from MasterNode.Models.AdvertisingPostsCatalogModels import Filters

# from typing import Union

logger = getLogger(__name__)

advertising_posts_catalog_router = APIRouter()


async def _search_advertising_posts_by_filters(
    body: Filters, db
) -> AdvertisingPostsList:
    # async with db as session:
    #     async with session.begin():
    print(body)
    return AdvertisingPostsList(
        advertising_posts_list=[
            AdvertisingPost(channel_name="AdvertisingPostsList", post_id=123)
        ],
        pages_count=1,
    )


@advertising_posts_catalog_router.post(
    "/search_advertising_posts_by_filters", response_model=AdvertisingPostsList
)
async def search_advertising_posts_by_filters(
    body: Filters, db: AsyncSession = Depends(get_db)
) -> AdvertisingPostsList:
    try:
        return await _search_advertising_posts_by_filters(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
