from typing import Optional

from fastapi import APIRouter, Depends
from starlette.requests import Request

from dependencies.user.auth import USER_ID_DEP
from dependencies.user.user_service import USER_SERVICE_DEP
from dependencies.user.party import USER_PARTY_SERVICE_DEP
from dto.request.user.party import InvitationAddDTO, UserMessageAddDTO
from enums.invitation import InvitationTypeEnum
from enums.status import InvitationStatusEnum
from scheme.response.user.base import UserInvitationResponseScheme, UserInvitationScheme

from scheme.response.user.party import UserMessageResponseScheme, UserPartyResponseScheme, \
    UserPartyScheme, UserMessageScheme

router = APIRouter(tags=["user.v1.chat"], prefix="/chat")


@router.get('/invitations', response_model=UserInvitationResponseScheme)
async def _get_user_invitations(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        user_party_service: USER_PARTY_SERVICE_DEP,
        is_user_sent: bool = False,
        limit: int = 100,
        offset: int = 0,
):
    user_invitations_dto, pagination = await user_party_service.get_user_invitations(user_id, is_user_sent, limit,
                                                                                     offset)
    return {
        "list": user_invitations_dto,
        "total": pagination.total,
        "offset": pagination.offset,
        "limit": pagination.limit,
    }


@router.get('/parties', response_model=UserPartyResponseScheme)
async def _get_user_parties(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        user_party_service: USER_PARTY_SERVICE_DEP,
        limit: int = 100,
        offset: int = 0,
):
    user_parties_dto, pagination = await user_party_service.get_user_parties(user_id, limit, offset)
    return {
        "list": user_parties_dto,
        "total": pagination.total,
        "offset": pagination.offset,
        "limit": pagination.limit,
    }


@router.get('/messages', response_model=UserMessageResponseScheme)
async def _get_user_messages(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        user_party_service: USER_PARTY_SERVICE_DEP,
        party_id: int,
        limit: int = 100,
        offset: int = 0,
):
    has_party = await user_party_service.get_party_by_id(party_id, need_exception=True)
    user_messages, pagination = await user_party_service.get_user_messages(party_id, limit, offset)
    return {
        "list": user_messages,
        "total": pagination.total,
        "offset": pagination.offset,
        "limit": pagination.limit,
    }


@router.post('/messages/read', response_model=UserPartyScheme)
async def _read_user_message(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        user_party_service: USER_PARTY_SERVICE_DEP,
        party_id: int,
):
    has_party = await user_party_service.get_party_by_id(party_id, need_exception=True)
    party_dto = await user_party_service.read_message(party_id, user_id)

    return party_dto


@router.post('/invitations/accept', response_model=UserInvitationScheme)
async def _accept_invitation(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        user_party_service: USER_PARTY_SERVICE_DEP,
        invitation_id: int
):
    has_invitation = await user_party_service.get_invitation_by_id(invitation_id, need_exception=True)
    invitation_dto = await user_party_service.accept_invitation(invitation_id, user_id)

    return invitation_dto


@router.post('/invitations/cancel', response_model=UserInvitationScheme)
async def _cancel_invitation(
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        user_party_service: USER_PARTY_SERVICE_DEP,
        invitation_id: int
):
    has_invitation = await user_party_service.get_invitation_by_id(invitation_id, need_exception=True)
    invitation_dto = await user_party_service.cancel_invitation(invitation_id)

    return invitation_dto


@router.post('/invitations/create', response_model=UserInvitationScheme)
async def _create_invitation(
        user_id: USER_ID_DEP,
        text: str | None,
        to_user_id: int,
        user_service: USER_SERVICE_DEP,
        user_party_service: USER_PARTY_SERVICE_DEP,
):
    await user_party_service.invitation_exists(user_id, to_user_id)

    invitation_add_dto = InvitationAddDTO(
        from_user_id=user_id,
        to_user_id=to_user_id,
        alias=InvitationTypeEnum.party,
        status=InvitationStatusEnum.waiting,
        text=text,
    )

    invitation_dto = await user_party_service.insert_invitation(invitation_add_dto)

    return invitation_dto


@router.post("/messages/create", response_model=UserMessageScheme)
async def _create_message(
        party_id: int,
        text: str,
        user_id: USER_ID_DEP,
        user_service: USER_SERVICE_DEP,
        user_party_service: USER_PARTY_SERVICE_DEP,
):
    exists_party = await user_party_service.get_party_by_id(party_id, need_exception=True)
    if exists_party.to_user_id == user_id:
        to_user_id = exists_party.from_user_id
    else:
        to_user_id = exists_party.to_user_id

    user_message_add_dto = UserMessageAddDTO(
        from_user_id=user_id,
        to_user_id=to_user_id,
        user_party_id=party_id,
        text=text
    )
    message_dto = await user_party_service.insert_user_messages(user_message_add_dto)

    return message_dto
