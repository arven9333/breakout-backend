from datetime import datetime

import logging
from _logging.base import setup_logging

from repositories.base import SQLAlchemyRepo
from models.user import UserLogs

logger = logging.getLogger(__name__)
setup_logging(__name__)


class UserLogsRepository(SQLAlchemyRepo):
    async def add_log(
            self,
            ip_address: str,
            request_time: datetime,
            endpoint_name: str,
            request_dict: dict | None = None,
            response_dict: dict | None = None,
            user_id: int | None = 0,
    ):
        user_log = UserLogs(
            user_id=user_id,
            ip_address=ip_address,
            request_time=request_time,
            endpoint_name=endpoint_name,
            json_request=request_dict,
            json_response=response_dict,
        )

        async with self.session as session:

            await session.add(user_log)
            await session.flush()
