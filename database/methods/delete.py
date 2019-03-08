from .base_query import BaseQuery
from database import Constants, DBFunction


class Delete(BaseQuery):
    def __init__(self, table_name, where=None):
        super().__init__(table_name=table_name, where=where)

    def where(self, *args, **kwargs):
        self._where = args, kwargs
        return self

    @property
    def build(self):
        query = Constants.Templates.DELETE.format(table=self._table_name)
        query_params = ()

        if self.where:
            where_query, where_query_params = self._build_where()
            query += where_query
            query_params = where_query_params

        return query, query_params
