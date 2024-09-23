import logging

from sqlalchemy.orm import joinedload, aliased

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
    async def get_map_layer_leaflet_path(map_id: int, map_layer_id: int):
        return str(
            MAPS_DIR / str(map_id) / str(map_layer_id) / "tiles"
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
                return {
                    "id": map.id,
                    "name": map.name,
                }
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
            map_layer_id: int,
            level: MapLevelEnum,
    ) -> dict:

        map_level = MapLevel(
            map_layer_id=map_layer_id,
            level=level,
        )
        async with self.session as session:
            await session.add(map_level)
            await session.flush()

            return {
                "id": map_level.id,
                "level": map_level.level.value,
                "map_layer_id": map_level.map_layer_id,
            }

    async def create_map_layer(self, map_id: int):
        map_layer = MapLayer(
            map_id=map_id
        )

        async with self.session as session:
            await session.add(map_layer)
            await session.flush()

            return {
                "id": map_layer.id,
                "map_id": map_layer.map_id,
                "leaflet_path": await self.get_map_layer_leaflet_path(
                    map_id=map_layer.map_id,
                    map_layer_id=map_layer.id
                )
            }

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
                    "map_id": map_layer.map_id,
                    "leaflet_path": await self.get_map_layer_leaflet_path(
                        map_id=map_layer.map_id,
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

    async def get_metrics(self):

        query = select(
            Map
        ).join(
            Map.map_layers
        ).options(
            joinedload(
                Map.map_layers
            ).joinedload(
                MapLayer.map_levels
            ).joinedload(
                MapLevel.metrics
            ),
        ).order_by(
            Map.id.desc(),
            MapLayer.id.desc(),
        )

        async with self.session as session:
            result = await session.execute(query)

            maps = result.unique().scalars().all()

            return [
                {
                    "map_id": map.id,
                    "name": map.name,
                    "layers": [
                        {
                            "map_layer_id": layer.id,
                            "leaflet_path": str(MAPS_DIR / str(map.id) / str(layer.id) / 'tiles').split(str(SRC_DIR))[
                                                -1][1:],
                            "levels": {
                                map_level.level.value: {
                                    "map_level_id": map_level.id,
                                    "icons": [
                                        {
                                            "icon_level_id": icon.id,
                                            "coord_x": icon.coord_x,
                                            "coord_y": icon.coord_y,
                                            "icon_id": icon.icon_id
                                        }
                                        for icon in map_level.metrics
                                    ]
                                }
                                for map_level in layer.map_levels
                            }
                        }
                        for layer in map.map_layers
                    ]
                }
                for map in maps
            ]
