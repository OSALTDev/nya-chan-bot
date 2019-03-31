class BaseQuery:
    __slots__ = ('_table_name', '_distinct', '_limit', '_order', '_where', '_items', '_query_params', '_appended',
                 '_duplicate_key_update_action')

    def __init__(self, table_name=None, distinct=False, appended_sql=None, limit=None, order=None, where=None,
                 items=None, or_update=None):
        self._table_name = table_name
        self._distinct = distinct
        self._limit = limit
        self._order = order
        self._where = where
        self._items = items
        self._appended = appended_sql
        self._duplicate_key_update_action = or_update
        self._query_params = ()

    def run(self, cursor):
        return cursor.execute(*self.build)

    @property
    def build(self):
        return None, None

    def __str__(self):
        return self.build[0]

    def _build_where(self):
        where_query = " WHERE "
        where_clause = []
        param_tuple = ()

        where_dict = self._where[1]
        if self._where[0] and isinstance(self._where[0], dict):
            where_dict.update(self._where[0])
        for key, val in where_dict.items():
            if isinstance(key, tuple):
                if not isinstance(val, tuple):
                    raise ValueError("Value must be a tuple for composite key where clause")

                where_clause.append(f"(`{'`, `'.join(key)}`) = ({', '.join(('%s',) * len(val))})")
                param_tuple += val
            else:
                where_clause.append(f"`{key}` = %s")
                param_tuple += (val,)
        where_query += ' AND '.join(where_clause)

        return where_query, param_tuple
