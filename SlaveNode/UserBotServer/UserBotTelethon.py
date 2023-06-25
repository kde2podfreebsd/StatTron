# import asyncio
import datetime
from typing import Optional

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerChannel
from responseModel import ChannelIds
from responseModel import ChannelObject
from responseModel import ChatObject
from responseModel import Mention
from responseModel import Post
from responseModel import UpdateChannel

# from typing import List

# from responseModel import UpdatePost

# # import uvloop

# # from typing import Dict
# # from typing import Union


class UserAgent(object):
    def __init__(self):
        self.app = TelegramClient("sessions/session5",
                                  api_id=23677472,
                                  api_hash="6945657dfb3f7d10558065c24bd8d904")
    @staticmethod
    async def main():
        async with TelegramClient(
            "sessions/session5",
            api_id=23677472,
            api_hash="6945657dfb3f7d10558065c24bd8d904",
        ) as app:
            await app.send_message("me", "Greetings from **Telethon**!")

    async def join_chat(self, chat_id: int | str):
        try:
            async with self.app as app:
                await app.join_chat(chat_id)
                return True

        except Exception as e:
            print(e)

    async def leave_chat(self, chat_id: str | int):
        try:
            async with self.app as app:
                await app.leave_chat(chat_id)
                return True

        except Exception as e:
            print(e)
    async def get_channels_ids(self) -> ChannelIds:
        try:
            async with self.app as app:
                chat_ids = list()
                for dialog in await app.get_dialogs():
                    if dialog.is_channel:
                        chat_ids.append(dialog.entity.id)
                return ChannelIds(channel_ids=chat_ids)

        except Exception as e:
            print(e)

    async def main_parse_chat(self, chat_id: int | str) -> ChannelObject:
        try:
            async with self.app as app:

                chat = await app(GetFullChannelRequest(chat_id))
                pwd = await app.download_profile_photo(
                    chat_id,
                    file=f"/home/fake_svoevolin/Desktop/StatTron/SlaveNode/UserBotServer/downloads/{chat_id}.png",
                    download_big=False
                )

                output = ChannelObject(
                    id_channel=chat_id,
                    name=chat.chats[0].title,
                    link=f"https://t.me/{chat.chats[0].username}"
                    if chat.chats[0].username is not None
                    else None,
                    avatar_url=pwd,
                    description=chat.full_chat.about,
                    subs_total=(await app.get_participants(chat_id, limit=0)).total
                )
                return output

        except ValueError or Exception as e:
            print(e)

    async def parse_chat(
        self,
        chat_id: int,
        stored_channels: Optional[dict[str, int]] = None,
        days_for_date_offset: int = 183,
    ) -> ChatObject:
        try:
            async with self.app as app:
                posts = []
                mentions = []
                date_offset = datetime.datetime.now() - datetime.timedelta(days=days_for_date_offset)

                channel = await app.get_input_entity(chat_id)

                async for message in app.iter_messages(entity=channel):

                    if message.views == 0:
                        continue

                    if (message.date.replace(tzinfo=None) - date_offset).days < 0:
                        break

                    if stored_channels is not None:
                        for name in stored_channels:

                            text = message.message

                            if (
                                f"{name} " in str(text)
                                and (name is not None)
                            ):
                                mention = Mention(
                                    id_mentioned_channel=stored_channels[name],
                                    id_post=message.id,
                                    id_channel=chat_id,
                                )
                                mentions.append(mention)
                    from_id = None

                    if message.fwd_from is not None:
                        try:
                            from_id = message.fwd_from.from_id.channel_id
                        except:
                            from_id = None

                    post = Post(
                        id_post=message.id,
                        id_channel=chat_id,
                        date=message.date.replace(tzinfo=None),
                        text=message.message if message.message != "" else None,
                        views=message.views if message.views is not None else 0,
                        id_channel_forward_from=from_id,
                        media_group_id=message.grouped_id
                        if message.grouped_id is not None
                        else None,
                    )

                    posts.append(post)

                mediaGroups = list()
                i = 1
                while i < len(posts):

                    mediaGroup = list()
                    if (
                            posts[i - 1].media_group_id is not None
                            and posts[i - 1].media_group_id == posts[i].media_group_id
                    ):

                        while (
                                i < len(posts)
                                and posts[i - 1].media_group_id == posts[i].media_group_id
                        ):
                            mediaGroup.append(posts[i - 1])
                            i += 1

                        mediaGroup.append(posts[i - 1])

                    if len(mediaGroup) != 0:
                        mediaGroups.append(mediaGroup)

                    i += 1
                print(i)

                for mediaGroup in mediaGroups:
                    for msg in mediaGroup:
                        if msg.text is None:
                            posts.remove(msg)

            return ChatObject(posts=posts, mentions=mentions)

        except ValueError or Exception as e:
            print(e)

    async def check_subs_per_day(self, chat_id: int) -> UpdateChannel:
        try:
            async with self.app as app:
                output = UpdateChannel(
                    id_channel=chat_id, subs_total=(await app.get_participants(chat_id, limit=0)).total
                )
                return output

        except ValueError or Exception as e:
            print(e)
