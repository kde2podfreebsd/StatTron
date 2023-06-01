import asyncio
import datetime

import uvloop
from UserBot import UserAgent

from Database.session import async_session
from Database.DAL.ChannelDAL import ChannelDAL
from Database.DAL.MentionDAL import MentionDAL
from Database.DAL.PostDAL import PostDAL
from Database.DAL.SubPerDayDAL import SubPerDayDAL


async def grabber(client, go_to_daily_checker: bool = True):


    while True:

        if not go_to_daily_checker:
            break

        channelsId = await client.get_channels_ids()

        for channel_id in channelsId.channel_ids:
            print("channel:" + str(channel_id))
            date_now = datetime.datetime.now()
            if date_now.hour == 15 and date_now.minute == 21:
                go_to_daily_checker = False
                break

            response = await client.main_parse_chat(channel_id)
            async with async_session() as session:
                async with session.begin():
                        channel = ChannelDAL(session)
                        await channel._create_channel(
                            id_channel=response.id_channel,
                            name=response.name,
                            link=response.link,
                            avatar_url=response.avatar_url,
                            description=response.description,
                            subs_total=response.subs_total,
                        )


        for channel_id in channelsId.channel_ids:
            print(channelsId.channel_ids)
            print("chat:" + str(channel_id))
            date_now = datetime.datetime.now()
            if date_now.hour == 15 and date_now.minute == 21:
                go_to_daily_checker = False
                break

            async with async_session() as session:
                async with session.begin():

                    channels = ChannelDAL(session)
                    posts = PostDAL(session)
                    mentions = MentionDAL(session)

                    stored_channels = await channels._select_all_channels()
                    stored_channels_usernames = list(
                        x.link.split('/')[-1] if x.link is not None else None for x in stored_channels
                    )
                    stored_channels_ids = list(x.id_channel for x in stored_channels)
                    stored_channels = dict(zip(stored_channels_usernames, stored_channels_ids))
                    response = await client.parse_chat(channel_id, stored_channels, 180)

                    for post in response.posts:
                        await posts.create_post(
                            id_post=post.id_post,
                            id_channel=post.id_channel,
                            date=post.date,
                            text=post.text,
                            views=post.views,
                            id_channel_forward_from=post.id_channel_forward_from
                        )

                    for mention in response.mentions:
                        await mentions.create_mention(
                            id_mentioned_channel=mention.id_mentioned_channel,
                            id_post=mention.id_post,
                            id_channel=mention.id_channel
                        )


async def daily_checker(client):

    channelsId = await client.get_channels_ids()
    for channel_id in channelsId.channel_ids:
        async with async_session() as session:
            async with session.begin():
                print("daily:" + str(channel_id))
                response = await client.check_subs_per_day(channel_id)

                sub_per_day = SubPerDayDAL(session)
                await sub_per_day.create_sub_per_day(
                    id_channel=response.id_channel,
                    subs=response.subs_total,
                    date=datetime.date.today()
                )
    await asyncio.sleep(60)


async def main():
#    await UserAgent.main()
    client = UserAgent()
    while True:
        await grabber(client)
        await daily_checker(client)


uvloop.install()
asyncio.run(main())


# async def mmm():
#     async with async_session() as session:
#         async with session.begin():
#             channels = ChannelDAL(session)
#             c = await channels.search_channel_by_link("t.me/ASGasparyan")
#             for i in c:
#                 print(i)
#
# asyncio.run(mmm())
