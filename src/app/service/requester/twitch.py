from dataclasses import dataclass
from service.requester.base import Requestor


@dataclass
class TwitchGetToken(Requestor):
    url: str = 'https://id.twitch.tv/oauth2/token'
    method: str = "post"


@dataclass
class TwitchGetUser(Requestor):
    url: str = 'https://api.twitch.tv/helix/users'
    method: str = "get"


@dataclass
class TwitchRevokeToken(Requestor):
    url: str = 'https://id.twitch.tv/oauth2/revoke'
    method: str = "post"


@dataclass
class TwitchStreams(Requestor):
    url: str = "https://api.twitch.tv/helix/streams"
    method: str = "get"
