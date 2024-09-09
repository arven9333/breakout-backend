from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from connectors.database import DatabaseConnector
from sqlalchemy.ext.asyncio import async_sessionmaker

from dependencies.common import get_settings
from settings import Settings


class DatabaseDep:
    def __init__(self):
        settings: Settings = get_settings()
        db_connector = DatabaseConnector(settings)
        self._master_session_maker = db_connector.master_session

    def get_master_session_maker(self) -> async_sessionmaker[AsyncSession]:
        return self._master_session_maker


database_dep = DatabaseDep()
MasterSessionMakerDep = Annotated[
    async_sessionmaker[AsyncSession],
    Depends(database_dep.get_master_session_maker),
]
