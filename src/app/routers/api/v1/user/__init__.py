from fastapi import APIRouter
from .auth import router as auth_router
from .base import router as registration_router
from .auth_callback import router as callback_router
from .password import router as password_router
from .donation import router as donation_router

router = APIRouter(prefix="/user")

router.include_router(auth_router)
router.include_router(registration_router)
router.include_router(callback_router)
router.include_router(password_router)
router.include_router(donation_router)
