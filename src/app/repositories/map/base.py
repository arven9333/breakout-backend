import logging
from settings import MAPS_DIR, SRC_DIR
from sqlalchemy import select, delete

from _logging.base import setup_logging
from enums.map import MapLevelEnum

from repositories.base import SQLAlchemyRepo
from models.maps.base import Map, MapLevel, MapLayer

logger = logging.getLogger(__name__)
setup_logging(__name__)


class MapServiceRepository(SQLAlchemyRepo):

    @staticmethod
    async def get_map_level_leaflet_path(map_id: int, level: MapLevelEnum):
        return str(
            MAPS_DIR / str(map_id) / level.value / 'tiles'
        ).split(str(SRC_DIR))[-1][1:]

    async def get_map_layer_leaflet_path(self, map_level_id: int, map_layer_id: int):
        map_level = await self.get_map_level_by_id(map_level_id)
        return str(
            MAPS_DIR / str(map_level['map_id']) / map_level['level'] / 'layers' / str(map_layer_id)
        ).split(str(SRC_DIR))[-1][1:]

    async def add_map(
            self,
            name: str,
            user_id: int,
    ) -> dict:

        map = Map(
            name=name,
            user_id=user_id,
        )
        async with self.session as session:
            await session.add(map)
            await session.flush()

            return {
                "id": map.id,
                "name": name
            }

    async def get_map_by_id(self, map_id: int):
        query = select(
            Map
        ).where(
            Map.id == map_id
        )

        async with self.session as session:
            result = await session.execute(query)

            if map := result.scalar_one():
                return map
            return

    async def delete_map(self, map_id: int):
        query = delete(
            Map
        ).where(
            Map.id == map_id
        )

        async with self.session as session:
            await session.execute(query)
            await session.flush()

    async def add_map_level(
            self,
            map_id: int,
            level: MapLevelEnum,
    ) -> dict:

        map_level = MapLevel(
            map_id=map_id,
            level=level,
        )
        async with self.session as session:
            await session.add(map_level)
            await session.flush()

            return {
                "id": map_level.id,
                "level": map_level.level.value,
                "map_id": map_level.map_id,
                "leaflet_path": await self.get_map_level_leaflet_path(
                    map_id=map_level.map_id,
                    level=level
                )
            }

    async def map_level_exists(self, map_id: int, level: MapLevelEnum):
        query = select(
            MapLevel
        ).where(
            MapLevel.map_id == map_id,
            MapLevel.level == level.value
        )

        async with self.session as session:
            result = await session.execute(query)

            test_ = result.scalar_one_or_none()

            return test_ is not None

    async def get_map_level_by_id(self, map_level_id: int):
        query = select(
            MapLevel
        ).where(
            MapLevel.id == map_level_id
        )

        async with self.session as session:
            result = await session.execute(query)

            if map_level := result.scalar_one():
                return {
                    "id": map_level.id,
                    "level": map_level.level.value,
                    "map_id": map_level.map_id,
                    "leaflet_path": await self.get_map_level_leaflet_path(
                        map_id=map_level.map_id,
                        level=map_level.level
                    )
                }
            return

    async def delete_map_level(self, map_level_id: int):
        query = delete(
            MapLevel
        ).where(
            MapLevel.id == map_level_id
        )

        async with self.session as session:
            await session.execute(query)
            await session.flush()

    async def create_map_layer(self, map_level_id: int):
        map_layer = MapLayer(
            map_level_id=map_level_id
        )

        async with self.session as session:
            await session.add(map_layer)
            await session.flush()

            temp = {
                "id": map_layer.id,
                "map_level_id": map_layer.map_level_id
            }

        return temp | {
            "leaflet_path": await self.get_map_layer_leaflet_path(
                map_level_id=temp['map_level_id'],
                map_layer_id=temp['id']
            )}

    async def get_map_layer_by_id(self, map_layer_id: int):

        query = select(
            MapLayer
        ).where(
            MapLayer.id == map_layer_id
        )

        async with self.session as session:
            result = await session.execute(query)

            if map_layer := result.scalar_one():
                return {
                    "id": map_layer.id,
                    "map_level_id": map_layer.map_level_id,
                    "leaflet_path": await self.get_map_layer_leaflet_path(
                        map_level_id=map_layer.map_level_id,
                        map_layer_id=map_layer.id
                    )
                }
            return

    async def delete_map_layer(self, map_layer_id: int):
        query = delete(
            MapLayer
        ).where(
            MapLayer.id == map_layer_id
        )

        async with self.session as session:
            await session.execute(query)
            await session.flush()
