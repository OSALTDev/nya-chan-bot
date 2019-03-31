from .base_query import BaseQuery
from database import Constants


class Select(BaseQuery):
    def __init__(self, table_name, distinct=False, limit=None, order=None, where=None, items=None):
        super().__init__(distinct=distinct, table_name=table_name, limit=limit, order=order, where=where, items=items)

    def items(self, *args):
        self._items = args
        return self

    def limit(self, limit):
        if not isinstance(limit, int):
            return self
        self._limit = limit
        return self

    def order(self, limit):
        self._order = limit
        return self

    def where(self, *args, **kwargs):
        self._where = args, kwargs
        return self

    @property
    def distinct(self):
        self._distinct = not self._distinct
        return self

    @property
    def build(self):
        query = Constants.Templates.SELECT
        param_tuple = ()

        distinct = "DISTINCT " if self._distinct else ""
        items = "`, `".join(self._items)
        query = query.format(distinct=distinct, table=self._table_name, item=items)

        if self._where:
            where_query, where_param_tuple = self._build_where()
            query += where_query
            param_tuple += where_param_tuple

        if self._order:
            token = self._order[0]
            if token not in "<=>":
                return self
            self._order = (self._order[1:], Constants.token_to_order.get(token, ""))
            query += f" ORDER BY {self._order[0]} {self._order[1]}"

        return query, param_tuple
