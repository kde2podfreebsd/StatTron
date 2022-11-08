import os
import logging
import time
import datetime

from pyrogram import Client, filters, enums
from typing import Optional, List
import asyncio


class UserBot:

    def __init__(self, username: str, debug: Optional[bool] = False) -> None:
        self.username = username
        self.app = Client(f"sessions/{username}")
        if debug:
            self.debug = logging.basicConfig(encoding='utf-8',
                                             format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s",
                                             level=logging.DEBUG)
        else:
            self.debug = logging.basicConfig(encoding='utf-8',
                                             format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s",
                                             level=logging.INFO)

    async def get_channels(self):
        try:
            channels = dict()
            async with self.app as app:
                chat_ids = list()
                async for dialog in app.get_dialogs():
                    if str(dialog.chat.type) == "ChatType.CHANNEL":
                        chat_ids.append(dialog.chat.id)
                i = 0
                for id in chat_ids:
                    i += 1
                    chat = await app.get_chat(id)
                    if chat != None:
                        channels[chat.id] = {
                            "id": chat.id,
                            "is_scam": chat.is_scam,
                            "is_private": True if chat.username == None else False,
                            "title": chat.title,
                            "username": chat.username,
                            "members_count": chat.members_count,
                            "description": chat.description,
                            "photo_big_file_id": chat.photo.big_file_id if chat.photo != None else None,
                            "photo_small_file_id": chat.photo.small_file_id if chat.photo != None else None,
                            "small_photo_path": await app.download_media(chat.photo.small_file_id) if chat.photo != None else None,
                        }

                self.channels = channels

                return channels



        except Exception as e:
            return e

    async def download_media(self, file_id):
        try:
            # TODO: сделать удаление старых фото перед скачиванием (small_photo_path)
            async with self.app as app:
                return await app.download_media(file_id)
        except Exception as e:
            return e

    async def join_chat(self, chat_id: str) -> "Result of join":
        try:
            async with self.app as app:
                return await app.join_chat(chat_id)
        except Exception as e:
            return e

    async def leave_chat(self, chat_id) -> "Result of leave":
        try:
            async with self.app as app:
                return await app.leave_chat(chat_id)

        except Exception as e:
            return e

    async def get_chat_members_count(self, chat_id: str) -> "Count of chat members":
        try:
            async with self.app as app:
                count = await app.get_chat_members_count(chat_id)
                return count
        except Exception as e:
            return e

    async def get_chat_history(self, chat_id: str, mentions: Optional[List[str]] = list()) -> "List of chat messages":
        try:
            #TODO: совмещать посты с одинаковой датой публикаций
            messages = dict()
            async with self.app as app:
                offset = 0
                all_views = 0
                all_posts = 0
                global iterate_status
                iterate_status = True
                while iterate_status:
                    async for message in app.get_chat_history(chat_id=chat_id, offset=offset, limit=200):
                        if message.id == 1:
                            iterate_status = False
                            break
                        def reaction_count(reactions):
                            if reactions != None:
                                count = 0
                                reactions = list(reactions.reactions)
                                for reaction in reactions:
                                    count += reaction.count
                                return count
                            else:
                                return 0

                        def find_mentions(mentions):
                            result = []
                            text = message.text if message.text != None else message.caption
                            for mention in mentions:
                                if f'@{mention}' in str(text) or f't.me/{mention}' in str(text):
                                    result.append(mention)
                            if len(result) > 0:
                                return result
                            else:
                                return False

                        all_posts += 1
                        all_views += message.views


                        messages[message.id] = {
                            "id": message.id,
                            "link": message.link,
                            # "text": message.text if message.text != None else message.caption,
                            "date": message.date,
                            "views": message.views,
                            "forward_from_chat": message.forward_from_chat.username \
                                if message.forward_from_chat != None else False,
                            "reactions": reaction_count(message.reactions),
                            # "media": message.media if message.media != None else False,
                            "mentions": find_mentions(mentions)
                        }
                    offset += 200

                avg_views = all_views/all_posts
                members_count = await app.get_chat_members_count(chat_id)
                er = (avg_views / int(members_count)) * 100



                return messages, avg_views, er

        except Exception as e:
            return e

    def loop_methods(self, fn):
        try:
            self.app.run(fn)
        except Exception as e:
            return e


def main():
    ubot = UserBot(username="donqhomo", debug=False)

    loop = asyncio.get_event_loop()
    run = loop.run_until_complete

    # res0 = run(ubot.download_media(file_id="AQADAgADxbAxGyB2GUoAEAMAA7R3peUW____9UWLTY68ItIABB4E"))

    # res1 = run(ubot.get_chat_members_count(chat_id="@CryptoVedma"))
    # res2 = run(ubot.get_channels())

    res3 , avg_views, er = run(ubot.get_chat_history(chat_id="@CryptoVedma", mentions=['donqhomo']))

    # print(f"Res1: {res1}")
    # print(f"Res2: {res2}")

    for res in res3:
        print(res3[res], '\n\n\n')

    print(avg_views)
    print(er)


main()
