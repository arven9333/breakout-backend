from fastapi import APIRouter, UploadFile, File, HTTPException
from dependencies.map.base import MAP_SERVICE_DEP
from dependencies.map.icon import ICON_ACTIONS_SERVICE_DEP
from dependencies.user.auth import USER_ID_DEP
from enums.map import MapLevelEnum, MapStatusEnum
from scheme.request.map.base import ActionScheme
from scheme.response.map.base import MapScheme, MapLayerScheme

router = APIRouter(tags=["maps.v1.service"], prefix='/service')


@router.post('/create', response_model=MapScheme)
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


@router.post('/mapLayer/create', response_model=MapLayerScheme)
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


@router.delete('/delete')
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
    await map_service.update_map(map_id=map_id, status=status,)
    return {
        "success": 1
    }


@router.delete('/mapLayer/delete')
async def _delete_map_layer(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,
        map_layer_id: int,
):
    await map_service.delete_map_layer(map_layer_id)
    return {
        "success": 1
    }


@router.get('/allMetrics')
async def _get_all_metrics(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,
        status: MapStatusEnum | None = None,
):
    data = await map_service.get_metrics(status=status)

    return data


@router.post('/actions/save')
async def _save_actions(
        user_id: USER_ID_DEP,
        icon_actions_service: ICON_ACTIONS_SERVICE_DEP,
        actions: list[ActionScheme],
):
    await icon_actions_service.handle_actions(actions)

    return {
        "success": 1
    }
