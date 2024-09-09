from exceptions.base import AppException


class JWTDecodeError(AppException):
    ...


class InvalidTokenError(AppException):
    ...


class InvalidTokenData(AppException):
    ...


class NoAuthToken(AppException):
    ...


class AuthenticationError(AppException):
    ...


class JWTEncodeError(AppException):
    ...
