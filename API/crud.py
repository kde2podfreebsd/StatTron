from database import database
from models import Accounts, Channels
from schemas import Channel, ChannelCreate, Account, AccountCreate
import asyncio

async def get_account(account_id: int):
    account = dict(await database.fetch_one(Accounts.select().where(Accounts.c.id == account_id)))
    list_item = await database.fetch_all(Channels.select().where(Channels.c.owner_id == account["id"]))
    account.update({"channels": [dict(result) for result in list_item]})
    return account


async def get_account_by_username(username: str):
    return await database.fetch_one(Accounts.select().where(Accounts.c.username == username))


async def get_accounts(skip: int = 0, limit: int = 100):
    results = await database.fetch_all(Accounts.select().offset(skip).limit(limit))
    return [dict(result) for result in results]


async def create_account(account: AccountCreate):
    #TODO Добавить валидацию номера телефона
    db_account = Accounts.insert().values(
        api_id=account.api_id, api_hash=account.api_hash,
        username=account.username, host=account.host,
        port=account.port, phone=account.phone
    )
    account_id = await database.execute(db_account)
    return Account(**account.dict(), id=account_id)


async def get_channels(skip: int = 0, limit: int = 200):
    query = Channels.select().offset(skip).limit(limit)
    results = await database.fetch_all(query)
    return [dict(result) for result in results]


async def get_channel_account(pk: int):
    channel = dict(await database.fetch_one(Channels.select().where(Channels.c.id == pk)))
    account = dict(await database.fetch_one(Accounts.select().where(Accounts.c.id == channel["owner_id"])))
    channel.update({"owner": account})
    return channel


async def create_account_channel(channel: ChannelCreate, account_id: int):
    query = Channels.insert().values(**channel.dict(), owner_id=account_id)
    channel_id = await database.execute(query)
    return Channel(**channel.dict(), id=channel_id, owner_id=account_id)

async def startup():
    await database.connect()

async def shutdown():
    await database.disconnect()

def main():
    loop = asyncio.new_event_loop()
    run = loop.run_until_complete

    run(startup())
    print(run(get_accounts))

if __name__ == "__main__":
    main()

