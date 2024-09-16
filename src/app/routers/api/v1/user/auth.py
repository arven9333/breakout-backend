from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from scheme.request.user.auth import TokenGetScheme
from scheme.response.user.auth import TokenScheme
from dependencies.user.auth import AUTH_SERVICE_DEP
from dependencies.user.user_service import USER_SERVICE_DEP

router = APIRouter(tags=["user.v1.auth"], prefix='/auth')


@router.post('/login', response_model=TokenScheme)
async def _login(
        auth_service: AUTH_SERVICE_DEP,
        user_service: USER_SERVICE_DEP,
        creds: TokenGetScheme,
):
    user = await user_service.get_user_db_by_email(creds.email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    password = await auth_service.verify_password(creds.password, user.password),

    if password is False:
        raise HTTPException(status_code=403, detail="Password wrong. Access Denied")

    token = auth_service.create_jwt_token(user.id, user.email)

    return {
        "token": token
    }
