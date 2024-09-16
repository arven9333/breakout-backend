from fastapi import APIRouter, Depends
from dependencies.user.user_service import USER_SERVICE_DEP
from scheme.request.user.base import UserCreateSchema
from scheme.response.user.base import UserGetSchema

router = APIRouter(tags=["user.v1.service"], prefix="/service")


@router.post('/create', response_model=UserGetSchema)
async def _create_user(
        user_service_dep: USER_SERVICE_DEP,
        user_create_scheme: UserCreateSchema,
):
    new_user = await user_service_dep.create_user(user_create_scheme.as_dataclass())
    return new_user
