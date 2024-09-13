from __future__ import annotations

from models.base import BaseModel, Column
from models.common.base import CascadeForeignKey

from sqlalchemy import BigInteger, String, Float
from sqlalchemy.orm import Mapped, relationship


class IconCategory(BaseModel):
    __tablename__ = 'icon_category'

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    name: Mapped[str] = Column(String(255), unique=True)


class Icon(BaseModel):
    __tablename__ = "icons"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    name: Mapped[str] = Column(String(255))
    image: Mapped[str] = Column(String(777))
    category_id: Mapped[int] = Column(BigInteger, CascadeForeignKey(IconCategory.id))


class IconAbstract(BigInteger):
    __abstract__ = True

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False)
    coord_x: Mapped[float] = Column(Float)
    coord_y: Mapped[float] = Column(Float)


class IconMetricLevel(IconAbstract):
    __tablename__ = "icon_metric_level"

    map_level_id: Mapped[int] = Column(BigInteger, CascadeForeignKey("MapLevel.id"))
    map_level = relationship("MapLevel", back_populates="metrics")


class IconMetricLayer(IconAbstract):
    __tablename__ = "icon_metric_layer"

    map_layer_id: Mapped[int] = Column(BigInteger, CascadeForeignKey("MapLayer.id"))
    map_layer = relationship("MapLevel", back_populates="metrics")
