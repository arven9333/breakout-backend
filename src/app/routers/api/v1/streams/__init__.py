from fastapi import APIRouter
from .base import router as stream_base_router

router = APIRouter(prefix="/streams")

router.include_router(stream_base_router)
