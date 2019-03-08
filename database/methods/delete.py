from .base_query import BaseQuery
from database import Constants, DBFunction


class Delete(BaseQuery):
    def __init__(self, table_name, where=None):
        super().__init__(table_name=table_name, where=where)

    def where(self, **kwargs):
        self._where = kwargs
        return self

    @property
    def build(self):
        if not self._where:
            return False

        query = Constants.Templates.DELETE
        query = query.format(table=self._table_name)
        query = self._append_where(query)

        return query, self._query_params
