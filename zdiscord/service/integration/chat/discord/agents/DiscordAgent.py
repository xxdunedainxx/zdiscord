from zdiscord.util.general.Agent import Agent
from zdiscord.service.integration.chat.discord.Discord import Discord
from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.integration.chat.discord.DiscordMiddleware import DiscordMiddleware

from multiprocessing import Process

class DiscordAgent(Discord, Agent):
    def __init__(self, conf: {}):
        Discord.__init__(self,conf=conf)
        Agent.__init__(self)

