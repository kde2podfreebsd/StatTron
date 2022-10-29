from typing import List
from fastapi import FastAPI, HTTPException

from .database import metadata, engine, database

from .crud import get_account_by_username, get_account, get_channel_account,\
create_account, create_account_channel, get_accounts, get_channels

from .schemas import Account, AccountCreate, ChannelAccount, Channel, ChannelCreate

# import sys
# sys.path.append("..")
# from UserBot.TGUserAgent.UserBot import UserBot

metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/accounts/", response_model=Account)
async def init_account(user: AccountCreate):
    db_user = await get_account_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await create_account(account=user)


@app.get("/accounts/", response_model=List[Account])
async def read_accounts(skip: int = 0, limit: int = 100):
    return await get_accounts(skip=skip, limit=limit)


@app.get("/accounts/{account_id}", response_model=Account)
async def read_account(account_id: int):
    db_user = await get_account(account_id=account_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_user


@app.post("/accounts/{account_id}/channel/", response_model=Channel)
async def create_channel_for_account(account_id: int, channel: ChannelCreate):
    return await create_account_channel(channel=channel, account_id=account_id)


@app.get("/channels/", response_model=List[Channel])
async def read_channels(skip: int = 0, limit: int = 100):
    return await get_channels(skip=skip, limit=limit)


@app.get("/channels/{channel_id}", response_model=ChannelAccount)
async def read_channel(channel_id: int):
    return await get_channel_account(pk=channel_id)