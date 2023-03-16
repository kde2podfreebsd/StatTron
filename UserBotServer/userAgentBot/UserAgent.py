import asyncio
import uvloop
from typing import Optional, List, Union
from pyrogram import Client
from UserBotServer.logger import Logger
from UserBotServer.exceptions import UserAgentException
from UserBotServer.responseModels import GetMeUser, DownloadFilePWD, ChannelIds, \
    ChatObject, MessageChatObject, MessageEntity

log = Logger()


class UserAgent(object):
    __instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UserAgent, cls).__new__(cls)
        return cls.instance

    @staticmethod
    async def get_me() -> GetMeUser:
        try:
            app = Client("sessions/session")
            async with app:
                response = await app.get_me()
                output = GetMeUser(
                    id=response.id,
                    is_self=response.is_self,
                    is_contact=response.is_contact,
                    is_mutual_contact=response.is_mutual_contact,
                    is_deleted=response.is_deleted,
                    is_bot=response.is_bot,
                    is_verified=response.is_verified,
                    is_restricted=response.is_restricted,
                    is_scam=response.is_scam,
                    is_fake=response.is_fake,
                    is_support=response.is_support,
                    is_premium=response.is_premium,
                    first_name=response.first_name,
                    last_name=response.last_name,
                    status=response.status,
                    last_online_date=response.last_online_date,
                    username=response.username,
                    dc_id=response.dc_id,
                    phone_number=response.phone_number,
                    photo=response.photo
                )

                log.logger.info(output)
                return output

        except Exception as e:
            log.logger.error(e)
            raise UserAgentException(err=e)

    @staticmethod
    async def download_media(file_id: str) -> DownloadFilePWD:
        try:
            app = Client("sessions/session")
            async with app as app:
                pwd = await app.download_media(file_id)
                log.logger.info(DownloadFilePWD(pwd=pwd))
                return DownloadFilePWD(pwd=pwd)

        except ValueError or Exception as e:
            log.logger.error(e)
            raise UserAgentException(err=e)

    @staticmethod
    async def get_channels_ids() -> ChannelIds:
        try:
            app = Client("sessions/session")
            async with app as app:
                chat_ids = list()
                async for dialog in app.get_dialogs():
                    if str(dialog.chat.type) == "ChatType.CHANNEL":
                        chat_ids.append(dialog.chat.id)
                return ChannelIds(chat_ids=chat_ids)

        except Exception as e:
            log.logger.error(e)
            raise UserAgentException(err=e)

    @staticmethod
    async def get_chat(chat_id: int | str) -> ChatObject:
        try:
            app = Client("sessions/session")
            async with app as app:
                chat = await app.get_chat(chat_id)
                output = ChatObject(
                    id=chat.id,
                    dc_id=chat.dc_id,
                    type=chat.type,
                    is_verified=chat.is_verified,
                    is_restricted=chat.is_restricted,
                    is_creator=chat.is_creator,
                    is_scam=chat.is_scam,
                    is_fake=chat.is_fake,
                    has_protected_content=chat.has_protected_content,
                    title=chat.title,
                    username=chat.username,
                    description=chat.description,
                    photo=chat.photo,
                    small_file_id=chat.photo.small_file_id if chat.photo is not None else None,
                    members_count=chat.members_count
                )

                log.logger.info(output)
                return output

        except ValueError or Exception as e:
            log.logger.error(e)
            raise UserAgentException(err=e)

    @staticmethod
    async def join_chat(chat_id: int | str):
        try:
            app = Client("sessions/session")
            async with app as app:
                chat = await app.join_chat(chat_id)
                output = ChatObject(
                    id=chat.id,
                    type=chat.type,
                    is_verified=chat.is_verified,
                    is_restricted=chat.is_restricted,
                    is_creator=chat.is_creator,
                    is_scam=chat.is_scam,
                    is_fake=chat.is_fake,
                    has_protected_content=chat.has_protected_content,
                    title=chat.title,
                    username=chat.username,
                    description=chat.description,
                    photo=chat.photo,
                    small_file_id=chat.photo.small_file_id if chat.photo is not None else None,
                    members_count=chat.members_count
                )

                log.logger.info(output)
                return output

        except Exception as e:
            log.logger.error(e)
            raise UserAgentException(err=e)

    @staticmethod
    async def leave_chat(chat_id: str | int):
        try:
            app = Client("sessions/session")
            async with app as app:
                updates = await app.leave_chat(chat_id)
                chat = updates.chats[0]
                output = ChatObject(
                    id=chat.id,
                    is_verified=chat.verified,
                    is_restricted=chat.restricted,
                    is_creator=chat.creator,
                    is_scam=chat.scam,
                    is_fake=chat.fake,
                    title=chat.title,
                    username=chat.username,
                    photo=chat.photo,
                    small_file_id=chat.photo.photo_id if chat.photo is not None else None
                )

                log.logger.info(output)
                return output

        except Exception as e:
            log.logger.error(e)
            raise UserAgentException(err=e)

    @staticmethod
    def reaction_count(reactions):
        if reactions != None:
            count = 0
            reactions = list(reactions.reactions)
            for reaction in reactions:
                count += reaction.count
            return count
        else:
            return 0

    @staticmethod
    def find_mentions(message, mentions: Optional[List[str]] = list):
        result = []
        text = message.text if message.text is not None else message.caption
        for mention in mentions:
            if f'@{mention}' in str(text) or f't.me/{mention}' in str(text) or f'{mention}' in str(text):
                result.append(mention)
        return len(result)

    async def get_chat_history(self, chat_id: int | str, mentions: Optional[List[str]] = list) -> List[MessageEntity]:
        app = Client("sessions/session")

        messages_of_chat = []
        message_entities = []

        async with app as app:

            iterate_status = True
            offset = 0
            all_views = 0
            all_posts = 0
            mention_count = 0

            while iterate_status:
                async for message in app.get_chat_history(chat_id=chat_id, offset=offset, limit=200):
                    if message.id <= 1:
                        iterate_status = False
                        break

                    all_posts += 1
                    all_views += message.views if message.views is not None else 0

                    mention_result = self.find_mentions(message=message, mentions=mentions)
                    mention_count += mention_result

                    msg = MessageChatObject(
                        chat_id=message.chat.id,
                        username=message.chat.username,
                        mention_result=mention_result,
                        reactions_count=self.reaction_count(reactions=message.reactions),
                        date_of_message=message.date,
                        forwards_count=message.forwards,
                        forward_from_chat=message.forward_from_chat,
                        text_or_caption=message.text if message.text is not None else message.caption,
                        sender_chat=message.sender_chat,
                        message_id= message.id
                    )

                    messages_of_chat.append(msg)


            for msg in messages_of_chat:
                e = MessageEntity(date_of_message=msg.date_of_message, message=[msg])
                message_entities.append(e)
            i = 0
            while i < len(message_entities):
                if message_entities[i-1].date_of_message == message_entities[i].date_of_message:
                    message_entities[i - 1].message.append(message_entities[i])
                    message_entities.pop(i)
                i += 1

        return message_entities








u = UserAgent()
uvloop.install()
# asyncio.run(u.join_chat(chat_id=-1001733300868))
# asyncio.run(u.leave_chat(chat_id=-1001733300868))
# b = asyncio.run(u.get_me())
# c = asyncio.run(u.download_media(file_id="AgACAgIAAx0EdAMSLAADC2QTd2SxArbeJFKbfD-Z3aEU1E9oAAKvxDEbFH-JSPFIPygmIIEHAAgBAAMCAAN5AAceBA"))
# c = asyncio.run(u.get_chat(chat_id="testuseragentbotASASD"))
# chat_ids = asyncio.run(u.get_channels_ids())
c = asyncio.run(u.get_chat_history(chat_id=-1001946358316, mentions=['@CryptoRichWitch']))
# for id in chat_ids.chat_ids:
#     print(asyncio.run(u.get_chat(chat_id=id)))

# c = asyncio.run(u.get_channels_ids())
# print(len(c))
# print(c.small_photo_unique_id)
