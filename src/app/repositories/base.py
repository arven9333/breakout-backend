from types import TracebackType
from typing import Optional, Type, Any

from sqlalchemy import func, select
from sqlalchemy.sql.selectable import Select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class SQLAlchemyManager:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.__session = session

    @property
    def session(self):
        return self.__session

    async def __aenter__(self):
        self.master_session = self.session()
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]] = None,
            exc_value: Optional[BaseException] = None,
            traceback: Optional[TracebackType] = None,
    ) -> None:
        if exc_value:
            await self.rollback()
        else:
            await self.commit()

        await self.master_session.close()

    async def commit(self):
        await self.master_session.commit()

    async def rollback(self):
        await self.master_session.rollback()

    async def flush(self, *args, **kwargs):
        await self.master_session.flush(*args, **kwargs)

    async def execute(self, *args, **kwargs):
        return await self.master_session.execute(*args, **kwargs)

    async def add(self, *args, **kwargs):
        self.master_session.add(*args, **kwargs)


class SQLAlchemyRepo:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session: SQLAlchemyManager = SQLAlchemyManager(
            session=session
        )

    @staticmethod
    async def get_count_from_query(query: Select) -> Select[Any]:
        stmt = select(
            func.count(1)
        ).select_from(
            query.subquery()
        )
        return stmt
