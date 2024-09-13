from typing import Optional

import jwt
import logging
from _logging.base import setup_logging

from .auth_abc import AuthBaseUseCase
from .constants import USER_ID_KEY
from exceptions.auth import JWTDecodeError, AuthenticationError, NoAuthToken
from dto.response.auth import AuthToken

logger = logging.getLogger(__name__)
setup_logging(__name__)


class VerifyToken(AuthBaseUseCase):
    """
    Raises:
        JWTDecodeError,
        InvalidTokenData,
        AuthenticationError
    """
    def __call__(
            self,
            authorization_token: str,
    ) -> Optional[AuthToken]:
        if not authorization_token:
            raise NoAuthToken(details="Authorisation token is absent")

        try:
            payload = jwt.decode(
                authorization_token,
                self.jwt_pub_key or self.jwt_pri_key,
                algorithms=self.algorithms,
                options={
                    "verify_signature": True,
                    "require": ["exp", "sub", ],
                }
            )
        except (ValueError,
                jwt.InvalidTokenError,
                jwt.DecodeError,
                jwt.InvalidAlgorithmError,
                jwt.InvalidSignatureError,
        ) as exc:
            logger.error("Error: %s", (exc, type(exc)))
            raise JWTDecodeError(details="Invalid Authorization token: " + str(type(exc)) + str(exc))

        try:
            auth_data = AuthToken(
                sub=payload["sub"],
                user_id=int(payload.get(USER_ID_KEY, 0)),
                exp=payload.get("exp", ""),
                iat=payload.get("iat", ""),
            )
            return auth_data
        except (ValueError, KeyError) as exc:
            logger.error("Error: %s", exc)
            raise AuthenticationError(details=f"Invalid Authorisation token payload: {str(exc)}")