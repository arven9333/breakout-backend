from fastapi import APIRouter

from .base import router as MapRouter
from .icons import router as IconRouter
from .categories import router as CategoryRouter

router = APIRouter(prefix="/maps")

router.include_router(IconRouter)
router.include_router(MapRouter)
router.include_router(CategoryRouter)