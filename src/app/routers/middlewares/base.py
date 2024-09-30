from uuid import uuid4
import logging
from _logging.base import setup_logging

from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from .process_error import (
    process_unexpected_error_middleware,
)
from .process_log_requests import LoggingRoute
from settings import settings

logger = logging.getLogger(__name__)
setup_logging(__name__)


def setup_middlewares(app: FastAPI, request_id_log_length: int = 6):
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex='.*',
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=['X-Request-ID']
    )

    app.add_middleware(
        CorrelationIdMiddleware,
        header_name='X-Request-ID',
        update_request_header=True,
        generator=lambda: uuid4().hex,
        validator=is_valid_uuid4,
        transformer=lambda a: str(a)[:request_id_log_length],
    )

    app.add_middleware(BaseHTTPMiddleware, dispatch=process_unexpected_error_middleware)
    if settings.ENABLE_LOG_REQUESTS:
        logger.info("Save user logs is turn on.")
        app.add_middleware(BaseHTTPMiddleware, dispatch=LoggingRoute())
    else:
        logger.info(
            "Save user logs is turn off. "
        )
