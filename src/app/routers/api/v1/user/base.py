from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from starlette.requests import Request

from dependencies.user.auth import USER_ID_DEP
from dependencies.user.user_service import USER_SERVICE_DEP
from dto.request.user.avatar import UserAvatarUpdateDTO, UserAvatarCreateDTO
from dto.request.user.registration import UserUpdateDTO

from scheme.request.user.avatar import UserAvatarCreateScheme, UserAvatarUpdateScheme
from scheme.request.user.base import UserCreateSchema, UserUpdateScheme
from scheme.response.user.avatar import UserAvatarScheme
from scheme.response.user.base import UserSchema, UserSearchResponseSchema, UserSearchSchema

router = APIRouter(tags=["user.v1.service"], prefix="/service")


@router.get('/getUserByToken', response_model=UserSchema)
async def _get_user_by_token(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
):
    user_dto = await user_service.get_user_by_id(user_id)
    return user_dto


@router.get('/getUserProfile', response_model=UserSchema)
async def _get_user_by_token(
        user_id: USER_ID_DEP,
        user_id_target: int,
        user_service: USER_SERVICE_DEP,
):
    main_user = await user_service.get_user_by_id(user_id, need_exception=True)
    if main_user.find_teammates is False:
        raise HTTPException(status_code=403, detail="User can't check others profile")

    user_dto = await user_service.get_user_by_id(user_id_target, need_exception=True)
    return user_dto


@router.post('/create', response_model=UserSchema)
async def _create_user(
        user_service_dep: USER_SERVICE_DEP,
        user_create_scheme: UserCreateSchema,
):
    new_user = await user_service_dep.create_user(user_create_scheme.as_dataclass())
    return new_user


@router.patch('/update', response_model=UserSchema)
async def _update_user(
        user_id: USER_ID_DEP,
        user_service_dep: USER_SERVICE_DEP,
        user_update_scheme: UserUpdateScheme
):
    user = await user_service_dep.get_user_by_id(user_id, need_exception=True)

    updated_user = await user_service_dep.update_user(
        user_update_dto=UserUpdateDTO(
            **user_update_scheme.model_dump()
        ),
        user_id=user_id,
    )
    return updated_user


@router.post('/avatar/update', response_model=UserAvatarScheme)
async def _update_avatar(
        request: Request,
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        user_avatar_update_scheme: UserAvatarUpdateScheme = Depends(),
        file: Optional[bytes] = File(None),
):
    if file is not None:
        file = request._form._dict['file']

    user_avatar_update_dto = UserAvatarUpdateDTO(
        **user_avatar_update_scheme.model_dump(),
    )

    user_avatar_dto = await user_service.update_avatar(user_avatar_update_dto, user_id, file)
    return user_avatar_dto


@router.post('/avatar/create', response_model=UserAvatarScheme)
async def _create_avatar(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        user_avatar_create_scheme: UserAvatarCreateScheme = Depends(),
        file: UploadFile = File(...),
):
    user_avatar_update_dto = UserAvatarCreateDTO(
        **user_avatar_create_scheme.model_dump(),
        user_id=user_id,
    )

    user_avatar_dto = await user_service.create_avatar(user_avatar_update_dto, file)
    return user_avatar_dto


@router.get('/avatar/get', response_model=UserAvatarScheme)
async def _get_avatar(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
):
    user_avatar_dto = await user_service.get_avatar_by_user_id(user_id=user_id, raise_exception=True)
    return user_avatar_dto


@router.delete('/avatar/delete', response_model=UserAvatarScheme)
async def _get_avatar(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
):
    user_avatar_dto = await user_service.delete_avatar(user_id)
    return user_avatar_dto


@router.get("/users/search", response_model=UserSearchResponseSchema)
async def _search_users(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        raids: str | None = None,
        hours: str | None = None,
        rank: str | None = None,
        stars_from: int | None = None,
        stars_to: int | None = None,
        damage: str | None = None,
        query_search: str | None = None,
        limit: int = 100,
        offset: int = 0,
):
    main_user = await user_service.get_user_by_id(user_id, need_exception=True)
    if main_user.find_teammates is False:
        raise HTTPException(status_code=403, detail="User can't check others profile")

    users_search, total = await user_service.search_users(
        user_id=user_id,
        raids=raids,
        hours=hours,
        rank=rank,
        query_search=query_search,
        stars_from=stars_from,
        stars_to=stars_to,
        damage=damage,
        limit=limit,
        offset=offset,
    )

    return {
        "list": users_search,
        "total": total,
        "limit": limit,
        "offset": offset,
    }
