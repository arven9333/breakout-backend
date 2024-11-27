from fastapi import APIRouter, UploadFile, File, HTTPException
from dependencies.map.base import MAP_SERVICE_DEP
from dependencies.map.icon import ICON_ACTIONS_SERVICE_DEP
from dependencies.user.auth import USER_ID_DEP
from dependencies.user.roles import ADMIN_ROLE_DEP
from dependencies.user.user_service import USER_SERVICE_DEP
from enums.map import MapLevelEnum, MapStatusEnum
from scheme.request.map.base import ActionScheme
from scheme.response.map.base import MapScheme, MapLayerScheme

router = APIRouter(tags=["maps.v1.service"], prefix='/service')


@router.post('/create', dependencies=[ADMIN_ROLE_DEP], response_model=MapScheme)
async def _create_map(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,

        name: str,
        status: MapStatusEnum = MapStatusEnum.hide,
):
    map = await map_service.create_map(
        name=name,
        user_id=user_id,
        status=status,
    )

    return map


@router.post('/mapLayer/create', dependencies=[ADMIN_ROLE_DEP], response_model=MapLayerScheme)
async def _create_map_layer(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,
        map_id: int,
        file: UploadFile = File(...),

):
    stream = await file.read()

    map_layer, status = await map_service.create_map_layer(
        stream=stream,
        map_id=map_id,
        format_str=file.filename.rsplit('.')[-1]
    )

    if status is True:
        for level in MapLevelEnum:
            await map_service.create_map_level(
                map_layer_id=map_layer['id'],
                level=level
            )
    else:
        await map_service.delete_map_layer(map_layer['id'])
        raise HTTPException(status_code=500, detail="Возникла ошибка при создание слоя")

    return map_layer


@router.delete('/delete', dependencies=[ADMIN_ROLE_DEP])
async def _delete_map(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,
        map_id: int,
):
    await map_service.delete_map(map_id)
    return {
        "success": 1
    }


@router.patch('/update')
async def _update_map(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,
        map_id: int,
        status: MapStatusEnum,
):
    await map_service.update_map(map_id=map_id, status=status, )
    return {
        "success": 1
    }


@router.delete('/mapLayer/delete', dependencies=[ADMIN_ROLE_DEP])
async def _delete_map_layer(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,
        map_layer_id: int,
):
    await map_service.delete_map_layer(map_layer_id)
    return {
        "success": 1
    }


@router.post('/mapLayer/update', dependencies=[ADMIN_ROLE_DEP])
async def _update_map_layer(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,
        map_layer_id: int,
        center: list[str, int, dict]

):
    map_layer = await map_service.update_map_layer(center, map_layer_id)
    return map_layer


@router.get('/allMetrics')
async def _get_all_metrics(
        user_service: USER_SERVICE_DEP,
        map_service: MAP_SERVICE_DEP,
        user_id: USER_ID_DEP | None = None,
        status: MapStatusEnum | None = None,
):
    if user_id is not None:
        user = await user_service.get_user_by_id(user_id)

    data = await map_service.get_metrics(status=status, user_id=user_id)

    return data


@router.post('/actions/save', dependencies=[ADMIN_ROLE_DEP])
async def _save_actions(
        user_id: USER_ID_DEP,
        icon_actions_service: ICON_ACTIONS_SERVICE_DEP,
        actions: list[ActionScheme],
):
    await icon_actions_service.handle_actions(actions)

    return {
        "success": 1
    }
