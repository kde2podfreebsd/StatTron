import asyncio

from Database.DAL.ChannelDAL import ChannelDAL
from Database.session import async_session


# async def mmm():
#     async with async_session() as session:
#         async with session.begin():
#             channels = ChannelDAL(session)
#             c = await channels.search_by_filters(page=1)
#             for i in c[0]:
#                 print(i)
#             print(c[1])
#
#
# asyncio.run(mmm())

# from UserBotTelethon import UserAgent
# asyncio.run(UserAgent.main())
