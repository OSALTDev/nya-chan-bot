from copy import copy


class ReadOnlyDictAttributeAccess(dict):
    def __readonly__(self, *args, **kwargs):
        raise RuntimeError("Cannot modify read-only object!")
    __setitem__ = __readonly__
    __delitem__ = __readonly__
    __setattr__ = __readonly__
    pop = __readonly__
    popitem = __readonly__
    clear = __readonly__
    update = __readonly__
    setdefault = __readonly__
    del __readonly__

    def __getattribute__(self, attr_name):
        # Use int() to convert channel id to integer
        return int(super().get(attr_name))

    def __getitem__(self, item):
        # Use int() to convert channel id to integer
        return int(super().get(item))


class BotConfig(object):
    def __init__(self, **kargs):
        self.bot = copy(kargs)

    @property
    def description(self):
        return self.bot.get('description')

    @description.setter
    def description(self, value):
        self.bot['description'] = value

    @property
    def name(self):
        return self.bot.get('name')

    @property
    def prefix(self):
        return self.bot.get('prefix')

    @property
    def cogs(self):
        # Ensures owner is always available.
        if 'owner' not in self.bot.get('startup_cogs'):
            self.bot.get('startup_cogs').append('owner')

        return self.bot.get('startup_cogs')

    @property
    def token(self):
        return self.bot.get('token')

    @property
    def channel(self):
        return ReadOnlyDictAttributeAccess(self.bot.get('custom_channels'))


