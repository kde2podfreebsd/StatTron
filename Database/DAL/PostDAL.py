# from sqlalchemy import and_
# from sqlalchemy import select
# from sqlalchemy import update
from sqlalchemy import Date
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Models.PostModel import Post


class PostDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_post(
            self,
            id_post: int,
            id_channel: int,
            date: Date,
            views: int,
            id_channel_forward_from: int
    ) -> Post:

        new_post = Post(
            id_post=id_post,
            id_channel=id_channel,
            date=date,
            views=views,
            id_channel_forward_from=id_channel_forward_from
        )
        self.db_session.add(new_post)
        await self.db_session.flush()
        return new_post
