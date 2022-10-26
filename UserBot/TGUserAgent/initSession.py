import configparser
import asyncio
from pyrogram import Client
import sys

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['donqhomo']['api_id']
api_hash = config['donqhomo']['api_hash']

async def main(session:str):
    async with Client("sessions/donqhomo", api_id, api_hash) as app:
        await app.send_message("me", "create session")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[0]))
