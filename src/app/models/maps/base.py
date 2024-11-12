from __future__ import annotations

from sqlalchemy import BigInteger, String, Enum, UniqueConstraint, Float, Integer, Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from enums.figure import FigureEnum
from enums.map import MapLevelEnum, MapStatusEnum
from models.base import BaseModel, Column
from models.common.base import CascadeForeignKey, RestrictForeignKey
from models.user.base import User


class Map(BaseModel):
    __tablename__ = 'maps'

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    name: Mapped[str] = Column(String(255))
    user_id: Mapped[int] = Column(BigInteger, RestrictForeignKey(User.id))
    status: Mapped[MapStatusEnum] = mapped_column(default=MapStatusEnum.hide, nullable=True)
    user = relationship(User)
    map_layers = relationship("MapLayer", back_populates="map", uselist=True)


class MapLayer(BaseModel):
    __tablename__ = "map_layers"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    map_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(Map.id))

    height: Mapped[int] = Column(BigInteger, default=0, nullable=True)
    width: Mapped[int] = Column(BigInteger, default=0, nullable=True)
    center: Mapped[dict] = Column(
        JSONB,
        nullable=True,
        server_default=None,
        comment="центровка",
    )

    map = relationship(Map, back_populates="map_layers", uselist=False)
    map_levels = relationship("MapLevel", back_populates="map_layer", uselist=True)


class MapLevel(BaseModel):
    __tablename__ = 'map_levels'
    __table_args__ = (
        UniqueConstraint(*('map_layer_id', "level"), name='map_levels_unique'),
        {'extend_existing': True}
    )
    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    map_layer_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(MapLayer.id))
    level: Mapped[MapLevelEnum] = Column(Enum(MapLevelEnum))

    map_layer = relationship("MapLayer", back_populates="map_levels", uselist=False)
    metrics = relationship("IconMetricLevel", back_populates="map_level", uselist=True)
    figures = relationship("IconMetricFigure", back_populates="map_level", uselist=True)


class IconCategory(BaseModel):
    __tablename__ = 'icon_category'

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    name: Mapped[str] = Column(String(255), unique=True)

    icons = relationship("Icon", back_populates="category", uselist=True)


class Icon(BaseModel):
    __tablename__ = "icons"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    name: Mapped[str] = Column(String(255))
    image: Mapped[str] = Column(String(777))
    category_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(IconCategory.id))
    category = relationship(IconCategory, back_populates="icons", uselist=False)


class IconAbstract(BaseModel):
    __abstract__ = True

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    icon_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(Icon.id))
    coord_x: Mapped[float] = Column(Float)
    coord_y: Mapped[float] = Column(Float)


class IconMetricLevel(IconAbstract):
    __tablename__ = "icon_metric_level"

    map_level_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(MapLevel.id))
    map_level = relationship(MapLevel, back_populates="metrics", uselist=False)
    radius: Mapped[float] = Column(Float, nullable=True)
    radius_color: Mapped[str] = Column(String(255), nullable=True)
    icon = relationship(Icon, uselist=False)


class IconMetricFigure(BaseModel):
    __tablename__ = "icon_metric_figure"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    map_level_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(MapLevel.id))

    coord_x: Mapped[float] = Column(Float, nullable=True)
    coord_y: Mapped[float] = Column(Float, nullable=True)
    color: Mapped[str] = Column(String, nullable=True)
    content: Mapped[str] = Column(String, nullable=True)
    type: Mapped[FigureEnum] = Column(Enum(FigureEnum), nullable=True)
    bounds: Mapped[dict] = Column(JSONB, nullable=True)
    latlngs: Mapped[dict] = Column(JSONB, nullable=True)
    radius: Mapped[float] = Column(Float, nullable=True)
    radius_color: Mapped[str] = Column(String(255), nullable=True)
    map_level = relationship(MapLevel, back_populates="figures", uselist=False)
