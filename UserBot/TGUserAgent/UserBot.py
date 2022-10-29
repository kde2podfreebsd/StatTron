import logging
from pyrogram import Client, filters, enums
from typing import Optional

class UserBot:

    channels_list = list()

    def __init__(self, username: str, debug: Optional[bool] = False) -> None:
        self.username = username
        self.app = Client(f"sessions/{username}")
        if debug:
            self.debug = logging.basicConfig(encoding='utf-8', format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s",level=logging.DEBUG)
        else:
            self.debug = logging.basicConfig(encoding='utf-8', format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s",level=logging.INFO)

    async def get_channels(self) -> channels_list:
        try:
            self.channels_list = []
            async with self.app as app:
                async for dialog in app.get_dialogs():
                    if str(dialog.chat.type) == "ChatType.CHANNEL":
                        self.channels_list.append(dialog.chat.username)
                        print(dialog.chat)
            if len(self.channels_list) == 0:
                return None
            else:
                output = {"channels": self.channels_list, "username": self.username}
                print(output)
                logging.INFO(output)
                return output

        except Exception as e:
            return e

    async def join_chat(self, chat_id: str) -> "Result of join":
        try:
            async with self.app as app:
                res = await app.join_chat(chat_id)
            logging.INFO()
            output = {"chatUsername": res.username, "id": res.id, "accountUsername": self.username}
            return output

        except Exception as e:
            return e

    async def leave_chat(self, chat_id)-> "Result of leave":
        try:
            async with self.app as app:
                res = await app.leave_chat(chat_id)
            logging.INFO()
            return f"Leave chat: {chat_id}"
        except Exception as e:
            return e

    async def get_chat_members_count(self, chat_id: str) -> "Count of chat members":
        try:
            async with self.app as app:
                count = await app.get_chat_members_count(chat_id)
                print(count)
            logging.INFO()
            return count
        except Exception as e:
            return e

    async def get_chat_members(self, chat_id: str) -> "Dict: 3 type members":
        try:
            async with self.app as app:
                members = []
                async for member in app.get_chat_members(chat_id):
                    print(member)
                    members.append(member)

                administrators = []
                async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                    administrators.append(m)

                bots = []
                async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BOTS):
                    bots.append(m)

            print({"members": members, "administrators": administrators, "bots": bots})
            logging.INFO()

            return {"members": members, "administrators": administrators, "bots": bots}

        except Exception as e:
            return e

    async def get_chat_history(self, chat_id: str) -> "List of chat messages":
        try:
            messages = list()
            async with self.app as app:
                async for message in app.get_chat_history(chat_id):
                    messages.append(message)

            print(messages)
            logging.INFO()
            return messages

        except Exception as e:
            return e

    def loop_methods(self, fn):
        try:
            self.app.run(fn)
            logging.INFO()
        except Exception as e:
            return e

ubot = UserBot(username="donqhomo", debug=False)
# ubot.loop_methods(ubot.get_chat_members_count(chat_id="@rozetked"))
# ubot.loop_methods(ubot.get_chat_history(chat_id="@CryptoVedma"))
# ubot.loop_methods(ubot.get_chat_members(chat_id="@CryptoVedma"))
ubot.loop_methods(ubot.get_channels())
# ubot.loop_methods(ubot.join_chat(chat_id="@rozetked"))
# ubot.loop_methods(ubot.leave_chat(chat_id="@rozetked"))