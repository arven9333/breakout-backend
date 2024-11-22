from fastapi import APIRouter, Depends

from dependencies.user.auth import USER_ID_DEP
from dependencies.user.user_service import USER_SERVICE_DEP
from dto.request.user.registration import UserDTO
from scheme.request.user.base import UserCreateSchema
from scheme.response.user.base import UserGetSchema

router = APIRouter(tags=["user.v1.service"], prefix="/service")


@router.get('/getUserByToken', response_model=UserDTO)
async def _get_user_by_token(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
):
    user_dto = await user_service.get_user_by_id(user_id)
    return user_dto


@router.post('/create', response_model=UserGetSchema)
async def _create_user(
        user_service_dep: USER_SERVICE_DEP,
        user_create_scheme: UserCreateSchema,
):
    new_user = await user_service_dep.create_user(user_create_scheme.as_dataclass())
    return new_user
