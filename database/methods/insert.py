from .base_query import BaseQuery
from database import Constants, DBFunction


class Insert(BaseQuery):
    def __init__(self, table_name, items=None):
        super().__init__(table_name=table_name, items=items)

    def items(self, **kwargs):
        self._items = kwargs.items()
        return self

    def or_update(self, **kwargs):
        self._duplicate_key_update_action = kwargs.items()
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

    def _build_update_items(self):
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
        query = Constants.Templates.INSERT

        items, values, query_params = self._build_items()
        query = query.format(table=self._table_name, items=items, values=values)

        if self._duplicate_key_update_action:
            dup_query, dup_params = self._build_update_items()
            query += " ON DUPLICATE KEY UPDATE " + dup_query
            query_params += dup_params

        return query, query_params
