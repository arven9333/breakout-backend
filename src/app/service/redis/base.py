import json
from redis import asyncio as aioredis

from settings import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_conn = aioredis.from_url(
    f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
    decode_responses=True
)


class Redis:

    @staticmethod
    async def delete(key):
        async with redis_conn.client() as conn:
            check = await conn.exists(key)
            if check:
                await conn.delete(key)

    @staticmethod
    async def save(key, values, time_expired):
        async with redis_conn.client() as conn:
            data = json.dumps(values) if isinstance(values, (dict, list, tuple)) else values
            await conn.set(key, data)
            await conn.expire(key, time_expired)

    @staticmethod
    async def get(key):
        async with redis_conn.client() as conn:
            data = await conn.get(key)
            return data