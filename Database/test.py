import asyncio

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Database.DAL.ChannelDAL import ChannelDAL
from Database.session import get_db


async def test(session: AsyncSession = Depends(get_db)):
    session = get_db()
    async with session:
        async with session.begin():

            ChannelDAL(session)
            print("kek")

            # await new_channel.create_channel(
            #     id_channel=123,
            #     name="123",
            #
            # )


asyncio.run(test())
