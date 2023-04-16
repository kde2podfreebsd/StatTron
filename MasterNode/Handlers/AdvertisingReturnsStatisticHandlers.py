# from datetime import datetime
from logging import getLogger
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Database.session import get_db
from MasterNode.Models.AdvertisingReturnsStatisticModels import (
    AdvertisingReturnsStatistic,
)
from MasterNode.Models.AdvertisingReturnsStatisticModels import (
    AdvertisingReturnsStatisticFilter,
)

# from Database.DAL import UserDAL

logger = getLogger(__name__)

advertising_returns_statistic_router = APIRouter()


async def _get_advertising_returns_statistic(
    body: AdvertisingReturnsStatisticFilter, db
) -> Union[AdvertisingReturnsStatistic, None]:
    # async with db as session:
    print(body)
    return AdvertisingReturnsStatistic(
        advertising_posts_count_all_time=123,
        repost_count_all_time=123,
        advertising_posts_count_week=123,
        repost_count_week=123,
        advertising_posts_count_month=123,
        repost_count_month=123,
    )


@advertising_returns_statistic_router.post(
    "/get_advertising_returns_statistic", response_model=AdvertisingReturnsStatistic
)
async def get_advertising_returns_statistic(
    body: AdvertisingReturnsStatisticFilter, db: AsyncSession = Depends(get_db)
) -> AdvertisingReturnsStatistic:
    try:
        return await _get_advertising_returns_statistic(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
