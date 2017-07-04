# import Singleton as Singleton
import pymysql
import yaml

from nyalib.bot_config import BotConfig

class Singleton(object):
    """
    This class is used to insure that you  only a single instance of the object is ever created.
    Since we're using a relative path this should be invoked from NyaChan.py first.
    """
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
            class_.__contruct__(class_)
        return class_._instance

    def __contruct__(class_ ):
        try:
            config_stream = open('config/settings.yaml', 'r')
            class_._instance.config = yaml.load(config_stream)
            config_stream.close()
        except Exception as err:
            pass

        if(class_._instance.config is not None):
            class_.bot = BotConfig(**class_._instance.config['bot'])


class AppConfig(Singleton):
    """
    This class will only ever create a single instance of itself, no matter how many times it's created.
    """

    def db_connection(self):
        db_config = self.config['database']
        return pymysql.connect(
            host=db_config['host'], user=db_config['user'], password=db_config['password'], db=db_config['database'], charset='utf8')
