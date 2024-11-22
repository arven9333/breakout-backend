from fastapi import HTTPException

from service.redis.base import Redis
from utils.mail import send_email

from service.user.password.manager import PasswordManager


class RecoverPasswordService:
    def __init__(self, email):
        self.email = email

    async def send_recover_url(self):
        link, uid = PasswordManager.generate_link_recover()

        await Redis.save(str(uid), self.email, 60 * 60 * 24)

        body_email = {
            "subject": f"We received a request to reset the password for the ArenaBreakout account associated with {self.email}",
            "message": f'<a href="{link}">Reset your password</a>. Link will be active for 24 hours',
            "recipient": self.email
        }
        try:
            send_email(**body_email)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unable to send message on email. Error: {str(e)}")

    @staticmethod
    async def verify_user(uid):
        user_mail = await Redis.get(uid)

        if user_mail is None:
            raise HTTPException(status_code=404, detail="Link not found (expired or wrong)")

        return user_mail
