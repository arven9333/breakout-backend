from passlib.hash import bcrypt
from uuid import uuid4
from settings import FRONT_FORGET_PASSWORD_URL


class PasswordManager:
    @staticmethod
    async def hash_password(password: str) -> str:
        hashed_password = bcrypt.hash(password)
        return hashed_password

    @staticmethod
    async def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.verify(password, hashed_password)

    @staticmethod
    def generate_link_recover() -> tuple:
        data = uuid4()

        return f"{FRONT_FORGET_PASSWORD_URL}?query={data}", data