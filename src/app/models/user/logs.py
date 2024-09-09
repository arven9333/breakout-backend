from datetime import datetime

from sqlalchemy import (
    String,
    BigInteger,
    TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import Mapped

from models.base import BaseModel, Column
from models.common.base import CascadeForeignKey
from models.user.base import User


class UserLogs(BaseModel):
    __tablename__ = "logs"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment="id лога")
    ip_address: Mapped[str] = Column(INET, nullable=False, comment="ip адрес")

    user_id: Mapped[int] = Column(
        BigInteger,
        CascadeForeignKey(User.id),
        nullable=False,
        default=0,
        server_default="0",
    )

    request_time: Mapped[datetime] = Column(
        TIMESTAMP(timezone=False),
        nullable=False,
        default=datetime.utcnow(),
        comment="Дата и время запроса",
    )

    endpoint_name: Mapped[str] = Column(
        String,
        nullable=False,
        default="",
        comment="Название запроса",
    )
    json_request: Mapped[dict] = Column(
        JSONB,
        nullable=False,
        default_factory=dict,
        server_default="{}",
        comment="json запроса",
    )
    json_response: Mapped[dict] = Column(
        JSONB,
        nullable=False,
        default_factory=dict,
        server_default="{}",
        comment="json ответа",
    )

    def __repr__(self):
        return (
            f"UserLogs(id={self.id},ip_address={self.ip_address},user_id={self.user_id},"
            f"request_time={self.request_time},endpoint_name={self.endpoint_name},"
            f"json_request={self.json_request},json_response={self.json_response})"
        )
