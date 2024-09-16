from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from scheme.request.user.auth import TokenGetScheme
from scheme.response.user.auth import TokenScheme
from dependencies.user.auth import AUTH_SERVICE_DEP
from dependencies.user.user_service import USER_SERVICE_DEP

router = APIRouter(tags=["maps.v1.service"], prefix='/service')