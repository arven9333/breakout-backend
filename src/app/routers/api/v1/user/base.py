from fastapi import APIRouter, Depends, UploadFile, File

from dependencies.user.auth import USER_ID_DEP
from dependencies.user.user_service import USER_SERVICE_DEP
from dto.request.user.avatar import UserAvatarUpdateDTO, UserAvatarCreateDTO
from dto.request.user.registration import UserDTO, UserUpdateDTO
from dto.response.user.avatar import UserAvatarDTO
from scheme.request.user.avatar import UserAvatarCreateScheme, UserAvatarUpdateScheme
from scheme.request.user.base import UserCreateSchema, UserUpdateScheme
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


@router.patch('/update', response_model=UserGetSchema)
async def _update_user(
        user_id: int,
        user_service_dep: USER_SERVICE_DEP,
        user_update_scheme: UserUpdateScheme
):
    user = await user_service_dep.get_user_by_id(user_id, need_exception=True)

    updated_user = await user_service_dep.update_user(
        user_update_dto=UserUpdateDTO(
            **user_update_scheme.model_dump()
        )
    )
    return updated_user


@router.patch('/avatar/update', response_model=UserAvatarDTO)
async def _update_avatar(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        zoom: int | None = None,
        alignment: int | None = None,
        file: UploadFile | None = None,
):
    user_avatar_update_dto = UserAvatarUpdateDTO(
        zoom=zoom,
        alignment=alignment,
    )

    user_avatar_dto = await user_service.update_avatar(user_avatar_update_dto, user_id, file)
    return user_avatar_dto


@router.post('/avatar/create', response_model=UserAvatarDTO)
async def _create_avatar(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        zoom: int = 1,
        alignment: int = 1,
        file: UploadFile = File(...),
):
    user_avatar_update_dto = UserAvatarCreateDTO(
        zoom=zoom,
        alignment=alignment,
        user_id=user_id,
    )

    user_avatar_dto = await user_service.create_avatar(user_avatar_update_dto, file)
    return user_avatar_dto


@router.get('/avatar/get', response_model=UserAvatarDTO)
async def _get_avatar(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
):
    user_avatar_dto = await user_service.get_avatar_by_user_id(user_id=user_id, raise_exception=True)
    return user_avatar_dto


@router.delete('/avatar/delete', response_model=UserAvatarDTO)
async def _get_avatar(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
):
    user_avatar_dto = await user_service.delete_avatar(user_id)
    return user_avatar_dto
