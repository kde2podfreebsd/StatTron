from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Models.MentionModel import Mention


class MentionDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_mention(
        self, id_mentioned_channel: int, id_post: int, id_channel: int
    ) -> Mention:
        try:

            not_empty = await self.db_session.execute(
                select(Mention).where(
                    and_(
                        Mention.id_post == id_post,
                        Mention.id_channel == id_channel,
                        Mention.id_mentioned_channel == id_mentioned_channel
                    )
                )
            )
            not_empty = not_empty.fetchone()

            if not_empty is None:

                new_mention = Mention(
                    id_mentioned_channel=id_mentioned_channel,
                    id_post=id_post,
                    id_channel=id_channel,
                )
                self.db_session.add(new_mention)
                await self.db_session.flush()
                return new_mention

        except Exception as e:
            print(e)