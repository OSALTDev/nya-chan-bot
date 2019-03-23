from .base_query import BaseQuery
from database import Constants, DBFunction


class Update(BaseQuery):
    def __init__(self, table_name, items=None, where=None):
        super().__init__(table_name=table_name, items=items, where=where)

    def items(self, **kwargs):
        # Append as many VALUES (?,?,?) as we need
        self._items = ""
        for key, value in kwargs.items():
            if isinstance(value, DBFunction):
                self._items += f"`{key}` = {value.val}, "
                continue

            self._items += f"`{key}` = %s, "
            self._query_params += (value,)
        self._items = self._items[:-2]
        return self

    def where(self, **kwargs):
        self._where = kwargs
        return self

    @property
    def build(self):
        if not self._where:
            return False

        query = Constants.Templates.UPDATE
        query = query.format(table=self._table_name, items=self._items)
        query = self._append_where(query)

        return query, self._query_params
