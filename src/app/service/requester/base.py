from dataclasses import dataclass
from typing import Optional
from _logging.base import setup_logging

import logging

import aiohttp


logger = logging.getLogger(__name__)
setup_logging(__name__)


@dataclass(kw_only=True)
class Requestor:
    url: str
    method: str = 'get'
    params: Optional[dict | str] = None
    session: Optional[aiohttp.ClientSession] = None
    auto_close_session: bool = True
    is_graphql: bool = False

    async def __call__(self, *args, **kwargs):
        extra_headers = kwargs.get("headers", {})
        if self.session is None:
            if kwargs.get("is_json") is True:
                extra_headers |= {"Content-Type": "application/json; charset=utf-8"}
            self.session = aiohttp.ClientSession(headers=extra_headers)

        if self.method == 'get':
            params = {"params": self.params}
        elif self.is_graphql is True:
            params = {"json": {"query": self.params}}
        else:
            params = {"data": self.params} if self.params else {}

        method = getattr(self.session, self.method, self.session.get)

        async with method(url=self.url, **params) as response:

            if response.status != 200:
                logger.error(
                    f'Response error with status '
                    f'{response.status}, {response.text}'
                )

            try:
                return await response.json()
            except:
                return await response.text()
            finally:
                if self.auto_close_session:
                    await self.session.close()
