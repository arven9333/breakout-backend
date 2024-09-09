from fastapi import APIRouter, FastAPI
from routers import api
from routers import index


def setup_routers(app: FastAPI, app_root: str):
    root_router = APIRouter(prefix=app_root)

    root_router.include_router(index.router)
    root_router.include_router(api.router)

    app.include_router(root_router)
