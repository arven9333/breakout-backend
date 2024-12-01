from fastapi import APIRouter, Depends

from dependencies.user.auth import USER_ID_DEP
from dependencies.user.roles import ADMIN_ROLE_DEP
from dependencies.user.user_service import USER_SERVICE_DEP
from dependencies.user.donation import USER_DONATION_SERVICE_DEP

from scheme.request.user.base import UserCreateSchema
from scheme.request.user.donation import UserDonationUpdateScheme, UserDonationAddScheme
from scheme.response.user.base import UserGetSchema
from scheme.response.user.donation import UserDonationListResponseScheme, UserDonationScheme

router = APIRouter(tags=["user.v1.donation"], prefix="/donation")


@router.get('/list', response_model=UserDonationListResponseScheme)
async def _get_user_donation_list(
        user_donation_service: USER_DONATION_SERVICE_DEP,
):
    user_donation_dtos = await user_donation_service.get_user_donations_list()
    return {
        "user_donations": user_donation_dtos
    }


@router.post('/create', response_model=UserDonationScheme, dependencies=[ADMIN_ROLE_DEP])
async def _create_user_donation(
        user_id: USER_ID_DEP,
        user_donation_create_scheme: UserDonationAddScheme,
        user_donation_service: USER_DONATION_SERVICE_DEP,
):
    user_donation = await user_donation_service.add_user_donation(user_donation_create_scheme.as_dataclass())
    return user_donation


@router.patch("/update", response_model=UserDonationListResponseScheme, dependencies=[ADMIN_ROLE_DEP])
async def _update_user_donation(
        user_id: USER_ID_DEP,
        user_donation_service: USER_DONATION_SERVICE_DEP,
        user_donations_update_scheme: list[UserDonationUpdateScheme],
):
    user_donations = await user_donation_service.update_user_donation(
        user_donation_update_dtos=[
            user_donation_scheme.as_dataclass() for user_donation_scheme in user_donations_update_scheme
        ]
    )
    return {
        "user_donations": user_donations
    }
