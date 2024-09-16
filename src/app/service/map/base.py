from exceptions.map import MapLevelAlreadyExists
from scheme.request.map.base import ActionScheme
from settings import SRC_DIR, MAPS_DIR
from dataclasses import dataclass
from enums.map import MapLevelEnum
from repositories.map.base import MapServiceRepository
from service.map.icon import delete_file

from utils.image_to_tiles import generate_tiles


@dataclass
class MapService:
    repo: MapServiceRepository

    async def create_map(self, name: str, user_id: int) -> dict:
        map = await self.repo.add_map(name=name, user_id=user_id)

        return map

    async def create_map_level(self, stream: bytes, map_id: int, level: MapLevelEnum) -> dict:
        if await self.repo.map_level_exists(map_id, level):
            raise MapLevelAlreadyExists(details=f"Map with level: {level.value} already exists")

        map_level = await self.repo.add_map_level(
            map_id=map_id,
            level=level,
        )
        generate_tiles(stream, map_level['leaflet_path'])
        return map_level

    async def create_map_layer(self, stream: bytes, map_level_id: int) -> dict:

        map_layer = await self.repo.create_map_layer(
            map_level_id=map_level_id,

        )
        generate_tiles(stream, map_layer['leaflet_path'])

        return map_layer

    async def delete_map_layer(self, map_layer_id: int):
        map_layer = await self.repo.get_map_layer_by_id(map_layer_id)

        if map_layer is not None:
            await delete_file(SRC_DIR / map_layer['leaflet_path'].split('/tiles')[-1])
            await self.repo.delete_map_layer(map_layer_id)

    async def delete_map_level(self, map_level_id: int):
        map_level = await self.repo.get_map_level_by_id(map_level_id)

        if map_level is not None:
            await delete_file(SRC_DIR / map_level['leaflet_path'].split('/tiles')[0])
            await self.repo.delete_map_level(map_level_id)

    async def delete_map(self, map_id: int):

        map = await self.repo.get_map_by_id(map_id)

        if map is not None:
            await delete_file(MAPS_DIR / str(map['id']))
            await self.repo.delete_map(map_id)

    async def get_metrics(self):
        return await self.repo.get_metrics()
