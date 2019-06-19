import discord
from discord.ext import commands


__all__ = ("CommandContext")


class CustomItem:
    def __init__(self, **kwargs):
        self.name = kwargs.pop("name", None)
        self.value = kwargs.pop("value", None)


class CustomItems:
    def __init__(self):
        self.__custom_items = []

    def get_item(self, item_name):
        return discord.utils.get(self.__custom_items, name=item_name)

    def __getitem__(self, item_name):
        item = self.get_item(item_name)
        return item.value if item else None

    # Only allow getting for attribute name, not setting
    def __getattr__(self, item_name):
        return self.__getitem__(item_name)

    def __setitem__(self, item_name, item_value):
        item = discord.utils.get(self.__custom_items, name=item_name)
        if not item:
            custom_item_instance = CustomItem(name=item_name, value=item_value)
            self.__custom_items.append(custom_item_instance)
        else:
            item.value = item_value


class CommandContext(commands.Context):
    def __init__(self, **attrs):
        super().__init__(**attrs)
        self._custom_items = None

    @property
    def custom(self):
        if not self._custom_items:
            self._custom_items = CustomItems()
        return self._custom_items
