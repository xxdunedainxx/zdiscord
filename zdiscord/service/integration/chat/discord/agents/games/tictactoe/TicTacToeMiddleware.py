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

class DiscordTicTacToeMiddleware(DiscordMiddleware):
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
        self._GAME: DiscordTicTacToeGameboard = DiscordTicTacToeGameboard(
            playerOne=DiscordPlayer(
                name=self._chat_client.player_one.name,
                symbol=DiscordTicTacToeGameboard.X_MOVE,
                discordUser=event.context['players']['player_one']
            ),
            playerTwo=AIPlayer(symbol=DiscordTicTacToeGameboard.O_MOVE),
            channel=self._chat_client.channel,
        )

        ServiceFactory.SERVICES['TicTacToe'] = self._GAME
        MacroFactory.TICTACTOE = TicTacToeMoves

        await self._chat_client.channel.send(self._GAME.print_board())

    async def event_subscriber(self, event: DiscordEvent):
        try:
            if event.type == 'on_ready':
                await self.on_ready(event=event)

            event_config: EventConfig = self._ef.is_valid_event(event=event)
            # Throw away invalid events
            if event_config is None:
                return
            try:
                self._logger.info(f"Event from discord client \'{str(event.type)}\'")
                await self._cf.execute_cmd(event, event_config)
            except Exception as e:
                self._logger.error(f"SOMETHING BAD HAPPENED {errorStackTrace(e)}")
                await event.context['message_object'].channel.send("Something bad happened :(")
        except Exception as e:
            self._logger.error(f"Failed to process event {errorStackTrace(e)}")
            return
