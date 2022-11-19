import asyncio
import logging
from typing import Optional

from dotenv import load_dotenv
from pyrogram import Client

config = load_dotenv()


class UserBot:

    def __init__(self, username: str, debug: Optional[bool] = False) -> None:
        self.username = username
        self.app = Client(f"sessions/{username}")
        if debug:
            logging.basicConfig(encoding='utf-8', format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s", level=logging.DEBUG)
        else:
            logging.basicConfig(encoding='utf-8', format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s", level=logging.INFO)

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
                        "small_photo_path": await app.download_media(
                            chat.photo.small_file_id) if chat.photo is not None else None,
                    }

        return channels


ubot = UserBot(username="donqhomo", debug=False)
loop = asyncio.get_event_loop()
run = loop.run_until_complete

channels = run(ubot.get_channels())

for key in channels:
    print(channels[key]['title'])
