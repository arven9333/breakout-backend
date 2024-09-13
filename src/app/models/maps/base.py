from __future__ import annotations

from enums.map import MapLevelEnum
from models.base import BaseModel, Column
from models.common.base import CascadeForeignKey, RestrictForeignKey

from sqlalchemy import BigInteger, String, Float, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from models.user.base import User


class Map(BaseModel):
    __tablename__ = 'maps'

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    name: Mapped[str] = Column(String(255))
    user_id: Mapped[int] = Column(BigInteger, RestrictForeignKey(User.id))

    user = relationship(User)
    map_levels = relationship("MapLevel", back_populates="map")


class MapLevel(BaseModel):
    __tablename__ = 'map_levels'
    __table_args__ = (
        UniqueConstraint(*('map_id', "level"), name='map_levels_unique'),
        {'extend_existing': True}
    )
    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    map_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(Map.id))
    level: Mapped[MapLevelEnum] = Column(Enum(MapLevelEnum))

    map = relationship(Map, back_populates="map_level")
    map_layers = relationship("MapLayer", back_populates="map_level")
    metrics = relationship("IconMetricLevel", back_populates="map_level")


class MapLayer(BaseModel):
    __tablename__ = "map_layer"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    map_level_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(MapLevel.id))

    map_level = relationship(Map, back_populates="map_layer")
    metrics = relationship("IconMetricLayer", back_populates="map_layer")
