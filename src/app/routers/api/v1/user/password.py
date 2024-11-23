from fastapi import APIRouter
from starlette import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from dependencies.user.user_service import USER_SERVICE_DEP
from dto.request.user.registration import UserUpdateDTO
from service.user.password.manager import PasswordManager

from service.user.password.recover import RecoverPasswordService

router = APIRouter()


@router.post('/password/recover/sendLink')
async def send_link(
        email: str,
        user_service: USER_SERVICE_DEP,
):
    user = await user_service.get_user_by_email(email)

    if user is None:
        raise HTTPException(status_code=404, detail="User with this email hadn't registered")

    recover = RecoverPasswordService(email)

    await recover.send_recover_url()
    return JSONResponse(status_code=200, content={
        "status": "successful",
    })


@router.post('/password/recover/verifyLink')
async def verify_link(query):
    await RecoverPasswordService.verify_user(query)

    return JSONResponse(status_code=200, content={
        "status": "successful"
    })


@router.post('/password/recover/update')
async def recover_password(
        query: str,
        new_password: str,
        user_service: USER_SERVICE_DEP,
):
    email = await RecoverPasswordService.verify_user(query)

    user = await user_service.get_user_by_email(email)

    if user is None:
        raise HTTPException(status_code=500, detail="User not found")

    hashed_password = await PasswordManager.hash_password(password=new_password)
    user_update_dto = UserUpdateDTO(password=hashed_password)

    await user_service.update_user(user_update_dto, user.id)

    return JSONResponse(status_code=200, content={
        "status": "successful",
    })
