from fastapi import APIRouter
from dependencies.map.icon import ICON_SERVICE_DEP
from dependencies.user.auth import USER_ID_DEP

from scheme.response.map.icons import CategoryResponseScheme

router = APIRouter(tags=["maps.v1.service"], prefix='/service/categories')


@router.post('/list', response_model=CategoryResponseScheme)
async def _create_map(
        #user_id: USER_ID_DEP,
        icon_service: ICON_SERVICE_DEP,
        offset: int = 0,
        limit: int = 100,
):
    categories = await icon_service.get_categories(offset=offset, limit=limit)
    return {
        "categories": categories
    }
