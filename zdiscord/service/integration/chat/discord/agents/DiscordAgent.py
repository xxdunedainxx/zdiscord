from zdiscord.service.integration.chat.discord.DiscordMiddleware import DiscordMiddleware
from zdiscord.service.Service import Service

from multiprocessing import Process

class DiscordAgent(Service):
    def __init__(self, conf: {}):
        Service.__init__(self, name=self.__class__.__name__)

        self.agent_configuration = conf

        self.__middleware: DiscordMiddleware = None

    def run(self):
        self.__middleware = DiscordMiddleware(self.agent_configuration)
