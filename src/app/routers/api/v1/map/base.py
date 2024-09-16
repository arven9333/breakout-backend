from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from dependencies.map.base import MAP_SERVICE_DEP
from dependencies.map.icon import ICON_ACTIONS_SERVICE_DEP
from dependencies.user.auth import USER_ID_DEP
from enums.map import MapLevelEnum
from scheme.request.map.base import ActionScheme
from scheme.response.map.base import MapScheme, MapLevelScheme, MapLayerScheme

router = APIRouter(tags=["maps.v1.service"], prefix='/service')


@router.post('/create', response_model=MapScheme)
async def _create_map(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,
        name: str,
):
    map = await map_service.create_map(
        name=name,
        user_id=user_id,
    )

    return map


@router.post('/mapLevel/create', response_model=MapLevelScheme)
async def _create_map_level(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,
        map_id: int,
        level: MapLevelEnum,
        file: UploadFile = File(...),

):
    stream = await file.read()

    map_level = await map_service.create_map_level(
        stream=stream,
        level=level,
        map_id=map_id,
    )

    return map_level


@router.post('/mapLayer/create', response_model=MapLayerScheme)
async def _create_map_layer(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,
        map_level_id: int,
        file: UploadFile = File(...),

):
    stream = await file.read()

    map_layer = await map_service.create_map_layer(
        stream=stream,
        map_level_id=map_level_id,
    )

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


@router.delete('/mapLevel/delete')
async def _delete_map_level(
        user_id: USER_ID_DEP,
        map_service: MAP_SERVICE_DEP,
        map_level_id: int,
):
    await map_service.delete_map_level(map_level_id)
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
):
    data = await map_service.get_metrics()

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
