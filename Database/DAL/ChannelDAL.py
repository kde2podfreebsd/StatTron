from typing import List
from typing import Union

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Models.ChannelModel import Channel

# from sqlalchemy import and_


class ChannelDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_channel(
        self,
        id_channel: int,
        name: str,
        link: str,
        avatar_url: str,
        description: str,
        subs_total: int,
    ) -> Union[Channel, List[Channel]]:

        if (
            await self.db_session.execute(
                select(Channel).where(Channel.id_channel == id_channel)
            )
            is None
        ):
            new_channel = Channel(
                id_channel=id_channel,
                name=name,
                link=link,
                avatar_url=avatar_url,
                description=description,
                subs_total=subs_total,
            )
            self.db_session.add(new_channel)
            await self.db_session.flush()
            return new_channel

        else:

            query = (
                update(Channel)
                .where(Channel.id_channel == id_channel)
                .values(
                    name=name,
                    link=link,
                    avatar_url=avatar_url,
                    description=description,
                    subs_total=subs_total,
                )
                .returning(Channel)
            )

            res = await self.db_session.execute(query)
            channel_row = res.fetchone()
            channels = channel_row[0]
            if channels is not None:
                return channels

    async def select_all_channels(self):
        query = select(Channel)
        res = await self.db_session.execute(query)
        channel_row = res.fetchmany()
        channels = list(x[0] for x in channel_row)
        if channels is not None:
            return channels

    async def select_by_id(self, id_channel: int):
        query = select(Channel).where(Channel.id_channel == id_channel)
        res = await self.db_session.execute(query)
        channel_row = res.fetchone()
        if channel_row is not None:
            return channel_row[0]

    # async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
    #     query = (
    #         update(User)
    #         .where(and_(User.user_id == user_id, User.is_active == True))
    #         .values(is_active=False)
    #         .returning(User.user_id)
    #     )
    #     res = await self.db_session.execute(query)
    #     deleted_user_id_row = res.fetchone()
    #     if deleted_user_id_row is not None:
    #         return deleted_user_id_row[0]
    #
    # async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
    #     query = select(User).where(User.user_id == user_id)
    #     res = await self.db_session.execute(query)
    #     user_row = res.fetchone()
    #     if user_row is not None:
    #         return user_row[0]
    #
    # async def update_channel_simple(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
    #     query = (
    #         update(User)
    #         .where(and_(User.user_id == user_id, User.is_active == True))
    #         .values(kwargs)
    #         .returning(User.user_id)
    #     )
    #     res = await self.db_session.execute(query)
    #     update_user_id_row = res.fetchone()
    #     if update_user_id_row is not None:
    #         return update_user_id_row[0]
