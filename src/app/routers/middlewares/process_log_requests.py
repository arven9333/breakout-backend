import json
import logging

from starlette.status import HTTP_204_NO_CONTENT

from _logging.base import setup_logging

from typing import Callable, Awaitable
from fastapi import FastAPI, Request, Response

from starlette.responses import StreamingResponse
from starlette.concurrency import iterate_in_threadpool

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from connectors.connectors_name import ConnectorsName

from service.user.auth.main import AuthService
from exceptions.auth import (
    JWTDecodeError,
    InvalidTokenData,
    AuthenticationError,
    NoAuthToken,
)

from repositories.user.user_logs import UserLogsRepository

from settings import settings

logger = logging.getLogger(__name__)
setup_logging(__name__)


class LoggingRoute:
    def __init__(self) -> None:
        self.auth_service = AuthService(
            jwt_pub_key=settings.JWT_SECRET_KEY,
            jwt_pri_key=settings.JWT_SECRET_KEY,
        )
        self.connector_name: str = ConnectorsName.master_async_session_maker

    async def set_request_body(self, request: Request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive

    def can_logs_request(self, request: Request, response: Response | None = None) -> bool:
        if not request.url.path.startswith("/api"):
            logger.debug(f"Can't log because {request.url.path} not start with /api")
            return False
        if request.headers.get("content-type", "").startswith("multipart/form-data"):
            logger.debug(f"Can't log because request is 'multipart/form-data'")
            return False
        if response and response.headers.get("content-type") != "application/json":
            logger.debug(f"Can't log because response is not json '{response.headers.get('content-type')}'")
            return False

        return True

    async def __call__(
            self,
            request: Request,
            call_next: Callable[[Request], Awaitable[StreamingResponse]],
    ) -> Response:
        if self.can_logs_request(request):
            await self.set_request_body(request)

        try:
            response = await call_next(request)
        except RuntimeError as exc:
            if str(exc) == 'No response returned.' and await request.is_disconnected():
                return Response(status_code=HTTP_204_NO_CONTENT)
            raise

        if not self.can_logs_request(request, response):
            return response

        response_body = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))

        request_body = await self.get_request_log(request)
        logger.debug(f"request_body={request_body}")

        try:
            response_item: dict = json.loads(response_body[0].decode())
        except json.decoder.JSONDecodeError:
            response_item = {}

        logger.debug(f"response_body={response_item}")

        user_id = self.get_user_id_from_jwt_or_response(request, response_item)

        app: FastAPI = request.app

        session_maker: async_sessionmaker[AsyncSession] = getattr(
            app.state,
            self.connector_name
        )
        async with session_maker() as session:
            user_logs_repository = UserLogsRepository(session)
            await user_logs_repository.add_log(
                endpoint_name=request_body.get("path", ""),
                ip_address=request_body.get("ip", "0.0.0.0"),
                request_time=datetime.utcnow(),
                response_dict=response_item,
                request_dict=request_body.get("body", {}),
                user_id=user_id,
            )
            await session.commit()

        return response

    async def get_request_log(self, request: Request) -> dict:
        path = request.url.path

        try:
            body: dict = await request.json()
        except json.decoder.JSONDecodeError:
            body = {}

        if request.query_params:
            body.update(dict(request.query_params))

        if body and body.get('password'):
            body['password'] = '*****'

        request_dict = {
            "method": request.method,
            "path": path,
            "ip": request.headers.get("x-real-ip", "0.0.0.0"),
            "body": body,
        }

        return request_dict

    def get_user_id_from_jwt_or_response(self, request: Request, response_dict: dict) -> int | None:
        user_id = None
        try:
            auth_data = self.auth_service.verify_auth_token(
                authorization_token=request.headers.get("authorization", ""),
            )
            if auth_data:
                user_id = auth_data.user_id
        except (
                NoAuthToken,
                JWTDecodeError,
                InvalidTokenData,
                AuthenticationError,
        ) as exc:
            logger.error("Auth error: %s", exc)

        url_path = request.url.path
        if not user_id and (url_path.endswith('login') or url_path.endswith('service')):
            user_id = response_dict.get("item", {}).get("id", 0)

        return user_id
