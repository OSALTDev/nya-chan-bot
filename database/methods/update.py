from .base_query import BaseQuery
from database import Constants, DBFunction


class Update(BaseQuery):
    def __init__(self, table_name, items=None, where=None):
        super().__init__(table_name=table_name, items=items, where=where)

    def items(self, **kwargs):
        # Append as many VALUES (?,?,?) as we need
        self._items = kwargs.items()
        return self

    def where(self, *args, **kwargs):
        self._where = args, kwargs
        return self

    def _build_items(self):
        item_tuple = ()
        param_tuple = ()
        for key, value in self._items:
            if isinstance(value, DBFunction):
                item_tuple += (f"`{key}` = {value.val}",)
                continue

            item_tuple += (f"`{key}` = %s",)
            param_tuple += (value,)
        return ", ".join(item_tuple), param_tuple

    @property
    def build(self):
        if not self._where:
            return False

        param_tuple = ()

        query = Constants.Templates.UPDATE
        item_string, item_param_tuple = self._build_items()

        query = query.format(table=self._table_name, items=item_string)

        where_query, where_param_tuple = self._build_where()
        query += where_query

        param_tuple += item_param_tuple + where_param_tuple

        print(query, param_tuple)

        return query, param_tuple
