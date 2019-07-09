from bot.config import Database as DBConfig
from requests.exceptions import ConnectionError

try:
    from pyArango.connection import Connection, CreationError
    from pyArango.theExceptions import DocumentNotFoundError
except ModuleNotFoundError as e:
    raise Exception("Nya-Chan requires pyArango to be installed") from e


class Collection:
    def __init__(self, col):
        self._collection = col

    def enter(self, item, key=None):
        doc = self._collection.createDocument(item)
        doc.setPrivates({
            "_key": key
        })
        doc.save()

    def update(self, key, updates):
        doc = self._collection[key]
        for item, value in updates.items():
            doc[item] = value
        doc.save()

    def entry(self, key):
        try:
            item = self._collection[key]
        except DocumentNotFoundError:
            return None

        return item

    def find(self, **kwattrs):
        for item in self.entries:
            try:
                is_valid = [item[key] == value for key, value in kwattrs.items()]
                if all(is_valid):
                    return item
            except:
                continue
        return None

    @property
    def entries(self):
        return self._collection.fetchAll()


class Arango:
    def __init__(self):
        conn = Connection(
            arangoURL=f"http://{DBConfig.host}:{DBConfig.port}",
            username=DBConfig.User.name, password=DBConfig.User.password
        )

        try:
            self.database = conn.createDatabase(name=DBConfig.database)
        except CreationError:
            self.database = conn[DBConfig.database]

    def collection(self, name):

        try:
            return Collection(self.database.createCollection(name=name))
        except CreationError:
            return Collection(self.database[name])
