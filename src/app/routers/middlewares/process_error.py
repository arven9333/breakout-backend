import traceback
from typing import Callable, Awaitable

from fastapi import Request, Response
from _logging.base import setup_logging
import logging

from starlette import status
from starlette.responses import JSONResponse

from dto.response.base import ErrorBaseDto

logger = logging.getLogger(__name__)
setup_logging(__name__)


async def process_unexpected_error_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    try:
        response = await call_next(request)


    except Exception as exc:
        logger.error("process_unexpected_error_middleware: Unexpected error: %s", traceback.format_exc(limit=2))
        error = ErrorBaseDto(
            error_fields={"Unexpected error ": str(exc)},
            params={},
            success=0,
            error=500,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error.as_dict(),
        )

    return response
