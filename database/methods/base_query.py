class BaseQuery:
    __slots__ = ('_table_name', '_distinct', '_limit', '_order', '_where', '_items', '_query_params')

    def __init__(self, table_name=None, distinct=False, limit=None, order=None, where=None, items=None):
        self._table_name = table_name
        self._distinct = distinct
        self._limit = limit
        self._order = order
        self._where = where
        self._items = items

        self._query_params = ()

    @property
    def build(self):
        return None

    def __str__(self):
        return self.build[0]

    def _append_where(self, query):
        query += " WHERE "
        where_clause = []
        for key, val in self._where.items():
            where_clause.append(f"`{key}` = %s")
            self._query_params += (val,)
        query += ' AND '.join(where_clause)

        return query
