from nyalib.config import AppConfig


class BaseCog(object):
      def __init__(self, bot):
          self.config = AppConfig()
          self.bot = bot
          # TODO: add logger here.
