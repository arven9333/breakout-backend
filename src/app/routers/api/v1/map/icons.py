from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from scheme.request.map.icons import IconCreateScheme
from scheme.response.map.icons import IconScheme, IconCategoryScheme
from dto.request.map.icon import IconCreateDTO, IconCategoryCreateDTO

from dependencies.map.icon import ICON_SERVICE_DEP
from dependencies.user.auth import USER_ID_DEP

router = APIRouter(tags=["maps.v1.service.icons"], prefix='/service/icons')


@router.post('/category/create', response_model=IconCategoryScheme)
async def _create_icon_category(
        icon_service: ICON_SERVICE_DEP,
        name: str,
):
    icon_category = await icon_service.add_icon_category(
        IconCategoryCreateDTO(name=name)
    )

    return icon_category


@router.delete('/category/delete')
async def _delete_icon(
        user_id: USER_ID_DEP,
        icon_service: ICON_SERVICE_DEP,
        icon_category_id: int,
):
    await icon_service.delete_category_icon(icon_category_id)
    return {
        "success": 1
    }


@router.post('/create', response_model=IconScheme)
async def _create_icon(
        user_id: USER_ID_DEP,
        icon_service: ICON_SERVICE_DEP,
        icon_scheme: IconCreateScheme = Depends(),
        file: UploadFile = File(...),
):
    image = await icon_service.upload_icon(file, category_id=icon_scheme.category_id)
    icon = await icon_service.add_icon(
        IconCreateDTO(
            image=image,
            **icon_scheme.model_dump()
        )
    )
    return icon


@router.delete('/delete')
async def _delete_icon(
        user_id: USER_ID_DEP,
        icon_service: ICON_SERVICE_DEP,
        icon_id: int,
):
    await icon_service.delete_icon(icon_id)
    return {
        "success": 1
    }
