from zdiscord.service.Service import Service
from zdiscord.service.integration.chat.discord.agents.DiscordAgent import DiscordAgent

import threading

class DiscordAgentFactory(Service):
    def __init__(self, conf: {}):

        super().__init__(name=self.__class__.__name__)

        self.DISCORD_AGENT_CONFIGS: {} = {}

        self.setup_agent_configs(conf)

    def setup_agent_configs(self, conf:{}):
        for agent in conf['chat']['agents'].keys():
            agent_conf=conf['chat']['agents'][agent]['conf'].copy()

            agent_conf['chat'] = {}
            agent_conf['chat']['token'] = conf['chat']['token']
            agent_conf['chat']['platform'] = conf['chat']['platform']
            agent_conf['chat']['agent_stamp'] = True

            self.DISCORD_AGENT_CONFIGS[agent] = DiscordAgent(agent_conf)


    def run(self, agent: str):
        self.DISCORD_AGENT_CONFIGS[agent].run()