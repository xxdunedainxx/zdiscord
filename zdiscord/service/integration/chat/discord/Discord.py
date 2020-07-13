from zdiscord.service.Service import Service
from zdiscord.service.integration.chat.discord.DiscordMiddleware import DiscordMiddleware

class Discord(Service):
    def __init__(self, conf: {}):
        self.middleware: DiscordMiddleware
        self.conf = conf
        super().__init__(name=self.__class__.__name__)

    def bootstrap(self, conf):
        self.middleware: DiscordMiddleware = DiscordMiddleware(conf)

    def run(self):
        self.bootstrap(self.conf)
        self.middleware.run()