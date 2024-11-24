from typing import Annotated
from fastapi import Depends

from dependencies.user.user_service import USER_SERVICE_DEP
from dependencies.user.auth import USER_ID_DEP


async def admin_role_required(
        user_service: USER_SERVICE_DEP,
        user_id: USER_ID_DEP,
):
    return await user_service.admin_role_required(user_id)


async def premium_role_required(
        user_service: USER_SERVICE_DEP,
        user_id: USER_ID_DEP,
):
    return await user_service.premium_user_role_required(user_id)


async def non_default_role_required(
        user_service: USER_SERVICE_DEP,
        user_id: USER_ID_DEP,
):
    return await user_service.no_default_role_required(user_id)

ADMIN_ROLE_DEP = Depends(admin_role_required)
PREMIUM_ROLE_DEP = Depends(premium_role_required)
NON_DEFAULT_ROLE_DEP = Depends(non_default_role_required)
