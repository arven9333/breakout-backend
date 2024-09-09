from dataclasses import dataclass
from dataclasses import field


@dataclass
class AuthToken:
    sub: str
    user_id: int | None = field(metadata={"user_id": "User id"})
    exp: int = field(metadata={"exp": "expiration time, timestamp"})
    iat: int = field(metadata={"iat": "момент, когда токен был создан timestamp"})