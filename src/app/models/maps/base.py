from __future__ import annotations

from sqlalchemy import BigInteger, String, Enum, UniqueConstraint, Float
from sqlalchemy.orm import Mapped, relationship

from enums.map import MapLevelEnum
from models.base import BaseModel, Column
from models.common.base import CascadeForeignKey, RestrictForeignKey
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

    map = relationship(Map, back_populates="map_levels")
    map_layers = relationship("MapLayer", back_populates="map_level")
    metrics = relationship("IconMetricLevel", back_populates="map_level")


class MapLayer(BaseModel):
    __tablename__ = "map_layer"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    map_level_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(MapLevel.id))

    map_level = relationship(MapLevel, back_populates="map_layers")
    metrics = relationship("IconMetricLayer", back_populates="map_layer")


class IconCategory(BaseModel):
    __tablename__ = 'icon_category'

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    name: Mapped[str] = Column(String(255), unique=True)

    icons = relationship("Icon", back_populates="category")


class Icon(BaseModel):
    __tablename__ = "icons"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    name: Mapped[str] = Column(String(255))
    image: Mapped[str] = Column(String(777))
    category_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(IconCategory.id))

    category = relationship(IconCategory, back_populates="icons")


class IconAbstract(BaseModel):
    __abstract__ = True

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    coord_x: Mapped[float] = Column(Float)
    coord_y: Mapped[float] = Column(Float)


class IconMetricLevel(IconAbstract):
    __tablename__ = "icon_metric_level"

    map_level_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(MapLevel.id))
    map_level = relationship(MapLevel, back_populates="metrics")


class IconMetricLayer(IconAbstract):
    __tablename__ = "icon_metric_layer"

    map_layer_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(MapLayer.id))
    map_layer = relationship(MapLayer, back_populates="metrics")
