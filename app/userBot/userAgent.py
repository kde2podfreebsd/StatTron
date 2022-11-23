import sys
import os

import logging
from dotenv import load_dotenv
from typing import Optional

import asyncio
from pyrogram import Client

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from db import conn
from config import app

from models.Accounts import Account
from models.Channels import Channel
from models.Messages import Message

config = load_dotenv()


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

                    if ch is not None and hasattr(chat.photo, 'small_file_id') and ch.photo_small_file_id == chat.photo.small_file_id:
                        photo_path = ch.photo_small_file_id
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
                        category="123",
                        photo_big_file_id=channels[chat.id]['photo_big_file_id'],
                        photo_small_file_id=channels[chat.id]['photo_small_file_id'],
                        small_photo_path=channels[chat.id]['small_photo_path'],
                        average_views=123,
                        er_all=456
                    )
                    logging.info(output)

        return channels

    async def join_chat(self, chat_id: str | int, category: str) -> "Result of join":
        async with self.app as app:
            res = await app.join_chat(chat_id)
            channels = dict()
            chat = await app.get_chat(res.id)
            if chat != None:
                return {
                    "id": chat.id,
                    "is_scam": chat.is_scam,
                    "is_private": True if chat.username is None else False,
                    "title": chat.title,
                    "username": chat.username,
                    "members_count": chat.members_count,
                    "description": chat.description,
                    "category": category,
                    "photo_big_file_id": chat.photo.big_file_id if chat.photo is not None else None,
                    "photo_small_file_id": chat.photo.small_file_id if chat.photo is not None else None,
                    "small_photo_path": await app.download_media(
                        chat.photo.small_file_id) if chat.photo is not None else None,
                }
            else:
                return False

    def loop_methods(self, fn):
        try:
            self.app.run(fn)
        except Exception as e:
            return e


if __name__ == "__main__":
    with app.app_context():
        loop = asyncio.get_event_loop()
        run = loop.run_until_complete
        app.config.from_pyfile("config.py")
        conn.init_app(app)

        accounts = Account.query.filter(Account.username is not None).all()

        for account in accounts:
            ubot = UserBot(username=account.username, debug=False)
            try:
                output = run(ubot.get_channels())
            except AttributeError:
                logging.warning(f'\n\n!!!session for account {account.username} doesnt inited!!!\n\n')
                continue

            print(account.channels)

