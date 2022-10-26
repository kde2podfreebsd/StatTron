import asyncio
from typing import List
from fastapi import FastAPI, HTTPException
from .database import metadata, engine, database
from .crud import get_user_by_email, get_user, get_item_user, create_user, create_user_item, get_users, get_items
from .schemas import User, UserCreate, ItemUser, Item, ItemCreate
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


@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    db_user = await get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(user=user)


@app.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100):
    return await get_users(skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    db_user = await get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=Item)
async def create_item_for_user(user_id: int, item: ItemCreate):
    return await create_user_item(item=item, user_id=user_id)


@app.get("/items/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 100):
    return await get_items(skip=skip, limit=limit)


@app.get("/items/{item_id}", response_model=ItemUser)
async def read_item(item_id: int):
    return await get_item_user(pk=item_id)