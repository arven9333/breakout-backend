import collections.abc
from typing import Mapping

from dto.response.base import ErrorBaseDto


class AppException(Exception):
    def __init__(self, error: Exception | int = None, details: str | Mapping | ErrorBaseDto = None):
        self.error = error
        self._response = details
        if isinstance(details, collections.abc.Mapping):
            try:
                params = details.get("params", None)
                if hasattr(params, 'dict'):
                    params = params.dict()
                self._response = ErrorBaseDto(
                    error_fields=details.get("error_fields", None),
                    success=details.get("success", 0),
                    error=details.get("error", error),
                    params=params,
                )
            except AttributeError:
                self._response = details

    @property
    def response(self):
        return self._response

    def __repr__(self):
        return f"error={self.error} response={self.response}"

    def __str__(self):
        return self.__repr__()


class DomainException(AppException):
    """Base Domain Exception"""


class NotAuthorized(AppException):
    """Not authorized"""
