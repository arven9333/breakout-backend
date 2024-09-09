from typing import Optional
import logging
from _logging.base import setup_logging

from dto.response.auth import AuthToken
from .auth_abc import AuthServiceABC
from .create_token import CreateToken
from exceptions.auth import NoAuthToken
from .verify import VerifyToken

logger = logging.getLogger(__name__)
setup_logging(__name__)


class AuthService(AuthServiceABC):
    def __init__(
            self,
            jwt_pub_key: str,
            jwt_pri_key: str,
    ):
        self.jwt_pub_key = jwt_pub_key
        self.jwt_pri_key = jwt_pri_key

    def verify_auth_token(
            self,
            authorization_token: str,
    ) -> Optional[AuthToken]:
        if not authorization_token:
            raise NoAuthToken(details="No auth token")
        return VerifyToken(jwt_pub_key=self.jwt_pub_key, jwt_pri_key=self.jwt_pri_key)(
            authorization_token
        )

    def create_jwt_token(self, user_id: int, email: str) -> str:
        return CreateToken(jwt_pub_key=self.jwt_pub_key, jwt_pri_key=self.jwt_pri_key)(
            user_id, email
        )
