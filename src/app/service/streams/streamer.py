from dataclasses import dataclass

from service.requester.twitch import TwitchGetToken, TwitchStreams

from settings import (
    TWITCH_CLIENT_ID,
    TWITCH_SECRET, STREAMER_NAME
)


@dataclass
class StreamerService:

    @staticmethod
    async def get_access_token() -> str | None:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        params = {
            "client_id": TWITCH_CLIENT_ID,
            'client_secret': TWITCH_SECRET,
            "grant_type": 'client_credentials'
        }
        requestor = TwitchGetToken(params=params)
        response_token = await requestor(headers=headers)

        if access_token := response_token.get("access_token"):
            return access_token
        return

    async def get_streamer(self, streamer_name: str = STREAMER_NAME):
        access_token = await self.get_access_token()

        if access_token is not None:
            headers = {
                "Client-ID": TWITCH_CLIENT_ID,
                "Authorization": f"Bearer {access_token}"
            }
            params = {
                "user_login": streamer_name
            }

            requestor = TwitchStreams(params=params)

            response_stream = await requestor(
                headers=headers,
                params=params
            )
            if stream_data := response_stream.get("data", []):
                return stream_data
        return []

    async def is_streaming(self, streamer_name: str = STREAMER_NAME):
        stream_data = await self.get_streamer(streamer_name)
        if not len(stream_data):
            return False
        return True
