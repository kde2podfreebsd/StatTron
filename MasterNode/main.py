import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from MasterNode.Handlers.AdvertisingPostsCatalogHandlers import (
    advertising_posts_catalog_router,
)
from MasterNode.Handlers.MainPageHandlers import main_page_router
from MasterNode.Handlers.СhannelСatalogHandlers import channel_catalog_router
from MasterNode.Handlers.ChannelStatisticsHandlers import channel_statistics_router

app = FastAPI(title="StatTron Master Node")

main_api_router = APIRouter()

main_api_router.include_router(
    main_page_router,
    prefix="/main_page",
    tags=["main_page"]
)

main_api_router.include_router(
    channel_catalog_router,
    prefix="/channel_catalog",
    tags=["channel_catalog"]
)

main_api_router.include_router(
    advertising_posts_catalog_router,
    prefix="/advertising_posts_catalog",
    tags=["advertising_posts_catalog"],
)

main_api_router.include_router(
    channel_statistics_router,
    prefix="/channel_statistics",
    tags=["channel_statistics"],
)

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9876)
