import httpx
from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest
from fastapi import APIRouter
from fastapi import Request
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse
from settings import FRONT_LOGIN_PAGE
from urllib.parse import urlencode

from dependencies.user.oauth import OAUTH_SERVICE_DEP


from utils.callback_twitch_reader import get_html_for_reading_fragment

router = APIRouter(tags=["user.v1.auth"], prefix='/auth')


@router.get('/callback/twitch', response_class=HTMLResponse)
async def _callback_twitch(
        request: Request,
):
    html_redirect = get_html_for_reading_fragment(
        from_endpoint="/callback/twitch",
        to_endpoint="/callback/twitch/handle"
    )

    return HTMLResponse(content=html_redirect, status_code=200)


@router.get('/callback/twitch/handle')
async def _callback_twitch_handle(
        request: Request,
        oauth_service: OAUTH_SERVICE_DEP,
):
    quote = ""
    query_params = dict(request.query_params)

    if access_token := query_params.get("access_token"):
        token_type = query_params.get("token_type", "Bearer").title()
        authorization_query = await oauth_service.get_token_from_twitch_callback(access_token, token_type)

        quote = urlencode(authorization_query)

    redirect_url = FRONT_LOGIN_PAGE + "?" + quote

    response = RedirectResponse(redirect_url)

    response.headers["Location"] = redirect_url
    response.status_code = status.HTTP_307_TEMPORARY_REDIRECT

    return response


@router.get('/callback/google/handle')
async def _callback_google(
        code: str,
        request: Request,
        oauth_service: OAUTH_SERVICE_DEP,

):
    authorization_query = await oauth_service.get_token_from_google_callback(code)

    quote = urlencode(authorization_query)
    redirect_url = FRONT_LOGIN_PAGE + "?" + quote

    response = RedirectResponse(redirect_url)

    response.headers["Location"] = redirect_url
    response.status_code = status.HTTP_307_TEMPORARY_REDIRECT

    return response
