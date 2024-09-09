import datetime

import jwt
import logging
from _logging.base import setup_logging

from .auth_abc import AuthBaseUseCase
from .constants import USER_ID_KEY, EXPIRATION_INTERVAL
from exceptions.auth import JWTEncodeError

logger = logging.getLogger(__name__)
setup_logging(__name__)


class CreateToken(AuthBaseUseCase):
    def __call__(self, user_id: int, email: str) -> str:
        payload = {
            USER_ID_KEY: str(user_id),
            "email": email,
            'exp': (datetime.datetime.utcnow() + datetime.timedelta(days=EXPIRATION_INTERVAL)).timestamp(),
        }

        try:
            token = jwt.encode(payload,
                               self.jwt_pri_key or self.jwt_pub_key,
                               algorithm=self.algorithm
                               )
        except ValueError as exc:
            logger.error("Encode error... %s", exc)
            raise JWTEncodeError(details="Can not create jwt token") from exc
        return token
