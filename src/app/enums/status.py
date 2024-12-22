from enum import Enum


class InvitationStatusEnum(str, Enum):
    waiting = "waiting"
    accepted = "accepted"
    canceled = "canceled"
