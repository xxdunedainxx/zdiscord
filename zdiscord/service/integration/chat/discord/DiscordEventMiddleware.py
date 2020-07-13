from zdiscord.service.Service import Service
from zdiscord.service.messaging.EventFactory import EventFactory
from zdiscord.service.integration.chat.discord.DiscordEvents import DiscordAlwaysTrue,DiscordStrictStringMatchEvent,DiscordStrictStringContainsEvent,DiscordStringParseCommand,DiscordStringParseCommandWithKeyword, DiscordOnVoiceStateUpdateEvent,DiscordEvent
from typing import Any

class DiscordEventFactory(EventFactory):
    def __init__(self, conf: {}):
        super().__init__(conf=conf)
