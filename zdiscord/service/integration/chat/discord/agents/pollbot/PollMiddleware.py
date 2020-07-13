from zdiscord.service.integration.chat.discord.DiscordMiddleware import DiscordMiddleware
from zdiscord.service.integration.chat.discord.agents.pollbot.PollDiscordClient import PollDiscordClient
from zdiscord.service.integration.chat.discord.DiscordEvents import DiscordStrictStringMatchEvent,DiscordEvent
from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.integration.chat.discord.macros.MacroFactory import MacroFactory
import zdiscord.service.integration.chat.discord.agents.pollbot.macros.close as PollBotMacros

class PollMiddleware(DiscordMiddleware):
    def __init__(self, conf: {}):
        super().__init__(conf=conf)

        self._logger.info("PollMiddleware initialized!")
        self.conf = conf
        self.context: {} = conf['context']

    def bootstrap_chat_client(self):
        self._chat_client: PollDiscordClient = PollDiscordClient(eventPusher=self.event_subscriber, context=self.context, options=self.conf['options'])

    def run(self):
        self.bootstrap_chat_client()
        self._chat_client.run(self._API_TOKEN)

    async def on_ready(self, event: DiscordEvent):
        self._logger.info(f"The tic tac toe game has started!")
        ServiceFactory.SERVICES['PollBot'] = self._chat_client
        MacroFactory.POLLBOT = PollBotMacros

