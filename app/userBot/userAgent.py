import sys
import os
import time
from time import sleep

import logging
from dotenv import load_dotenv
from typing import Optional, List

import asyncio
from pyrogram import Client

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from db import conn
from config import app

from models.Accounts import Account
from models.Channels import Channel
from models.Messages import Message

config = load_dotenv()

loop = asyncio.get_event_loop()
run = loop.run_until_complete


class UserBot:

    def __init__(self, username: str, debug: Optional[bool] = False) -> None:
        self.username = username
        self.app = Client(f"sessions/{username}")
        if debug:
            logging.basicConfig(encoding='utf-8', format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s",
                                level=logging.DEBUG)
        else:
            logging.basicConfig(encoding='utf-8', format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s",
                                level=logging.INFO)

    async def download_media(self, file_id):
        try:
            async with self.app as app:
                return await app.download_media(file_id)
        except Exception as e:
            return e

    async def get_channels(self):
        channels = dict()
        async with self.app as app:
            chat_ids = list()
            async for dialog in app.get_dialogs():
                if str(dialog.chat.type) == "ChatType.CHANNEL":
                    chat_ids.append(dialog.chat.id)
            for id in chat_ids:
                chat = await app.get_chat(id)
                if chat is not None:

                    ch = Channel.query.filter_by(channel_id=chat.id).first()

                    if ch is not None and hasattr(chat.photo,
                                                  'small_file_id') and ch.photo_small_file_id == chat.photo.small_file_id:
                        photo_path = ch.small_photo_path
                    else:
                        if hasattr(chat.photo, 'small_file_id'):
                            try:
                                if ch is not None and ch.small_photo_path is not None:
                                    os.system(f'rm {ch.small_photo_path}')
                            except Exception:
                                pass
                            photo_path = await app.download_media(chat.photo.small_file_id)
                        else:
                            photo_path = None

                    channels[chat.id] = {
                        "id": chat.id,
                        "is_scam": chat.is_scam,
                        "is_private": True if chat.username is None else False,
                        "title": chat.title,
                        "username": chat.username,
                        "members_count": chat.members_count,
                        "description": chat.description,
                        "photo_big_file_id": chat.photo.big_file_id if chat.photo is not None else None,
                        "photo_small_file_id": chat.photo.small_file_id if chat.photo is not None else None,
                        "small_photo_path": photo_path,
                    }

                    channel = Channel()
                    output = channel.create_channel(
                        account=Account.query.filter_by(username=self.username).first(),
                        channel_id=channels[chat.id]['id'],
                        is_scam=channels[chat.id]['is_scam'],
                        is_private=channels[chat.id]['is_private'],
                        title=channels[chat.id]['title'],
                        username=channels[chat.id]['username'],
                        members_count=channels[chat.id]['members_count'],
                        description=channels[chat.id]['description'],
                        photo_big_file_id=channels[chat.id]['photo_big_file_id'],
                        photo_small_file_id=channels[chat.id]['photo_small_file_id'],
                        small_photo_path=channels[chat.id]['small_photo_path']
                    )
                    logging.info(output)

        return channels

    async def get_chat_history(self, chat_id: str | int, acc, channel, mentions: Optional[List[str]] = list()):
        # TODO: совмещать посты с одинаковой датой публикаций
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
                    all_views += message.views if message.views is not None else 0

                    messages[message.id] = {
                        "id": message.id,
                        "link": message.link,
                        "text": message.text if message.text is not None else message.caption,
                        "date": message.date,
                        "views": message.views,
                        "forward_from_chat": message.forward_from_chat.username if message.forward_from_chat is not None else False,
                        "reactions": reaction_count(message.reactions),
                        "media": message.media if message.media is not None else False,
                        "mentions": find_mentions(mentions)
                    }

                    msg = Message()
                    res = msg.create_message(
                        account=acc,
                        channel=channel,
                        message_id=messages[message.id]["id"],
                        link=messages[message.id]["link"],
                        text=messages[message.id]["text"],
                        date=messages[message.id]["date"],
                        views=messages[message.id]["views"],
                        forward_from_chat=messages[message.id]["forward_from_chat"],
                        reaction=messages[message.id]["reactions"],
                        media=messages[message.id]["media"],
                        mentions=messages[message.id]["mentions"]
                    )

                    logging.info(res)
                    logging.info("sleep 0.2")
                    time.sleep(0.2)

                offset += 200

            avg_views_all_time = all_views / all_posts
            er_all_time = (avg_views_all_time / int(channel.members_count)) * 100

            channel.average_views = avg_views_all_time
            channel.er_all = er_all_time

            output = channel.update(channel=channel)
            logging.info(output)

    async def join_chat(self, chat_id: str | int) -> "Result of join":
        try:
            async with self.app as app:
                res = await app.join_chat(chat_id)
                channels = dict()
                chat = await app.get_chat(res.id)
                if chat is not None:
                    ch = Channel.query.filter_by(channel_id=chat.id).first()

                    if ch is not None and hasattr(chat.photo,
                                                  'small_file_id') and ch.photo_small_file_id == chat.photo.small_file_id:
                        photo_path = ch.small_photo_path
                    else:
                        if hasattr(chat.photo, 'small_file_id'):
                            try:
                                if ch is not None and ch.small_photo_path is not None:
                                    os.system(f'rm {ch.small_photo_path}')
                            except Exception:
                                pass
                            photo_path = await app.download_media(chat.photo.small_file_id)
                        else:
                            photo_path = None

                    channels[chat.id] = {
                        "id": chat.id,
                        "is_scam": chat.is_scam,
                        "is_private": True if chat.username is None else False,
                        "title": chat.title,
                        "username": chat.username,
                        "members_count": chat.members_count,
                        "description": chat.description,
                        "photo_big_file_id": chat.photo.big_file_id if chat.photo is not None else None,
                        "photo_small_file_id": chat.photo.small_file_id if chat.photo is not None else None,
                        "small_photo_path": photo_path,
                    }

                    channel = Channel()
                    output = channel.create_channel(
                        account=Account.query.filter_by(username=self.username).first(),
                        channel_id=channels[chat.id]['id'],
                        is_scam=channels[chat.id]['is_scam'],
                        is_private=channels[chat.id]['is_private'],
                        title=channels[chat.id]['title'],
                        username=channels[chat.id]['username'],
                        members_count=channels[chat.id]['members_count'],
                        description=channels[chat.id]['description'],
                        photo_big_file_id=channels[chat.id]['photo_big_file_id'],
                        photo_small_file_id=channels[chat.id]['photo_small_file_id'],
                        small_photo_path=channels[chat.id]['small_photo_path']
                    )
                    print(f'\n\n\n\nOUTPUT {output}\n\n\n\n')
                    logging.info(output)

                return res
        except Exception as e:
            return e

    async def leave_chat(self, chat_id: str | int):
        # try:
        async with self.app as app:
            chat = await app.leave_chat(chat_id)
            print(chat)
            ch = Channel.query.filter_by(channel_id=chat_id).first()
            output = ch.delete()
            return True

    # except Exception as e:
    #     return e

    def loop_methods(self, fn):
        try:
            self.app.run(fn)
        except Exception as e:
            return e


if __name__ == "__main__":
    with app.app_context():
        app.config.from_pyfile("config.py")
        conn.init_app(app)

        if len(sys.argv) < 2:

            accounts = Account.query.filter(Account.username is not None).all()

            for account in accounts:
                ubot = UserBot(username=account.username, debug=False)
                try:
                    output = run(ubot.get_channels())
                except AttributeError:
                    logging.warning(f'\n\n!!!session for account {account.username} doesnt inited!!!\n\n')
                    continue

                print(account.channels)

                for channel in account.channels:
                    run(ubot.get_chat_history(chat_id=channel.channel_id, acc=account, channel=channel))
                    logging.info("Sleep 5 sec")
                    time.sleep(5)
        else:
            print(sys.argv[1], sys.argv[2], sys.argv[3])
            ubot = UserBot(username=sys.argv[2], debug=False)
            match sys.argv[1]:
                case 'join':
                    output = run(ubot.join_chat(chat_id=sys.argv[3]))
                case 'left':
                    output = run(ubot.leave_chat(chat_id=sys.argv[3]))
