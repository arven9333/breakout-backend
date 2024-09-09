from pydantic import BaseModel
from dto.request.user.registration import UserCreateDTO


class UserCreateSchema(BaseModel):
    email: str
    username: str
    password: str
    verified_password: str

    def as_dataclass(self):
        return UserCreateDTO(
            **self.model_dump()
        )



