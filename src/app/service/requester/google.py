from dataclasses import dataclass
from service.requester.base import Requestor


@dataclass
class GoogleTokenRequestor(Requestor):
    url: str = 'https://oauth2.googleapis.com/token'
    method: str = "post"
