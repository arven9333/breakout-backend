from settings import MAPS_DIR
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

    async def create_map_level(self, map_layer_id: int, level: MapLevelEnum) -> dict:

        map_level = await self.repo.add_map_level(
            map_layer_id=map_layer_id,
            level=level,
        )
        return map_level

    async def create_map_layer(self, stream: bytes, map_id: int, format_str: str) -> tuple[dict, bool]:

        map_layer = await self.repo.create_map_layer(
            map_id=map_id,
        )

        try:
            generate_tiles(stream=stream, path=map_layer['leaflet_path'], format_str=format_str)
            status = True
        except Exception as e:
            status = False
        return map_layer, status

    async def delete_map_layer(self, map_layer_id: int):
        map_layer = await self.repo.get_map_layer_by_id(map_layer_id)

        if map_layer is not None:
            await delete_file(MAPS_DIR / str(map_layer['map_id']) / str(map_layer['id']))
            await self.repo.delete_map_layer(map_layer_id)

    async def delete_map(self, map_id: int):

        map = await self.repo.get_map_by_id(map_id)

        if map is not None:
            await delete_file(MAPS_DIR / str(map['id']))
            await self.repo.delete_map(map_id)

    async def get_metrics(self):
        return await self.repo.get_metrics()
