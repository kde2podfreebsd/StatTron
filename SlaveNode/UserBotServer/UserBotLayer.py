import asyncio
import datetime

import uvloop
from UserBotTelethon import UserAgent

from Database.DAL.ChannelDAL import ChannelDAL
from Database.DAL.MentionDAL import MentionDAL
from Database.DAL.PostDAL import PostDAL
from Database.DAL.SubPerDayDAL import SubPerDayDAL
from Database.session import async_session
from Utils import extractUsernameToIdDict, gotoDailyBackup


async def grabber(client):
    while True:

        if gotoDailyBackup():
            break

        channelsId = await client.get_channels_ids()
        print(channelsId.channel_ids)


        for channel_id in channelsId.channel_ids:

            print("channel:" + str(channel_id))

            if gotoDailyBackup():
                break

            response = await client.main_parse_chat(channel_id)

            async with async_session() as session:
                async with session.begin():
                    channel = ChannelDAL(session)

                    await channel.create_channel(
                        id_channel=response.id_channel,
                        name=response.name,
                        link=response.link,
                        avatar_url=response.avatar_url,
                        description=response.description,
                        subs_total=response.subs_total,
                    )

        for channel_id in channelsId.channel_ids:

            print("chat:" + str(channel_id))

            if gotoDailyBackup():
                break

            async with async_session() as session:
                async with session.begin():
                    channels = ChannelDAL(session)
                    stored_channels = extractUsernameToIdDict(await channels.select_all_channels())

            response = await client.parse_chat(chat_id=channel_id,
                                               stored_channels=stored_channels,
                                               days_for_date_offset=360)

            async with async_session() as session:
                async with session.begin():

                    posts = PostDAL(session)
                    mentions = MentionDAL(session)

                    for post in response.posts:
                        await posts.create_post(id_post=post.id_post,
                                                id_channel=post.id_channel,
                                                date=post.date,
                                                text=post.text,
                                                views=post.views,
                                                id_channel_forward_from=post.id_channel_forward_from)

                    for mention in response.mentions:
                        await mentions.create_mention(id_mentioned_channel=mention.id_mentioned_channel,
                                                      id_post=mention.id_post,
                                                      id_channel=mention.id_channel)


async def daily_checker(client):

    channelsId = await client.get_channels_ids()
    for channel_id in channelsId.channel_ids:

        response = await client.check_subs_per_day(channel_id)

        async with async_session() as session:
            async with session.begin():
                print("daily:" + str(channel_id))

                sub_per_day = SubPerDayDAL(session)

                await sub_per_day.create_sub_per_day(
                    id_channel=response.id_channel,
                    subs=response.subs_total,
                    date=datetime.date.today() - datetime.timedelta(days=1),
                )

    await asyncio.sleep(600)


async def main():
    client = UserAgent()
    while True:
        await grabber(client)
        await daily_checker(client)


uvloop.install()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
