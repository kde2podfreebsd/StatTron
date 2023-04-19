import asyncio

import uvloop
from UserBot import UserAgent

from Database.DAL.ChannelDAL import ChannelDAL
from Database.DAL.MentionDAL import MentionDAL
from Database.DAL.PostDAL import PostDAL
from Database.session import async_session

# from Database.DAL.SubPerDayDAL import SubPerDayDAL

# import datetime


async def main():
    # await UserAgent.main()

    while True:

        channelsId = await UserAgent.get_channels_ids()

        for channel_id in channelsId.channel_ids:
            response = await UserAgent.main_parse_chat(channel_id)
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

            async with async_session() as session:
                async with session.begin():

                    channels = ChannelDAL(session)
                    posts = PostDAL(session)
                    mentions = MentionDAL(session)

                    stored_channels = await channels.select_all_channels()
                    stored_channels_usernames = list(
                        x.link.split("/")[-1] if x.link is not None else None
                        for x in stored_channels
                    )
                    stored_channels_ids = list(x.id_channel for x in stored_channels)
                    stored_channels = dict(
                        zip(stored_channels_usernames, stored_channels_ids)
                    )
                    response = await UserAgent.parse_chat(
                        channel_id, stored_channels, 40
                    )

                    for i in response.mentions:
                        print(i)

                    for post in response.posts:
                        await posts.create_post(
                            id_post=post.id_post,
                            id_channel=post.id_channel,
                            date=post.date,
                            text=post.text,
                            views=post.views,
                            id_channel_forward_from=post.id_channel_forward_from,
                        )

                    for mention in response.mentions:
                        await mentions.create_mention(
                            id_mentioned_channel=mention.id_mentioned_channel,
                            id_post=mention.id_post,
                            id_channel=mention.id_channel,
                        )


uvloop.install()
asyncio.run(main())
