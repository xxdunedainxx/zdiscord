from zdiscord.service.Service import Service
from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.integration.chat.discord.DiscordAgentFactory import DiscordAgentFactory
from zdiscord.service.integration.chat.discord.DiscordMiddleware import DiscordMiddleware
from zdiscord.service.ThreadQ import ThreadQueue
import json
class Discord(Service):
    def __init__(self, conf: {}):

        super().__init__(name=self.__class__.__name__)
        
        self.__middleware: DiscordMiddleware = DiscordMiddleware(conf)


        if conf['chat']['agent_stamp'] == False:
            self._af: DiscordAgentFactory = DiscordAgentFactory(conf)
            conf['chat']['agent_stamp'] = False
        else:
            self._af = None

        ServiceFactory.SERVICES['agent'] = self._af


    def run(self):
        if self._af is not None:
            ThreadQueue.add_thread(config=f"{json.dumps(self._af.DISCORD_AGENT_CONFIGS['test_agent'].agent_configuration)}")
        self.__middleware.run()