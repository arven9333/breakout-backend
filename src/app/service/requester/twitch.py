from dataclasses import dataclass
from service.requester.base import Requestor


@dataclass
class TwitchGetUser(Requestor):
    url: str = 'https://api.twitch.tv/helix/users'


@dataclass
class TwitchRevokeToken(Requestor):
    url: str = 'https://id.twitch.tv/oauth2/revoke'
    method: str = "post"
