from __future__ import annotations
import datetime

from enums.invitation import InvitationTypeEnum
from enums.status import InvitationStatusEnum
from models.base import BaseModel, Column
from models.user.base import User
from models.common.ts_mixin import TsMixin
from sqlalchemy import BigInteger, String, UniqueConstraint, Boolean, Text, Integer, ForeignKey, DateTime, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship


class Invitation(BaseModel, TsMixin):
    __tablename__ = "user_invitations"
    __table_args__ = (
        UniqueConstraint(*("from_user_id", "to_user_id", "status"), name='user_invitations_unique'),
        {'extend_existing': True}
    )

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False,
                             comment='invitation id')
    from_user_id = Column(BigInteger, ForeignKey(User.id, ondelete="CASCADE"))
    to_user_id = Column(BigInteger, ForeignKey(User.id, ondelete="CASCADE"))
    text = Column(Text, nullable=True)
    alias = Column(String(127), default=InvitationTypeEnum.party, server_default=InvitationTypeEnum.party,
                   nullable=False, init=False)
    status = Column(String(127), default=InvitationStatusEnum.waiting, server_default=InvitationStatusEnum.waiting,
                    nullable=False, init=False)
    from_user = relationship(User, foreign_keys=[from_user_id], uselist=False)
    to_user = relationship(User, foreign_keys=[to_user_id], uselist=False)


class UserParty(BaseModel, TsMixin):
    __tablename__ = "user_parties"
    __table_args__ = (
        UniqueConstraint(*("from_user_id", "to_user_id", "invitation_id"), name='user_parties_unique'),
        {'extend_existing': True}
    )

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False,
                             comment='party id')
    from_user_id = Column(BigInteger, ForeignKey(User.id, ondelete="CASCADE"))
    to_user_id = Column(BigInteger, ForeignKey(User.id, ondelete="CASCADE"))
    invitation_id = Column(BigInteger, ForeignKey(Invitation.id, ondelete="CASCADE"))
    last_seen_from_user: Mapped[datetime.datetime] = Column(
        TIMESTAMP(timezone=False),
        nullable=True,
        default=None,
        comment="Дата и время прочтения чата пользователем отправителя"
    )
    last_seen_to_user: Mapped[datetime.datetime] = Column(
        TIMESTAMP(timezone=False),
        nullable=True,
        default=None,
        comment="Дата и время чата пользователем получателя"
    )
    from_user = relationship(User, foreign_keys=[from_user_id], uselist=False)
    to_user = relationship(User, foreign_keys=[to_user_id], uselist=False)
    invitation = relationship(Invitation, uselist=False)
    last_message = relationship(
        "UserMessages",
        uselist=False,
        back_populates="user_party",
        order_by="UserMessages.ts_create.desc()"
    )


class UserMessages(BaseModel, TsMixin):
    __tablename__ = "user_messages"
    __table_args__ = (
        UniqueConstraint(*("from_user_id", "to_user_id", "user_party_id", "ts_create"), name='user_mes_unique'),
        {'extend_existing': True}
    )

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True, init=False, nullable=False,
                             comment='user id')
    from_user_id = Column(BigInteger, ForeignKey(User.id, ondelete="CASCADE"))
    to_user_id = Column(BigInteger, ForeignKey(User.id, ondelete="CASCADE"))
    user_party_id = Column(BigInteger, ForeignKey(UserParty.id, ondelete="CASCADE"))
    text = Column(Text)
    from_user = relationship(User, foreign_keys=[from_user_id], uselist=False)
    to_user = relationship(User, foreign_keys=[to_user_id], uselist=False)
    user_party = relationship(UserParty, uselist=False, back_populates="last_message")
