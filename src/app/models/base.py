from sqlalchemy import MetaData
from sqlalchemy.orm import mapped_column, MappedAsDataclass, DeclarativeBase

Column = mapped_column

metadata = MetaData()


class BaseModel(DeclarativeBase, MappedAsDataclass):
    __table_args__ = {'extend_existing': True}

