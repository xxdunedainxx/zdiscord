from zdiscord.service.Service import Service
from zdiscord.service.integration.chat.discord.DiscordMiddleware import DiscordMiddleware

class Discord(Service):
    def __init__(self, conf: {}):

        super().__init__(name=self.__class__.__name__)
        
        self.__middleware: DiscordMiddleware = DiscordMiddleware(conf)

    def run(self):
        self.__middleware.run()