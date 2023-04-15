import asyncio
import uvloop
from typing import Optional, List, Union, Dict
from pyrogram import Client
from Database.DAL.ChannelDAL import ChannelDAL
from Database.DAL.PostDAL import PostDAL
from Database.DAL.MentionDAL import MentionDAL
# from Database.DAL.SubPerDayDAL import SubPerDay
from responseModel import ChannelObject, ChannelIds, ChatObject, Mention, Post, UpdateChannel, UpdatePost
from Database.session import get_db2
from fastapi import Depends
import datetime


class UserAgent(object):

    @staticmethod
    async def join_chat(chat_id: int | str):
        try:
            app = Client("sessions/session")
            async with app as app:
                await app.join_chat(chat_id)
                return True

        except Exception as e:
            print(e)

    @staticmethod
    async def leave_chat(chat_id: str | int):
        try:
            app = Client("sessions/session")
            async with app as app:
                await app.leave_chat(chat_id)
                return True

        except Exception as e:
            print(e)

    @staticmethod
    async def get_channels_ids() -> ChannelIds:
        try:
            app = Client("sessions/session")
            async with app as app:
                chat_ids = list()
                async for dialog in app.get_dialogs():
                    if str(dialog.chat.type) == "ChatType.CHANNEL":
                        chat_ids.append(dialog.chat.id)
                return ChannelIds(channel_ids=chat_ids)

        except Exception as e:
            print(e)

    @staticmethod
    async def main_parse_chat(chat_id: int | str) -> ChannelObject:
        try:
            app = Client("sessions/session")
            async with app as app:

                chat = await app.get_chat(chat_id)

                pwd = await app.download_media(
                    message=chat.photo.small_file_id,
                    file_name=f"{chat.id}.jpg"
                ) if chat.photo is not None else None

                output = ChannelObject(
                    id_channel=chat.id,
                    name=chat.title,
                    link=f"https://t.me/{chat.username}" if chat.username is not None else None,
                    avatar_url=pwd,
                    description=chat.description,
                    subs_total=chat.members_count
                )
                print(output)
                return output

        except ValueError or Exception as e:
            print(e)

    @staticmethod
    async def parse_full_chat(chat_id: int, stored_channels: Optional[dict[str, int]] = None) -> ChatObject:
        try:
            app = Client("sessions/session")

            async with app as app:
                posts = []
                mentions = []
                iterate_status = True
                offset_id = 0
                date_183_day_later = datetime.datetime.now() - datetime.timedelta(days=183)

                while iterate_status:
                    async for message in app.get_chat_history(chat_id=chat_id, offset_id=offset_id, limit=100):

                        if (message.date - date_183_day_later).days < 0:
                            iterate_status = False
                            break

                        if stored_channels is not None:
                            for name in stored_channels:

                                text = message.text if message.text is not None else message.caption

                                if f'@{name}' in str(text) or f't.me/{name}' in str(text) or f'{name}' in str(text):

                                    mention = Mention(
                                        id_mentioned_channel=stored_channels[name],
                                        id_post=message.id,
                                        id_channel=chat_id
                                    )
                                    mentions.append(mention)

                        post = Post(
                            id_post=message.id,
                            id_channel=chat_id,
                            date=message.date,
                            text=message.text if message.text is not None else message.caption,
                            views=message.views if message.views is not None else 0,
                            id_channel_forward_from=message.forward_from_chat.id
                            if message.forward_from_chat is not None else None
                        )

                        posts.append(post)

                        if message.id <= 1:
                            iterate_status = False
                            break

                    offset_id = posts[len(posts) - 1].id_post


                i = 1
                while i < len(posts) - 1:
                    if posts[i - 1].date == posts[i].date:
                        del posts[i - 1]
                    i += 1

            return ChatObject(posts=posts, mentions=mentions)

        except ValueError or Exception as e:
            print(e)

    @staticmethod
    async def update_views_for_last_30_days(chat_id: int) -> List[UpdatePost]:
        try:
            app = Client("sessions/session")

            async with app as app:

                posts = []
                iterate_status = True
                offset_id = 0
                date_30_day_later = datetime.datetime.now() - datetime.timedelta(days=30)

                while iterate_status:
                    async for message in app.get_chat_history(chat_id=chat_id, offset_id=offset_id, limit=100):

                        if (message.date - date_30_day_later).days < 0:
                            iterate_status = False
                            break

                        post = UpdatePost(
                            id_post=message.id,
                            id_channel=chat_id,
                            views=message.views if message.views is not None else 0,
                        )

                        posts.append(post)

                        if message.id <= 1:
                            iterate_status = False
                            break

                    offset_id = posts[len(posts) - 1].id_post

                # i = 1
                # while i < len(posts) - 1:
                #     if posts[i - 1].date == posts[i].date:
                #         del posts[i - 1]
                #         print(i)
                #     i += 1

            return posts

        except ValueError or Exception as e:
            print(e)

    @staticmethod
    async def check_subs_per_day(chat_id: int) -> UpdateChannel:
        try:
            app = Client("sessions/session")
            async with app as app:

                chat = await app.get_chat(chat_id)

                output = UpdateChannel(
                    id_channel=chat.id,
                    subs_total=chat.members_count
                )

                return output

        except ValueError or Exception as e:
            print(e)


uvloop.install()
#
c = asyncio.run(UserAgent.get_channels_ids())
# for j in c.channel_ids:
#     print(asyncio.run(UserAgent.check_subs_per_day(j)))

# print(c)
# print(len(c.channel_ids))
# k = list()
# for i in c.channel_ids[:1]:
# k = asyncio.run(UserAgent.parse_full_chat(-1001214137365))
# for i in k.posts:
#     if i.id_channel_forward_from is not None:
#         print(i)

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


async def add_all_channel(channel_ids, session: AsyncSession = Depends(get_db2)):

    for i in channel_ids:

        async with session:

            async with session.begin():

                from_parse = asyncio.run(UserAgent.main_parse_chat(i))

                new_channel = ChannelDAL(session)

                await new_channel.create_channel(
                    id_channel=from_parse.id_channel,
                    name=from_parse.name,
                    link=from_parse.link,
                    avatar_url=from_parse.avatar_url,
                    description=from_parse.description,
                    subs_total=from_parse.subs_total
                )

m = asyncio.run(add_all_channel(c.channel_ids[:1]))


# print("------")
# for i in k:
#     print(i)
# -1001618792964 DNS
# -1001660158742 Так себе шутник
# -1001214137365 Не морген

# c.posts.sort(key=lambda x: x.id_post)
# for i in c.posts:
#     print(i.id_post)
# for post in c.posts:
#     k = PostDAL()
#     PostDAL.create_post(
#             id_post=post.id_post,
#             id_channel=post.id_channel,
#             date=post.date,
#             views=post.views,
#             id_channel_forward_from=post.id_channel_forward_from)
# print(c.posts[0].date)

    # @staticmethod
    # def find_mentions(message, mentions: Optional[List[str]] = list):
    #     result = []
    #     text = message.text if message.text is not None else message.caption
    #     for mention in mentions:
    #         if f'@{mention}' in str(text) or f't.me/{mention}' in str(text) or f'{mention}' in str(text):
    #             result.append(mention)
    #     return len(result)
    # @staticmethod
    # async def parse_full_chat(chat_id: int | str) -> ChatObject:
    # @staticmethod
    # async def get_me() -> GetMeUser:
    #     try:
    #         app = Client("sessions/session")
    #         async with app:
    #             response = await app.get_me()
    #             print(response)
    #             output = GetMeUser(
    #                 id=response.id,
    #                 is_self=response.is_self,
    #                 is_contact=response.is_contact,
    #                 is_mutual_contact=response.is_mutual_contact,
    #                 is_deleted=response.is_deleted,
    #                 is_bot=response.is_bot,
    #                 is_verified=response.is_verified,
    #                 is_restricted=response.is_restricted,
    #                 is_scam=response.is_scam,
    #                 is_fake=response.is_fake,
    #                 is_support=response.is_support,
    #                 is_premium=response.is_premium,
    #                 first_name=response.first_name,
    #                 last_name=response.last_name,
    #                 status=response.status,
    #                 last_online_date=response.last_online_date,
    #                 username=response.username,
    #                 dc_id=response.dc_id,
    #                 phone_number=response.phone_number,
    #                 photo=response.photo
    #             )
    #
    #             log.logger.info(output)
    #             return output
    #
    #     except Exception as e:
    #         log.logger.error(e)
    #         raise UserAgentException(err=e)

    # @staticmethod
    # async def _download_media(file_id: str) -> str:
    #     try:
    #         app = Client("sessions/session")
    #         async with app as app:
    #             pwd = await app.download_media(file_id)
    #             return pwd
    #
    #     except ValueError or Exception as e:
    #         print(e)


    # @staticmethod
    # async def main_parse_chat(chat_id: int | str) -> ChatObject:
    #     try:
    #         app = Client("sessions/session")
    #         async with app as app:
    #
    #             chat = await app.get_chat(chat_id)
    #
    #             pwd = await app.download_media(
    #                 message=chat.photo.small_file_id,
    #                 file_name=f"{chat.id}.jpg"
    #             ) if chat.photo is not None else None
    #
    #             output = ChatObject(
    #                 id_channel=chat.id,
    #                 name=chat.title,
    #                 link=f"https://t.me/{chat.username}",
    #                 avatar_url=pwd,
    #                 description=chat.description,
    #                 subs_total=chat.members_count
    #             )
    #
    #             return output
    #
    #     except ValueError or Exception as e:
    #         print(e)


    #

    #
    # @staticmethod
    # def reaction_count(reactions):
    #     if reactions != None:
    #         count = 0
    #         reactions = list(reactions.reactions)
    #         for reaction in reactions:
    #             count += reaction.count
    #         return count
    #     else:
    #         return 0
    #


    # @staticmethod
    # async def get_message():
    #     app = Client("sessions/session")
    #     async with app as app:
    #         c = await app.get_messages("etp_invest", 2724)



# print(UserAgent.)
# u.get_chat()
# b = asyncio.run(u.get_me())

# asyncio.run(u.join_chat(chat_id="@etp_invest"))
# asyncio.run(u.leave_chat(chat_id="@etp_invest"))
# c = asyncio.run(u.download_media(file_id="AQADAgADAqgxG-9aNRgAEAIAA-9aNRgABHYhe-aCoYWMAAQeBA"))
# c = asyncio.run(u.get_chat(chat_id=-1001169520716))
# chat_ids = asyncio.run(u.get_channels_ids())
# print(chat_ids)
# c = asyncio.run(u.get_chat_history(chat_id="@teststatron", mentions=['@CryptoRichWitch']))
# print(c)
# for id in chat_ids.chat_ids:
#     print(asyncio.run(u.get_chat(chat_id=id)))

# c = asyncio.run(u.get_channels_ids())
# print(len(c))
# print(c.small_photo_unique_id)