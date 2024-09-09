import enum


class ConnectorsName(str, enum.Enum):
    master_async_engine = "master_async_engine"
    master_async_session_maker = "master_async_session_maker"
    slave_async_session_maker = "slave_async_session_maker"
    redis_pool = "redis_pool"
