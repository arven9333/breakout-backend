from abc import ABC
from typing import ClassVar, Optional

from dto.response.auth import AuthToken


class AuthBaseUseCase:
    algorithms: ClassVar[list[str]] = ["RS256", "HS256"]
    encode_algorithm_rs: ClassVar[str] = "RS256"
    encode_algorithm_hs: ClassVar[str] = "HS256"

    def __init__(self,
                 jwt_pub_key: str,
                 jwt_pri_key: str | None = None,
                 ):
        self.jwt_pub_key = jwt_pub_key
        self.jwt_pri_key = jwt_pri_key
        if jwt_pub_key == jwt_pri_key or not jwt_pri_key:
            self.algorithm = self.encode_algorithm_hs
        else:
            self.algorithm = self.encode_algorithm_rs


class AuthServiceABC(ABC):
    def verify_auth_token(self, authorization_token: str) -> Optional[AuthToken]:
        ...

    def create_jwt_token(self, user_id: int, email: str) -> str:
        ...
