import datetime
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from Database.DAL.ChannelDAL import ChannelDAL
from Database.Models.PostModel import Post


class PostDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_post(
        self,
        id_post: int,
        id_channel: int,
        date: datetime.date,
        text: str,
        views: int,
        id_channel_forward_from: int,
    ) -> Post:
        try:

            channel = ChannelDAL(db_session=self.db_session)

            already_exists = await channel._select_by_id(id_channel_forward_from)

            if already_exists is None:
                id_channel_forward_from = None

            not_empty = await self.db_session.execute(
                    select(Post).where(
                        and_(
                            Post.id_post == id_post,
                            Post.id_channel == id_channel
                        )
                    )
            )
            not_empty = not_empty.fetchone()

            if not_empty is None:
                new_post = Post(
                    id_post=id_post,
                    id_channel=id_channel,
                    date=date,
                    text=text,
                    views=views,
                    id_channel_forward_from=id_channel_forward_from,
                )
                self.db_session.add(new_post)
                await self.db_session.flush()
                return new_post

            else:
                query = update(Post).where(
                    and_(
                        Post.id_post == id_post,
                        Post.id_channel == id_channel
                    )
                ).values(
                    views=views
                ).returning(Post)

                res = await self.db_session.execute(query)
                post_row = res.fetchone()
                if post_row is not None:
                    return post_row[0]

        except Exception as e:
            print(e)
