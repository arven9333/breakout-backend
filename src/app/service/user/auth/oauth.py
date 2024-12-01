from dataclasses import dataclass
from urllib import parse

from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest

from dto.request.user.registration import UserCreateDTO
from service.requester.google import GoogleTokenRequestor
from service.requester.twitch import TwitchGetUser, TwitchRevokeToken
from service.user.auth.main import AuthService
from service.user.service.main import UserService
from settings import (
    TWITCH_CLIENT_ID,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URL,
)


@dataclass
class OauthService:
    user_service: UserService
    auth_service: AuthService

    @staticmethod
    async def revoke_twitch_token(access_token: str):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        params = {
            "client_id": TWITCH_CLIENT_ID,
            "token": access_token
        }
        params = parse.urlencode(params)
        requestor = TwitchRevokeToken(params=params)
        try:
            await requestor(headers=headers)
        except:
            pass  #если не удалить токен, возможны колизии на стороне твича

    @staticmethod
    async def validate_user(user_data: dict):
        data = user_data.get("data", [])
        if len(data) == 1 and data[0].get("id") is not None:
            return True
        return False

    async def get_twitch_user(self, access_token: str, token_type: str = 'bearer'):
        requestor = TwitchGetUser()

        headers = {
            'Authorization': f'{token_type} {access_token}',
            'Client-Id': TWITCH_CLIENT_ID,
        }
        user_data = await requestor(headers=headers)

        is_valid_user = await self.validate_user(user_data)

        if is_valid_user:
            await self.revoke_twitch_token(access_token)
            return {
                "user": user_data["data"][0],
            }
        return {
            "error": user_data.get("error", "Не удалось авторизоваться"),
        }

    async def get_token_from_twitch_callback(self, access_token: str, token_type: str = 'bearer'):
        twitch_user_response = await self.get_twitch_user(access_token, token_type)
        if twitch_user := twitch_user_response.get("user"):
            external_id = int(twitch_user.get("id", 0))
            user = await self.user_service.get_user_by_external_id(external_id)

            if user is None:
                username_exists = await self.user_service.get_user_by_username(twitch_user.get("login"))
                if username_exists:
                    username = twitch_user.get("login", "") + "_" + str(external_id)
                else:
                    username = twitch_user.get("login", "")

                user = await self.user_service.create_user(
                    UserCreateDTO(
                        email=None,
                        username=username,
                        password='',
                        verified_password='',
                        external_id=external_id,
                    )
                )
            token = self.auth_service.create_jwt_token(user.id, user.username)

            return {
                "token": token,
            }
        return {
            "token_error": twitch_user_response.get("error"),
        }

    @staticmethod
    async def get_google_token(code: str):
        data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': GOOGLE_REDIRECT_URL,
            'grant_type': 'authorization_code',
        }
        requestor = GoogleTokenRequestor(params=data)
        response = await requestor()
        return response.get('id_token')

    async def get_user_google(self, code: str):
        id_token_value = await self.get_google_token(code)
        if id_token_value:
            try:
                google_user = {
                    "user": id_token.verify_oauth2_token(
                        id_token=id_token_value,
                        request=GoogleRequest(),
                        audience=GOOGLE_CLIENT_ID,
                    )
                }
            except ValueError as e:
                google_user = {
                    "error": f"Invalid id_token: {str(e)}"
                }

            return google_user
        return {
            "error": "Missing id_token in response."
        }

    async def get_token_from_google_callback(self, code: str):
        google_user_response = await self.get_user_google(code)

        if google_user := google_user_response.get("user"):
            email = google_user.get("email")
            user = await self.user_service.get_user_by_email(email)
            if user is None:
                username = email.split('@')[0]

                username_exists = await self.user_service.get_user_by_username(username)
                if username_exists:
                    username = username + "_" + str(google_user.get("at_hash"))

                user_create_dto = UserCreateDTO(
                    email=google_user.get("email"),
                    username=username,
                    password="",
                    verified_password="",
                )
                user = await self.user_service.create_user(user_create_dto)
            token = self.auth_service.create_jwt_token(user.id, user.username)

            return {
                "token": token,
            }
        return {
            "token_error": google_user_response.get("error"),
        }
