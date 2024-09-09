from fastapi import APIRouter
from .auth import router as auth_router
from .registration import router as registration_router

router = APIRouter(prefix="/user")

router.include_router(auth_router)
router.include_router(registration_router)

