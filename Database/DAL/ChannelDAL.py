from typing import List, Optional
from typing import Union

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from Database.Models.ChannelModel import Channel
from SlaveNode.UserBotServer.responseRoute import MainPageGraphicMentionPerHour
from SlaveNode.UserBotServer.responseRoute import MainPageTopChannelsER
from SlaveNode.UserBotServer.responseRoute import MainPageTopChannelsUpSubsToday
from SlaveNode.UserBotServer.responseRoute import MainPageTopChannelsUpSubsWeek
from SlaveNode.UserBotServer.responseRoute import MainPageTopChannelsUpSubsYesterday
from SlaveNode.UserBotServer.responseRoute import SearchChannelByLinkAndByName
from SlaveNode.UserBotServer.responseRoute import TripleCharts
from SlaveNode.UserBotServer.responseRoute import TopActiveChannelByER72hours


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

        not_empty = await self.db_session.execute(
            select(Channel).where(Channel.id_channel == id_channel)
        )
        not_empty = not_empty.fetchone()
        if not_empty is None:
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
            if channel_row is not None:
                return channel_row[0]

    async def _select_all_channels(self):
        query = select(Channel)
        res = await self.db_session.execute(query)
        channel_row = res.fetchall()
        if channel_row is not None:
            return list(x[0] for x in channel_row)

    async def _select_by_id(self, id_channel: int):
        query = select(Channel).where(Channel.id_channel == id_channel)
        res = await self.db_session.execute(query)
        channel_row = res.fetchone()
        if channel_row is not None:
            return channel_row[0]

    async def top_active_channel(self):
        """Return top active channels for maximum ER for 1 week from 50% top channels by total subscribers"""
        query = """
                SELECT
                name,
                avatar_url,
                description,
                subs_total,
                CAST(COALESCE(tv.total_views, 0) AS bigint),
                channel.id_channel,
                CAST(ROUND(COALESCE(avg_views_per_post, 0) / subs_total * 100) AS smallint) AS ER
                FROM channel
                LEFT JOIN (SELECT id_channel, (sum(views) / count(id_post)) as avg_views_per_post from post
                            WHERE post.date > now() - interval '7 day'
                            GROUP BY id_channel) AS avg

                            ON channel.id_channel = avg.id_channel

                LEFT JOIN (SELECT post.id_channel, SUM(views) AS total_views
                            FROM channel
                            INNER JOIN post ON channel.id_channel = post.id_channel
                                                AND now() - post.date < interval '30 day'
                            GROUP BY post.id_channel) AS tv

                            ON channel.id_channel = tv.id_channel

                WHERE channel.subs_total >= ANY(SELECT subs_total FROM channel
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
                        channel_id=channel[5],
                    )
                )

            return response

    # если данных за вчера нет то в new_subscribers_today приходит текущее кол-во подписчиков[баг] решение (приходит None)
    async def top_channels_by_new_subscribers_today(self):
        """Returns the top channels by subscriber growth for that day"""
        query = """
                SELECT
                channel.name,
                channel.avatar_url,
                channel.subs_total,
                channel.id_channel,
                channel.subs_total - COALESCE(yesterday.subs, 0) AS grow
                FROM channel
                LEFT JOIN
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
                        new_subscribers_today=channel[4],
                    )
                )

            return response

    # если данных за вчера и позавчера нет то в new_subscribers_yesterday приходит 0 [баг] решение (приходит None)

    async def top_channels_by_new_subscribers_yesterday(self):
        """Returns the top channels by subscriber growth for last day"""
        query = """
                SELECT
                channel.name,
                channel.avatar_url,
                channel.subs_total,
                channel.id_channel,
                COALESCE(one_day_ago.subs - two_day_ago.subs, 0) AS grow
                FROM channel
                    LEFT JOIN (SELECT subs, id_channel, date FROM sub_per_day
                                WHERE date = date(now()) - interval '1 day') AS one_day_ago
                                USING(id_channel)
                    LEFT JOIN (SELECT subs, id_channel, date FROM sub_per_day
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
                        new_subscribers_yesterday=channel[4],
                    )
                )

            return response

    async def top_channels_by_new_subscribers_week(self):
        """Returns the top channels by subscriber growth for last week"""
        query = """
                SELECT
                channel.name,
                channel.avatar_url,
                channel.subs_total,
                channel.id_channel,
                COALESCE(channel.subs_total - one_week_ago.subs, 0) AS grow
                FROM channel
                LEFT JOIN
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
                        new_subscribers_week=channel[4],
                    )
                )

            return response
    async def top_active_channel_by_er_72hours(self):
        query = """
                SELECT
                name,
                avatar_url,
                subs_total,
                channel.id_channel,
                CAST(ROUND(COALESCE(avg_views_per_post, 0) / subs_total * 100) AS smallint) AS ER
                FROM channel
                LEFT JOIN (SELECT id_channel, (sum(views) / count(id_post)) as avg_views_per_post from post
                            WHERE post.date > now() - interval '3 day'
                            GROUP BY id_channel) AS avg
                
                            ON channel.id_channel = avg.id_channel
                ORDER BY ER DESC
                LIMIT 6
                """
        res = await self.db_session.execute(text(query))
        channel_row = res.fetchall()
        if res is not None:
            response: List[TopActiveChannelByER72hours] = list()
            for channel in channel_row:
                response.append(
                    TopActiveChannelByER72hours(
                        channel_name=channel[0],
                        profile_img_url=channel[1],
                        subscribers=channel[2],
                        channel_id=channel[3],
                        er_72_hours=channel[4],
                    )
                )

            return response
    async def advertising_record_by_day_chart(self):
        """Returns 30 points for each of 3 charts for 1/3/6 months"""

        query_one_months = """
                            SELECT
                            last_30_day_dates::date,
                            COALESCE(flt.count_posts, 0)
                            FROM generate_series(current_date::date, (current_date - interval '29 day')::date, - interval '1 day'::interval) AS last_30_day_dates

                            LEFT JOIN
                            (
                                SELECT
                                date_trunc('day', date)::date AS date,
                                COUNT(mention.id_post) AS count_posts
                                FROM mention
                                    INNER JOIN post ON post.id_post = mention.id_post
                                                    AND post.id_channel = mention.id_channel
                                                    AND post.date > now() - interval '30 day'
                                WHERE mention.id_mentioned_channel <> mention.id_channel
                                GROUP BY 1
                                LIMIT 30
                            ) AS flt
                            ON last_30_day_dates::date = flt.date
                            ORDER BY 1 DESC
                            """

        query_three_months = """
                            SELECT to_timestamp(var.period_3_day * 259200)::date, count
                            FROM
                                (SELECT
                                FLOOR(EXTRACT('epoch' from date) / 259200) AS period_3_day,
                                COUNT(mention.id_post) AS count
                                FROM post
                                    LEFT JOIN mention ON post.id_post = mention.id_post
                                            AND post.id_channel = mention.id_channel
                                            AND mention.id_channel <> mention.id_mentioned_channel
                                GROUP BY 1
                                ORDER BY 1 DESC
                                LIMIT 30) AS var
                            """

        query_six_months = """
                            SELECT to_timestamp(var.period_3_day * 518400)::date, count
                            FROM
                                (SELECT
                                FLOOR(EXTRACT('epoch' from date) / 518400) AS period_3_day,
                                COUNT(mention.id_post) AS count
                                FROM post
                                    LEFT JOIN mention ON post.id_post = mention.id_post
                                            AND post.id_channel = mention.id_channel
                                            AND mention.id_channel <> mention.id_mentioned_channel
                                GROUP BY 1
                                ORDER BY 1 DESC
                                LIMIT 30) AS var
                            """
        res_1 = await self.db_session.execute(text(query_one_months))
        res_3 = await self.db_session.execute(text(query_three_months))
        res_6 = await self.db_session.execute(text(query_six_months))

        chart_1_month = res_1.fetchall()
        chart_3_month = res_3.fetchall()
        chart_6_month = res_6.fetchall()

        response: List[TripleCharts] = list()

        for x, y, z in zip(chart_1_month, chart_3_month, chart_6_month):

            response.append(
                TripleCharts(
                    day_1month=x[0],
                    advertising_records_1month=x[1],
                    day_3month=y[0],
                    advertising_records_3month=y[1],
                    day_6month=z[0],
                    advertising_records_6month=z[1],
                )
            )

        return response
    #с 0 по 23 час нужно
    async def advertising_records_by_hours_chart(self):
        query = """
                SELECT
                COALESCE(count_per_hour, 0),
                CAST(COALESCE(percent, 0) AS float),
                calendar.hours
                FROM
                (SELECT hours FROM generate_series(1, 24) AS hours) AS calendar
                LEFT JOIN
                (
                    SELECT
                    EXTRACT(hour FROM post.date) AS hour,
                    COUNT(mention.id_post) AS count_per_hour,
                    ROUND(CAST(COUNT(mention.id_post) AS NUMERIC) * 100
                    / CAST((SELECT COUNT(*) FROM mention WHERE mention.id_channel <> mention.id_mentioned_channel) AS NUMERIC), 2) AS percent
                    FROM mention
                    INNER JOIN post ON post.id_channel = mention.id_channel
                                    AND post.id_post = mention.id_post
                                    AND mention.id_channel <> id_mentioned_channel
                    GROUP BY hour) AS var
                ON calendar.hours = hour
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
                        hour=str(mention[2]),
                    )
                )

            return response
    async def search_channel_by_link(self, url: str, page: int):

        if "t.me" in url:
            username = url.split("/")[-1]
            if username == "":
                username = url.split("/")[-2]

            query = f"""
                    SELECT
                    channel.name,
                    channel.id_channel,
                    channel.avatar_url,
                    channel.description,
                    channel.subs_total,
                    COALESCE(channel.subs_total - yesterday_subs.subs, 0) AS new_subs_today,
                    CAST(COALESCE(avg_yesterday.avg_views_per_post, 0) AS int) as avg_views_per_post,
                    CAST(ROUND(COALESCE(avg_3_last_days.avg_views_per_post, 0) / channel.subs_total * 100) AS smallint) AS ER
                    FROM channel
                        LEFT JOIN (SELECT
                                    id_channel,
                                    FLOOR(SUM(views) / COUNT(id_post)) as avg_views_per_post
                                    FROM post
                                    WHERE post.date::date = (current_date - interval '1 day')::date
                                    GROUP BY id_channel) AS avg_yesterday
                                    ON channel.id_channel = avg_yesterday.id_channel
                    
                        LEFT JOIN (SELECT subs, id_channel FROM sub_per_day
                                    WHERE date = date(now()) - interval '1 day') AS yesterday_subs
                                    ON channel.id_channel = yesterday_subs.id_channel
                    
                        LEFT JOIN (SELECT
                                    id_channel,
                                    SUM(views) / COUNT(id_post) as avg_views_per_post
                                    FROM post
                                    WHERE post.date > now() - interval '3 days'
                                    GROUP BY id_channel) AS avg_3_last_days
                                    ON channel.id_channel = avg_3_last_days.id_channel
                    WHERE LOWER(channel.link) LIKE LOWER('%{username}%')
                    ORDER BY channel.name
                    LIMIT 6 OFFSET {6 * (page - 1)}
                      """
            res = await self.db_session.execute(text(query))
            channel_row = res.fetchall()
            if res is not None:

                response_count: int
                response_channel: List[SearchChannelByLinkAndByName] = list()

                query = f"""
                        SELECT
                        count(channel.id_channel)
                        FROM channel
                            LEFT JOIN (SELECT
                                        id_channel,
                                        FLOOR(SUM(views) / COUNT(id_post)) as avg_views_per_post
                                        FROM post
                                        WHERE post.date::date = (current_date - interval '1 day')::date
                                        GROUP BY id_channel) AS avg_yesterday
                                        ON channel.id_channel = avg_yesterday.id_channel

                            LEFT JOIN (SELECT subs, id_channel FROM sub_per_day
                                        WHERE date = date(now()) - interval '1 day') AS yesterday_subs
                                        ON channel.id_channel = yesterday_subs.id_channel

                            LEFT JOIN (SELECT
                                        id_channel,
                                        SUM(views) / COUNT(id_post) as avg_views_per_post
                                        FROM post
                                        WHERE post.date > now() - interval '3 days'
                                        GROUP BY id_channel) AS avg_3_last_days
                                        ON channel.id_channel = avg_3_last_days.id_channel
                        WHERE LOWER(channel.name) LIKE LOWER('%{username}%')
                        """
                res = await self.db_session.execute(text(query))
                count_row = res.fetchone()
                response_count = count_row[0]

                for channel in channel_row:
                    response_channel.append(
                        SearchChannelByLinkAndByName(
                            channel_name=channel[0],
                            channel_id=channel[1],
                            profile_img_url=channel[2],
                            description=channel[3],
                            subscribers=channel[4],
                            new_subscribers_today=channel[5],
                            average_post_views_yesterday=channel[6],
                            er=channel[7],
                        )
                    )

                return [response_channel, response_count]
        else:
            return []

    async def search_by_username(self, name: str, page: int):

        name = name.lower().split()
        query = f"""
                SELECT
                channel.name,
                channel.id_channel,
                channel.avatar_url,
                channel.description,
                channel.subs_total,
                COALESCE(channel.subs_total - yesterday_subs.subs, 0) AS new_subs_today,
                CAST(COALESCE(avg_yesterday.avg_views_per_post, 0) AS int) as avg_views_per_post,
                CAST(ROUND(COALESCE(avg_3_last_days.avg_views_per_post, 0) / channel.subs_total * 100) AS smallint) AS ER
                FROM channel
                    LEFT JOIN (SELECT
                                id_channel,
                                FLOOR(SUM(views) / COUNT(id_post)) as avg_views_per_post
                                FROM post
                                WHERE post.date::date = (current_date - interval '1 day')::date
                                GROUP BY id_channel) AS avg_yesterday
                                ON channel.id_channel = avg_yesterday.id_channel

                    LEFT JOIN (SELECT subs, id_channel FROM sub_per_day
                                WHERE date = date(now()) - interval '1 day') AS yesterday_subs
                                ON channel.id_channel = yesterday_subs.id_channel

                    LEFT JOIN (SELECT
                                id_channel,
                                SUM(views) / COUNT(id_post) as avg_views_per_post
                                FROM post
                                WHERE post.date > now() - interval '3 days'
                                GROUP BY id_channel) AS avg_3_last_days
                                ON channel.id_channel = avg_3_last_days.id_channel
                WHERE LOWER(channel.name) SIMILAR TO '% ({" %|% ".join(name)}) %'
                ORDER BY channel.name
                LIMIT 6 OFFSET {6 * (page - 1)}
                """

        res = await self.db_session.execute(text(query))
        channel_row = res.fetchall()

        if res is not None:

            response_count: int
            response_channel: List[SearchChannelByLinkAndByName] = list()

            query = f"""
                    SELECT
                    count(channel.id_channel)
                    FROM channel
                        LEFT JOIN (SELECT
                                    id_channel,
                                    FLOOR(SUM(views) / COUNT(id_post)) as avg_views_per_post
                                    FROM post
                                    WHERE post.date::date = (current_date - interval '1 day')::date
                                    GROUP BY id_channel) AS avg_yesterday
                                    ON channel.id_channel = avg_yesterday.id_channel

                        LEFT JOIN (SELECT subs, id_channel FROM sub_per_day
                                    WHERE date = date(now()) - interval '1 day') AS yesterday_subs
                                    ON channel.id_channel = yesterday_subs.id_channel

                        LEFT JOIN (SELECT
                                    id_channel,
                                    SUM(views) / COUNT(id_post) as avg_views_per_post
                                    FROM post
                                    WHERE post.date > now() - interval '3 days'
                                    GROUP BY id_channel) AS avg_3_last_days
                                    ON channel.id_channel = avg_3_last_days.id_channel
                    WHERE LOWER(channel.name) SIMILAR TO '% {" %|% ".join(name)}) %'
                    """
            res = await self.db_session.execute(text(query))
            count_row = res.fetchone()
            response_count = count_row[0]

            for channel in channel_row:
                response_channel.append(
                    SearchChannelByLinkAndByName(
                        channel_name=channel[0],
                        channel_id=channel[1],
                        profile_img_url=channel[2],
                        description=channel[3],
                        subscribers=channel[4],
                        new_subscribers_today=channel[5],
                        average_post_views_yesterday=channel[6],
                        er=channel[7],
                    )
                )

            return [response_channel, response_count]

    async def search_by_filters(
            self,
            page: int,
            description: Optional[str] = None,
            subscribers_from: Optional[int] = None,
            subscribers_to: Optional[int] = None,
            post_average_views_from: Optional[int] = None,
            post_average_views_to: Optional[int] = None,
            mentions_by_week_from: Optional[int] = None,
            mentions_by_week_to: Optional[int] = None,
            channel_type: Optional[str] = None,
            category: Optional[str] = None,
            er72h_from: Optional[int] = None,
            er72h_to: Optional[int] = None,
    ):
        description = description.lower().split() if description is not None else None
        query = """
                SELECT
                channel.name,
                channel.id_channel,
                channel.avatar_url,
                channel.description,
                channel.subs_total,
                COALESCE(channel.subs_total - yesterday_subs.subs, 0) AS new_subs_today,
                CAST(COALESCE(avg_yesterday.avg_views_per_post, 0) AS int) as avg_views_per_post,
                CAST(ROUND(COALESCE(avg_3_last_days.avg_views_per_post, 0) / channel.subs_total * 100) AS smallint) AS ER,
                COALESCE(mention_by_week.mention_by_week, 0) AS mention_by_week
                FROM channel
                    LEFT JOIN (SELECT
                                id_channel,
                                FLOOR(SUM(views) / COUNT(id_post)) as avg_views_per_post
                                FROM post
                                WHERE post.date::date = (current_date - interval '1 day')::date
                                GROUP BY id_channel) AS avg_yesterday
                                ON channel.id_channel = avg_yesterday.id_channel
                
                    LEFT JOIN (SELECT subs, id_channel FROM sub_per_day
                                WHERE date = date(now()) - interval '1 day') AS yesterday_subs
                                ON channel.id_channel = yesterday_subs.id_channel
                
                    LEFT JOIN (SELECT
                                id_channel,
                                SUM(views) / COUNT(id_post) as avg_views_per_post
                                FROM post
                                WHERE post.date > now() - interval '3 days'
                                GROUP BY id_channel) AS avg_3_last_days
                                ON channel.id_channel = avg_3_last_days.id_channel
                                
                    LEFT JOIN (SELECT id_mentioned_channel, COUNT(id_channel) AS mention_by_week
                                FROM (SELECT mention.id_mentioned_channel, date, mention.id_channel 
                                        FROM mention
                                            INNER JOIN post USING(id_post)
                                        WHERE mention.id_mentioned_channel <> mention.id_channel 
                                            AND post.date > now() - interval '1 week')	AS unic_ment
                                GROUP BY id_mentioned_channel) AS mention_by_week
                                ON mention_by_week.id_mentioned_channel = channel.id_channel
                """

        filters = [description, subscribers_from, subscribers_to, post_average_views_from, post_average_views_to,
                   mentions_by_week_from, mentions_by_week_to, category, er72h_from, er72h_to]

        keyword_by_filters = {
            "0": f"""LOWER(channel.description) SIMILAR TO '% {" %|% ".join(description) if description is not None else ""} %'""",
            "1": f"""channel.subs_total > {subscribers_from}""",
            "2": f"""channel.subs_total < {subscribers_from}""",
            "3": f"""CAST(COALESCE(avg_yesterday.avg_views_per_post, 0) AS int) > {post_average_views_from}""",
            "4": f"""CAST(COALESCE(avg_yesterday.avg_views_per_post, 0) AS int) < {post_average_views_from}""",
            "5": f"""COALESCE(mention_by_week.mention_by_week, 0) > {mentions_by_week_from}""",
            "6": f"""COALESCE(mention_by_week.mention_by_week, 0) < {mentions_by_week_from}""",
            "7": f"""channel.category LIKE '{category}'""",
            "8": f"""CAST(ROUND(COALESCE(avg_3_last_days.avg_views_per_post, 0) / channel.subs_total * 100) AS smallint) > {er72h_from}""",
            "9": f"""CAST(ROUND(COALESCE(avg_3_last_days.avg_views_per_post, 0) / channel.subs_total * 100) AS smallint) AS ER < {er72h_to}"""
        }


        if len([filter for filter in filters if filter is not None]) > 0:

            query += "WHERE "

            filters_str = list()

            for i, filter in enumerate(filters):
                if filter is not None:
                    filters_str.append(keyword_by_filters[str(i)])

            filters_str = " AND ".join(filters_str)

            query += filters_str

        query += f"""\nORDER BY channel.name 
                      LIMIT 6 OFFSET {6 * (page - 1)}"""

        print(query)

        res = await self.db_session.execute(text(query))
        channel_row = res.fetchall()
        if res is not None:

            response_count: int
            response_channel: List[SearchChannelByLinkAndByName] = list()

            query = f"""
                    SELECT
                    count(channel.id_channel)
                    FROM channel
                        LEFT JOIN (SELECT
                                    id_channel,
                                    FLOOR(SUM(views) / COUNT(id_post)) as avg_views_per_post
                                    FROM post
                                    WHERE post.date::date = (current_date - interval '1 day')::date
                                    GROUP BY id_channel) AS avg_yesterday
                                    ON channel.id_channel = avg_yesterday.id_channel
                    
                        LEFT JOIN (SELECT subs, id_channel FROM sub_per_day
                                    WHERE date = date(now()) - interval '1 day') AS yesterday_subs
                                    ON channel.id_channel = yesterday_subs.id_channel
                    
                        LEFT JOIN (SELECT
                                    id_channel,
                                    SUM(views) / COUNT(id_post) as avg_views_per_post
                                    FROM post
                                    WHERE post.date > now() - interval '3 days'
                                    GROUP BY id_channel) AS avg_3_last_days
                                    ON channel.id_channel = avg_3_last_days.id_channel
                                    
                        LEFT JOIN (SELECT id_mentioned_channel, COUNT(id_channel) AS mention_by_week
                                    FROM (SELECT mention.id_mentioned_channel, date, mention.id_channel 
                                            FROM mention
                                                INNER JOIN post USING(id_post)
                                            WHERE mention.id_mentioned_channel <> mention.id_channel 
                                                AND post.date > now() - interval '1 week') AS unic_ment
                                    GROUP BY id_mentioned_channel) AS mention_by_week
                                    ON mention_by_week.id_mentioned_channel = channel.id_channel
                    """
            if len([filter for filter in filters if filter is not None]) > 0:

                query += "WHERE "

                filters_str = list()

                for i, filter in enumerate(filters):
                    if filter is not None:
                        filters_str.append(keyword_by_filters[f'{i}'])

                filters_str = " AND ".join(filters_str)

                query += filters_str

            res = await self.db_session.execute(text(query))
            count_row = res.fetchone()
            response_count = count_row[0]

            for channel in channel_row:
                response_channel.append(
                    SearchChannelByLinkAndByName(
                        channel_name=channel[0],
                        channel_id=channel[1],
                        profile_img_url=channel[2],
                        description=channel[3],
                        subscribers=channel[4],
                        new_subscribers_today=channel[5],
                        average_post_views_yesterday=channel[6],
                        er=channel[7],
                    )
                )

            return [response_channel, response_count]






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
