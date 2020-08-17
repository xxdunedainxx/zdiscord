from zdiscord.service.integration.chat.IChatMiddleware import IChatMiddleware
from zdiscord.service.integration.chat.discord.DiscordClient import DiscordBot
from zdiscord.service.integration.chat.discord.voice.DiscordVoice import DiscordVoice
from zdiscord.service.integration.chat.discord.DiscordEventMiddleware import DiscordEventFactory
from zdiscord.service.integration.chat.discord.DiscordEvents import DiscordStrictStringMatchEvent,DiscordEvent
from zdiscord.service.messaging.Events import EventConfig
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.service.integration.chat.discord.DiscordCommandMiddleware import DiscordCommandMiddleware
from zdiscord.service.integration.chat.discord.voice.VoiceFactory import VoiceFactory
from zdiscord.service.ServiceFactory import ServiceFactory
import discord
from typing import Any

class DiscordMiddleware(IChatMiddleware):
    def __init__(self, conf: {}):
        super().__init__(conf=conf)
        self._API_TOKEN = conf['chat']['token']
        self._ef: DiscordEventFactory = DiscordEventFactory(conf=conf['event_factory'] if 'event_factory' in conf.keys() else {})
        self._vf: VoiceFactory = VoiceFactory(conf['voice_factory']['conf'], conf['voice_factory']['ffmpeg']) if 'voice_factory' in conf.keys() and 'ffmpeg' in conf['voice_factory'].keys() else None

        self._cf: DiscordCommandMiddleware = DiscordCommandMiddleware(conf=conf['command_factory'] if 'command_factory' in conf.keys() else {})
        self._logger.info("DiscordMiddleware initialized!")

    def bootstrap_chat_client(self):
        self._chat_client: DiscordBot = DiscordBot(eventPusher=self.event_subscriber)
        if self._vf is not None:
            self.__voice_client = DiscordVoice(bot=self._chat_client, voiceFactory=self._vf, ffmpeg=self._vf.ffmpeg)
            ServiceFactory.SERVICES['voice'] = self.__voice_client

    def run(self):
        self.bootstrap_chat_client()
        self._logger.info("In thread?")
        self._chat_client.run(self._API_TOKEN)

    def is_alive(self) -> bool:
        return not self._chat_client.is_closed()

    async def event_subscriber(self, event: DiscordEvent):
        try:
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
