from math import floor
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from Database.Models.ChannelModel import Channel
from SlaveNode.UserBotServer.responseRoute import MainPageTopChannelsER
from SlaveNode.UserBotServer.responseRoute import MainPageTopChannelsUpSubsToday
from SlaveNode.UserBotServer.responseRoute import MainPageTopChannelsUpSubsYesterday
from SlaveNode.UserBotServer.responseRoute import MainPageTopChannelsUpSubsWeek
from SlaveNode.UserBotServer.responseRoute import MainPageGraphicMentionPerHour
from typing import Union, List

class ChannelDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def _create_channel(
        self,
        id_channel: int,
        name: str,
        link: str,
        avatar_url: str,
        description: str,
        subs_total: int,
    ) -> Union[Channel, List[Channel]]:

        not_empty = await self.db_session.execute(select(Channel).where(Channel.id_channel == id_channel))
        not_empty = not_empty.fetchone()
        if not_empty is None:
            new_channel = Channel(
                id_channel=id_channel,
                name=name,
                link=link,
                avatar_url=avatar_url,
                description=description,
                subs_total=subs_total
            )
            self.db_session.add(new_channel)
            await self.db_session.flush()
            return new_channel

        else:

            query = update(Channel).where(
                Channel.id_channel == id_channel
            ).values(
                name=name,
                link=link,
                avatar_url=avatar_url,
                description=description,
                subs_total=subs_total
            ).returning(Channel)

            res = await self.db_session.execute(query)
            channel_row = res.fetchone()
            if channel_row is not None:
                return channel_row[0]

    async def _select_all_channels(self):
        query = select(Channel)
        res = await self.db_session.execute(query)
        channel_row = res.fetchmany()
        if channel_row is not None:
            return list(x[0] for x in channel_row)

    async def _select_by_id(
            self,
            id_channel: int
    ):
        query = select(Channel).where(Channel.id_channel == id_channel)
        res = await self.db_session.execute(query)
        channel_row = res.fetchone()
        if channel_row is not None:
            return channel_row[0]

    async def top_active_channel(self):
        query = """
                SELECT
                name,
                avatar_url,
                description,
                subs_total,
                CAST(tv.total_views AS bigint),
                channel.id_channel,
                CAST(ROUND(avg_views_per_post / subs_total * 100) AS smallint) AS ER
                FROM channel
                INNER JOIN (SELECT id_channel, (sum(views) / count(id_post)) as avg_views_per_post from post
                            WHERE post.date > now() - interval '3 day'
                            GROUP BY id_channel) AS avg
            
                            ON channel.id_channel = avg.id_channel
                
                INNER JOIN (SELECT post.id_channel, SUM(views) AS total_views 
                            FROM channel
                            INNER JOIN post ON channel.id_channel = post.id_channel
                                                AND now() - post.date < interval '31 day'
                            GROUP BY post.id_channel) AS tv
                            
                            ON channel.id_channel = tv.id_channel
            
                WHERE channel.subs_total > ANY(SELECT subs_total FROM channel
                                                ORDER BY subs_total DESC
                                                LIMIT ROUND(0.5 * (SELECT count(*) FROM channel)))
                ORDER BY ER DESC
                LIMIT 6
                """
        res = await self.db_session.execute(text(query))
        channel_row = res.fetchall()
        if res is not None:
            response: List[MainPageTopChannelsER] = list()
            for channel in channel_row:

                response.append(
                    MainPageTopChannelsER(
                        channel_name=channel[0],
                        profile_img_url=channel[1],
                        description=channel[2],
                        subscribers=channel[3],
                        total_views_last_month=channel[4],
                        channel_id=channel[5]
                    )
                )

            return response

    async def top_channels_by_new_subscribers_today(self):
        query = """
                SELECT
                channel.name,
                channel.avatar_url,
                channel.subs_total,
                channel.id_channel,
                channel.subs_total - yesterday.subs AS grow
                FROM channel
                INNER JOIN 
                        (SELECT subs, id_channel FROM sub_per_day
                        WHERE date = date(now()) - interval '1 day') AS yesterday
                        USING(id_channel)
                ORDER BY 5 DESC, 1 ASC
                LIMIT 6
                """
        res = await self.db_session.execute(text(query))
        channel_row = res.fetchall()
        if res is not None:
            response: List[MainPageTopChannelsUpSubsToday] = list()
            for channel in channel_row:

                response.append(
                    MainPageTopChannelsUpSubsToday(
                        channel_name=channel[0],
                        profile_img_url=channel[1],
                        subscribers=channel[2],
                        channel_id=channel[3],
                        new_subscribers_today=channel[4]
                    )
                )

            return response

    async def top_channels_by_new_subscribers_yesterday(self):
        query = """
                SELECT 
                channel.name,
                channel.avatar_url,
                channel.subs_total,
                channel.id_channel,
                one_day_ago.subs - two_day_ago.subs AS grow
                FROM channel
                    INNER JOIN (SELECT subs, id_channel, date FROM sub_per_day
                                WHERE date = date(now()) - interval '1 day') AS one_day_ago
                                USING(id_channel)
                    INNER JOIN (SELECT subs, id_channel, date FROM sub_per_day
                                WHERE date = date(now()) - interval '2 day') AS two_day_ago
                                USING(id_channel)
                                
                ORDER BY 5 DESC, 1 ASC
                LIMIT 6
                """
        res = await self.db_session.execute(text(query))
        channel_row = res.fetchall()
        if res is not None:
            response: List[MainPageTopChannelsUpSubsYesterday] = list()
            for channel in channel_row:

                response.append(
                    MainPageTopChannelsUpSubsYesterday(
                        channel_name=channel[0],
                        profile_img_url=channel[1],
                        subscribers=channel[2],
                        channel_id=channel[3],
                        new_subscribers_yesterday=channel[4]
                    )
                )

            return response

    async def top_channels_by_new_subscribers_week(self):
        query = """
                SELECT
                channel.name,
                channel.avatar_url,
                channel.subs_total,
                channel.id_channel,
                channel.subs_total - one_week_ago.subs AS grow
                FROM channel
                INNER JOIN 
                        (SELECT subs, id_channel FROM sub_per_day
                        WHERE date = date(now()) - interval '1 week') AS one_week_ago
                        USING(id_channel)
                ORDER BY 5 DESC, 1 ASC
                LIMIT 6
                """
        res = await self.db_session.execute(text(query))
        channel_row = res.fetchall()
        if res is not None:
            response: List[MainPageTopChannelsUpSubsWeek] = list()
            for channel in channel_row:
                response.append(
                    MainPageTopChannelsUpSubsWeek(
                        channel_name=channel[0],
                        profile_img_url=channel[1],
                        subscribers=channel[2],
                        channel_id=channel[3],
                        new_subscribers_week=channel[4]
                    )
                )

            return response

    async def advertising_records_by_hours_chart(self):
        query = """
                SELECT 
                COUNT(mention.id_post) AS mentions_per_hour,
                CAST(
                    ROUND(
                        CAST(COUNT(mention.id_post) AS NUMERIC) * 100 
                        / 
                        CAST((SELECT COUNT(*) FROM mention WHERE mention.id_channel <> mention.id_mentioned_channel) AS NUMERIC)
                        , 2) 
                AS FLOAT) AS percent,
                EXTRACT(HOUR FROM post.date) AS hour
                FROM mention
                    INNER JOIN post ON mention.id_post = post.id_post 
                                    AND mention.id_channel = post.id_channel
                    
                WHERE mention.id_channel <> mention.id_mentioned_channel
                GROUP BY 3
                ORDER BY 3 
                """
        res = await self.db_session.execute(text(query))
        mentions_row = res.fetchall()
        if res is not None:
            response: List[MainPageGraphicMentionPerHour] = list()
            for mention in mentions_row:
                response.append(
                    MainPageGraphicMentionPerHour(
                        advertising_record_count=mention[0],
                        advertising_record_percentage=mention[1],
                        hour=str(mention[2])
                    )
                )

            return response

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
