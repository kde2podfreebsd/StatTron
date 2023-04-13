# from sqlalchemy import and_
# from sqlalchemy import select
# from sqlalchemy import update
from sqlalchemy import Date
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Models.SubPerDayModel import SubPerDay


class SubPerDayDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_sub_per_day(
            self,
            date: Date,
            subs: int,
            id_channel: int
    ) -> SubPerDay:

        new_sub_per_day = SubPerDay(
            date=date,
            subs=subs,
            id_channel=id_channel
        )
        self.db_session.add(new_sub_per_day)
        await self.db_session.flush()
        return new_sub_per_day
