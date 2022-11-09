import os
import logging
import time
import datetime
import asyncio
from dotenv import load_dotenv


from pyrogram import Client, filters, enums
from typing import Optional, List

from database.Channels import Channel, create_channel, get_channel, delete_channel, update_members_count
from database.Accounts import Account, create_account, get_account, delete_account, init_session
from database.Messages import Message, create_message
from database.database import db, app

config = load_dotenv()

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
    async def get_channels(self, account: Account, category: str):
        try:
            channels = dict()
            async with self.app as app:
                chat_ids = list()
                async for dialog in app.get_dialogs():
                    if str(dialog.chat.type) == "ChatType.CHANNEL":
                        chat_ids.append(dialog.chat.id)
                for id in chat_ids:
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
                            "category": category,
                            "photo_big_file_id": chat.photo.big_file_id if chat.photo != None else None,
                            "photo_small_file_id": chat.photo.small_file_id if chat.photo != None else None,
                            "small_photo_path": await app.download_media(chat.photo.small_file_id) if chat.photo != None else None,
                        }

                        res = create_channel(
                            channel_id = channels[chat.id]['id'],
                            is_scam = channels[chat.id]['is_scam'],
                            is_private = channels[chat.id]['is_private'],
                            title = channels[chat.id]['title'],
                            username = channels[chat.id]['username'],
                            members_count = channels[chat.id]['members_count'],
                            description = channels[chat.id]['description'],
                            category = channels[chat.id]['category'],
                            photo_big_file_id = channels[chat.id]['photo_big_file_id'],
                            photo_small_file_id = channels[chat.id]['photo_small_file_id'],
                            small_photo_path = channels[chat.id]['small_photo_path'],
                            average_views = 0.0,
                            er_all = 0.0
                        )

                        if res['status'] == True:
                            account.channels.append(res['channel'])
                            db.session.add(account)
                            db.session.commit()
                        else:
                            pass

                self.channels = channels

                return self.channels

        except Exception as e:
            return e

    async def download_media(self, file_id):
        try:
            # TODO: сделать удаление старых фото перед скачиванием (small_photo_path)
            async with self.app as app:
                return await app.download_media(file_id)
        except Exception as e:
            return e

    async def join_chat(self, account: Account, chat_id: str | int, category: str) -> "Result of join":
        try:
            async with self.app as app:
                res = await app.join_chat(chat_id)
                channels = dict()
                chat = await app.get_chat(res.id)
                if chat != None:
                    channels[chat.id] = {
                        "id": chat.id,
                        "is_scam": chat.is_scam,
                        "is_private": True if chat.username == None else False,
                        "title": chat.title,
                        "username": chat.username,
                        "members_count": chat.members_count,
                        "description": chat.description,
                        "category": category,
                        "photo_big_file_id": chat.photo.big_file_id if chat.photo != None else None,
                        "photo_small_file_id": chat.photo.small_file_id if chat.photo != None else None,
                        "small_photo_path": await app.download_media(
                            chat.photo.small_file_id) if chat.photo != None else None,
                    }

                    res = create_channel(
                        channel_id=channels[chat.id]['id'],
                        is_scam=channels[chat.id]['is_scam'],
                        is_private=channels[chat.id]['is_private'],
                        title=channels[chat.id]['title'],
                        username=channels[chat.id]['username'],
                        members_count=channels[chat.id]['members_count'],
                        description=channels[chat.id]['description'],
                        category=channels[chat.id]['category'],
                        photo_big_file_id=channels[chat.id]['photo_big_file_id'],
                        photo_small_file_id=channels[chat.id]['photo_small_file_id'],
                        small_photo_path=channels[chat.id]['small_photo_path'],
                        average_views=0.0,
                        er_all=0.0
                    )

                    if res['status'] == True:
                        account.channels.append(res['channel'])
                        db.session.add(account)
                        db.session.commit()
                    else:
                        pass

                self.channels = channels

                return res
        except Exception as e:
            return e

    async def leave_chat(self, chat_id: str | int) -> "Result of leave":
        try:
            async with self.app as app:
                #TODO: удаление аккаунта
                chat = await app.leave_chat(chat_id)
                print(chat.chats[0].id)
                return True

        except Exception as e:
            return e

    async def get_chat_members_count(self, chat_id: str | int) -> "Count of chat members":
        try:
            async with self.app as app:
                count = await app.get_chat_members_count(chat_id)
                res = update_members_count(channel_id = chat_id, members_count = count)
                return res
        except Exception as e:
            return e

    async def get_chat_history(self, chat_id: str | int, account: Account, mentions: Optional[List[str]] = list()) -> "List of chat messages":
        # try:
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
                            "text": message.text if message.text != None else message.caption,
                            "date": message.date,
                            "views": message.views,
                            "forward_from_chat": message.forward_from_chat.username \
                                if message.forward_from_chat != None else False,
                            "reactions": reaction_count(message.reactions),
                            "media": message.media if message.media != None else False,
                            "mentions": find_mentions(mentions)
                        }

                        res = create_message(
                            message_id = messages[message.id]["id"],
                            link = messages[message.id]["link"],
                            text = messages[message.id]["text"],
                            date = messages[message.id]["date"],
                            views = messages[message.id]["views"],
                            forward_from_chat = messages[message.id]["forward_from_chat"],
                            reaction = messages[message.id]["reactions"],
                            media = messages[message.id]["media"],
                            mentions = messages[message.id]["mentions"]
                        )

                        if res['status'] == True:
                            # print(res['message'])
                            i = 0
                            for channel in account.channels:
                                if chat_id == channel.channel_id:
                                    break
                                i += 1

                            account.channels[i].messages.append(res['message'])
                            db.session.add(account)
                            db.session.commit()
                        else:
                            pass

                    offset += 200

                avg_views = all_views/all_posts
                members_count = await app.get_chat_members_count(chat_id)
                er = (avg_views / int(members_count)) * 100

                i = 0
                for channel in account.channels:
                    if chat_id == channel.channel_id:
                        break
                    i += 1

                account.channels[i].average_views = avg_views
                account.channels[i].er_all = er

                db.session.add(account)
                db.session.commit()

                return messages, avg_views, er

        # except Exception as e:
        #     return e

    def loop_methods(self, fn):
        try:
            self.app.run(fn)
        except Exception as e:
            return e


def main():
    pass
    # Register new account!
    #----------------------
    # register_account = create_account(
    #     api_id=os.getenv('api_id'),
    #     api_hash=os.getenv('api_hash'),
    #     phone="89162107493",
    #     username=os.getenv('username'),
    #     host="149.154.167.50",
    #     port=443,
    #     public_key="-----BEGIN RSA PUBLIC KEY-----MII <...> AB-----END RSA PUBLIC KEY-----"
    # )
    # print(register_account)

    # Get account from db
    # ----------------------
    # get_account_res = get_account(username="donqhomo")
    # print(get_account_res)

    # Create session for account in db
    # ----------------------
    # res3 = init_session(username="donqhomo")
    # print(res3)

    # Delete account from db
    # ----------------------
    # res4 = delete_account(username="donqhomo")
    # print(res4)

    # Init User Agent Bot
    # ----------------------
    # if get_account_res['status']:
    #     ubot = UserBot(username=get_account_res['account'].username, debug=False)
    #
    #     loop = asyncio.get_event_loop()
    #     run = loop.run_until_complete

    # Get channels of account
    # ----------------------
    #     channels = run(ubot.get_channels(account = get_account_res['account'], category="category1"))
    #     for channel in channels:
    #         print(channel, "\n\n")

    # Download media from telegram
    # ----------------------
    # download_media = run(ubot.download_media(file_id="AQADAgADxbAxGyB2GUoAEAMAA7R3peUW____9UWLTY68ItIABB4E"))
    # print(download_media)

    # Join chat
    # ----------------------
    # join_chat = run(ubot.join_chat(chat_id = "@rozetked", account=get_account_res['account'], category="category2"))
    # print(join_chat)

    # Members count (+update members_count)
    # ----------------------
    # members_count = run(ubot.get_chat_members_count(chat_id=-1001007302005))
    # print(members_count)

    # Leave chat
    # ----------------------
    # res = run (ubot.leave_chat(chat_id=-1001007302005))
    # print(res)
    # leave_chat = delete_channel(channel_id=-1001007302005)
    # print(leave_chat)

    # Get chat History | update average views(for all times) and er(for all times)
    # ----------------------
    # chat_history, avg_views, er  = run(ubot.get_chat_history(chat_id=-1001301455979,account=get_account_res['account'], mentions=['donqhomo']))
    #
    # for res in chat_history:
    #     print(chat_history[res], '\n\n\n')
    #
    # print(avg_views)
    # print(er)




main()


