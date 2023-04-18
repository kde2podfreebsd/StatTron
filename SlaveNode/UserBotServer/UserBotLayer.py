import asyncio

import uvloop
from UserBot import UserAgent

from Database.DAL.ChannelDAL import ChannelDAL
from Database.session import async_session

# from fastapi import Depends
# from responseModel import ChannelIds
# from responseModel import ChannelObject
# from responseModel import ChatObject
# from responseModel import Mention
# from responseModel import Post
# from responseModel import UpdateChannel
# from responseModel import UpdatePost
# from Database.DAL.MentionDAL import MentionDAL
# from Database.DAL.PostDAL import PostDAL
# from Database.DAL.SubPerDayDAL import SubPerDayDAL
# from Database.Models.ChannelModel import Channel
# from Database.Models.MentionModel import Mention
# from Database.Models.PostModel import Post
# from Database.Models.SubPerDayModel import SubPerDay

# import datetime


async def main():

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


uvloop.install()
asyncio.run(main())
