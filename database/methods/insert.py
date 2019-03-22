from .base_query import BaseQuery
from database import Constants, DBFunction


class Insert(BaseQuery):
    def __init__(self, table_name, items=None):
        super().__init__(table_name=table_name, items=items)
        if self._items:
            self.items(**self._items)

    def items(self, **kwargs):
        keys = kwargs.keys()
        values = kwargs.values()

        self._items = {"items": '`, `'.join(f"{key}" for key in keys)}
        # Append as many VALUES (?,?,?) as we need
        values_str = ""
        for value in values:
            if isinstance(value, DBFunction):
                values_str += f"{value.val}, "
                continue

            values_str += "%s, "
            self._query_params += (value,)
        self._items["values"] = f"{values_str[:-2]}"

        return self

    @property
    def build(self):
        query = Constants.Templates.INSERT

        query, query_data = query.format(table=self._table_name, **self._items), ()

        return query, self._query_params + query_data
