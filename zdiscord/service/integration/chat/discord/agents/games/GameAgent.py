from zdiscord.service.integration.chat.discord.agents.DiscordAgent import DiscordAgent

class GameAgent(DiscordAgent):
    def __init__(self, conf: {}):
        DiscordAgent.__init__(self,conf=conf)