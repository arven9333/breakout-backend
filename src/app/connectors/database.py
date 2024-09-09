import orjson
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from connectors.base import DatabaseSettings
from settings import Settings


def orjson_dumps(v, *args, **kwargs):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, *args, **kwargs).decode()


class DatabaseConnector:
    def __init__(self, settings: Settings):
        config = settings.pg_db_config
        master_db_settings = DatabaseSettings(
            driver=config.PG_MASTER_DRIVER,
            user=config.PG_MASTER_USER,
            password=config.PG_MASTER_PASSWORD,
            host=config.PG_MASTER_HOST,
            port=config.PG_MASTER_PORT,
            name=config.PG_MASTER_DB,
        )

        __master_engine = create_async_engine(
            master_db_settings.get_dsn(),
            json_serializer=orjson_dumps,
            json_deserializer=orjson.loads,
        )

        self.master_session = async_sessionmaker(__master_engine)

