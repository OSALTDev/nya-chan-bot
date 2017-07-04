from copy import copy


class BotConfig(object):
    def __init__(self, **kargs):
        self.bot = copy(kargs)

    @property
    def description(self):
        return self.bot.get('description')

    @description.setter
    def description(self, value):
        self.bot['description']= value

    @property
    def name(self):
        return self.bot.get('name')

    @property
    def prefix(self):
        return self.bot.get('prefix')

    @property
    def cogs(self):
        return self.bot.get('startup_cogs')

    @property
    def token(self):
        return self.bot.get('token')
