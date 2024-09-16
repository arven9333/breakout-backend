from fastapi import APIRouter

from .user import router as auth_router
from .map import router as map_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth_router)
v1_router.include_router(map_router)

