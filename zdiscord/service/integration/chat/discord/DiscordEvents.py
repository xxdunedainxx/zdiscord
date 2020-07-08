from zdiscord.service.messaging.EventFactory import IEvent, EventConfig
from typing import Any
import discord
class DiscordEvent(IEvent):

    def __init__(self, type: str, context: Any = None):
        super().__init__(type, context)
        self.parsed_command: str = None
        self.parsed_message: str = None

class DiscordOnVoiceStateUpdateEvent(EventConfig):
    def __init__(self, conf: {}):
        super().__init__(conf)

    def is_valid_event(self, event: IEvent) -> bool:
        return True

class DiscordStrictStringMatchEvent(EventConfig):
    def __init__(self, conf: {}):
        super().__init__(conf)

        self.__str_match_str: str = conf['StrictString'] if 'StrictString' in conf.keys() else None
        self.__keyword: str = conf['keyword'] if 'keyword' in conf.keys() else None

    def is_valid_event(self, event: IEvent) -> bool:
        if self.contains_keyword(msg=event.context['message_object'].content):
            event.context['message_object'].content = event.context['message_object'].content.replace(f"{self.__keyword} ", '')

        return self.__str_match_str is not None and event.context['message_object'].content == self.__str_match_str

    def parse_event(self, event: {}):
        return event

    def contains_keyword(self, msg: str) -> bool:
        return  f"{self.__keyword} " in msg


class DiscordStrictStringContainsEvent(EventConfig):
    def __init__(self, conf: {}):
        super().__init__(conf)

        self.__str_match_str: str = conf['StringRegex'] if 'StringRegex' in conf.keys() else None

    def is_valid_event(self, event: IEvent) -> bool:
        return self.__str_match_str is not None and self.__str_match_str in event.context['message_object'].content

    def parse_event(self, event: {}):
        return event

class DiscordStringParseCommand(EventConfig):
    def __init__(self, conf: {}):
        super().__init__(conf)

        self.__str_match_str: str = conf['StringRegex'] if 'StringRegex' in conf.keys() else None
        self.__keyword: str = conf['keyword'] if 'keyword' in conf.keys() else None

    def is_valid_event(self, event: DiscordEvent) -> bool:
        self.parse_event(event=event, message=event.context['message_object'])
        return self.__str_match_str is not None and self.__str_match_str == event.parsed_command

    def parse_event(self, event: DiscordEvent,message: discord.Message):
        cmd = self.parse_cmd(event, message)
        self.parse_msg(message=message, event=event)


    def parse_cmd(self, event: DiscordEvent, message: discord.Message) -> None:
        try:
            if self.contains_keyword(msg=message.content):
                message.content = message.content.replace(f"{self.__keyword} ", '')

            if ' ' in message.content:
                event.parsed_command = message.content.split(' ')[0]
            else:
                event.parsed_command = ''
        except Exception as e:
            event.parsed_command = ''

    def parse_msg(self,message: discord.Message,event: DiscordEvent) -> None:
        try:
            event.parsed_message = message.content.replace(f"{event.parsed_command} ", '')
        except Exception as e:
            event.parsed_message = ''

    def contains_keyword(self, msg: str) -> bool:
        return f"{self.__keyword} " in msg

class DiscordStringParseCommandWithKeyword(DiscordStringParseCommand):
    def __init__(self, conf: {}):
        super().__init__(conf)

        self.__str_match_str: str = conf['StringRegex'] if 'StringRegex' in conf.keys() else None
        self.__keyword: str = conf['keyword'] if 'keyword' in conf.keys() else None

    def is_valid_event(self, event: DiscordEvent) -> bool:
        self.parse_event(event=event, message=event.context['message_object'])
        return self.__str_match_str is not None and self.__str_match_str == event.parsed_command

    def parse_cmd(self, event: DiscordEvent, message: discord.Message) -> None:
        try:
            if self.contains_keyword(msg=message.content):
                message.content = message.content.replace(f"{self.__keyword} ", '')

            if ' ' in message.content:
                event.parsed_command = message.content.split(' ')[0]
            else:
                event.parsed_command = ''
        except Exception as e:
            event.parsed_command = ''

    def contains_keyword(self, msg: str) -> bool:
        return f"{self.__keyword} " in msg