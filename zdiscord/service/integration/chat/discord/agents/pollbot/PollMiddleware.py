from zdiscord.service.integration.chat.discord.DiscordMiddleware import DiscordMiddleware
from zdiscord.service.integration.chat.discord.agents.games.tictactoe.TicTacToeDiscordClient import TicTacToeDiscordClient
from zdiscord.service.integration.chat.discord.voice.DiscordVoice import DiscordVoice
from zdiscord.service.integration.chat.discord.DiscordEventMiddleware import DiscordEventFactory
from zdiscord.service.integration.chat.discord.DiscordEvents import DiscordStrictStringMatchEvent,DiscordEvent
from zdiscord.service.messaging.Events import EventConfig
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.service.integration.chat.discord.agents.games.tictactoe.TicTacToeGameboard import AIPlayer
from zdiscord.service.integration.chat.discord.agents.games.tictactoe.TicTacToeDiscordGameboard import DiscordTicTacToeGameboard, DiscordPlayer
from zdiscord.service.integration.chat.discord.DiscordCommandMiddleware import DiscordCommandMiddleware
from zdiscord.service.integration.chat.discord.voice.VoiceFactory import VoiceFactory
from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.integration.chat.discord.macros.MacroFactory import MacroFactory
import zdiscord.service.integration.chat.discord.agents.games.tictactoe.macros.Moves as TicTacToeMoves
import discord
from typing import Any

class PollMiddleware(DiscordMiddleware):
    def __init__(self, conf: {}):
        super().__init__(conf=conf)

        self._logger.info("DiscordTicTacToeMiddleware initialized!")
        self.context: {} = conf['context']

    def bootstrap_chat_client(self):
        self._chat_client: TicTacToeDiscordClient = TicTacToeDiscordClient(eventPusher=self.event_subscriber, context=self.context)

    def run(self):
        self.bootstrap_chat_client()
        self._chat_client.run(self._API_TOKEN)

    async def on_ready(self, event: DiscordEvent):
        self._logger.info(f"The tic tac toe game has started!")
        ServiceFactory.SERVICES['PollBot'] = self._chat_client
        MacroFactory.POLLBOT = TicTacToeMoves

