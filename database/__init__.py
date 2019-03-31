from database.constants import Constants, DBFunction
import database.methods as query


class Methods:
    @staticmethod
    def select(table_name, distinct=False, limit=None, order=None, where=None, items=None):
        return query.Select(table_name, distinct=distinct, limit=limit, order=order, where=where, items=items)

    @staticmethod
    def insert(table_name, **kwargs):
        return query.Insert(table_name=table_name, items=kwargs)

    @staticmethod
    def update(table_name, items=None, where=None):
        return query.Update(table_name=table_name, items=items, where=where)

    @staticmethod
    def delete(table_name, where=None):
        return query.Delete(table_name=table_name, where=where)
