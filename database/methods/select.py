from .base_query import BaseQuery
from database import Constants


class Select(BaseQuery):
    def __init__(self, table_name, distinct=False, limit=None, order=None, where=None, items=None):
        super().__init__(distinct=distinct, table_name=table_name, limit=limit, order=order, where=where, items=items)

    def items(self, *args):
        self._items = "`, `".join(args)
        return self

    def limit(self, limit):
        if not isinstance(limit, int):
            return self
        self._limit = limit
        return self

    def order(self, limit):
        token = limit[0]
        if token not in "<=>":
            return self
        self._order = (limit[1:], Constants.token_to_order.get(token, ""))
        return self

    def where(self, **kwargs):
        self._where = kwargs
        return self

    @property
    def distinct(self):
        self._distinct = not self._distinct
        return self

    @property
    def build(self):
        query = Constants.Templates.SELECT

        distinct = "DISTINCT " if self._distinct else ""
        query = query.format(distinct=distinct, table=self._table_name, item=self._items)
        if self._where:
            query = self._append_where(query)

        if self._order:
            query += f" ORDER BY {self._order[0]} {self._order[1]}"

        return query, self._query_params
