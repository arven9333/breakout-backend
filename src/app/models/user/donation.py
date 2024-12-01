from __future__ import annotations

from models.base import BaseModel, Column
from models.common.ts_mixin import TsMixin
from sqlalchemy import String, BigInteger, Integer, Float, UniqueConstraint
from sqlalchemy.orm import Mapped


class UserDonation(BaseModel, TsMixin):
    __tablename__ = "donations"
    __table_args__ = (
        UniqueConstraint('name', name='user_donations_name_unique'),
        {'extend_existing': True},
    )

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False,
                             comment='user donation id')

    name: Mapped[str] = Column(
        String,
        nullable=False,
        init=False,
    )
    order: Mapped[int] = Column(
        Integer,
        nullable=True,
        init=False,
    )
    total_amount: Mapped[float] = Column(
        Float,
        nullable=False,
        init=False,
        default=0,
        server_default="0"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return (
            f"UserDonation(id={self.id},name={self.name},total_amount={self.total_amount}"
        )
