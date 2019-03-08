from .base_query import BaseQuery
from database import Constants, DBFunction


class Insert(BaseQuery):
    def __init__(self, table_name, items=None):
        super().__init__(table_name=table_name, items=items)

    def items(self, **kwargs):
        self._items = kwargs.items()
        return self

    def _build_items(self):
        item_tuple = ()
        value_tuple = ()
        param_tuple = ()
        # Append as many VALUES (?,?,?) as we need
        for key, value in self._items:
            item_tuple += (f"`{key}`",)

            if isinstance(value, DBFunction):
                value_tuple += (f"{value.val}",)
                continue

            value_tuple += ("%s",)
            param_tuple += (value,)

        return ", ".join(item_tuple), ", ".join(value_tuple), param_tuple

    @property
    def build(self):
        query = Constants.Templates.INSERT

        items, values, query_params = self._build_items()
        query = query.format(table=self._table_name, items=items, values=values)

        if self._appended:
            query += self._appended[0]
            query_params += self._appended[1]

        return query, query_params
