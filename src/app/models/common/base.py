from sqlalchemy import ForeignKey


class RestrictForeignKey(ForeignKey):
    def __init__(self, column, **dialect_kw):
        super().__init__(column, ondelete='RESTRICT', onupdate='RESTRICT', **dialect_kw)


class CascadeForeignKey(ForeignKey):
    def __init__(self, column, **dialect_kw):
        super().__init__(column, ondelete='CASCADE', onupdate='CASCADE', **dialect_kw)
