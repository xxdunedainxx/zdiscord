# contains connectors between discord api logic && command logic
from zdiscord.service.messaging.CommandFactory import CommandFactory
from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.integration.chat.discord.DiscordEvents import DiscordEvent
from zdiscord.service.messaging.Events import EventConfig
from zdiscord.service.integration.chat.discord.macros.MacroFactory import MacroFactory
import importlib
import json
from typing import Any

class Command:
    def __init__(self, command: str, responseMsg: str,type, logic: Any = None, fallBack = None, arg: str = '', syncMsg: str = None,description: str = None, example: str = None):
        self.command = command
        self.response = responseMsg
        self.command_logic = logic
        self.fallback_logic: Any = fallBack
        self.type=type
        self.arg = arg
        self.sync_msg: str = syncMsg
        self.description = description
        self.example = example

    # execute command logic
    def run(self, event: DiscordEvent):
        # no-op, must ber overridden
        raise Exception('THIS METHOD MUST BE OVERRIDDEN!!')

class SimpleStringCommand(Command):

    def __init__(self, conf: {}):
        super().__init__(
            command=conf['command'] if 'command' in conf.keys() else None,
            responseMsg=conf['responseMsg'] if 'responseMsg' in conf.keys() else None,
            type=conf['type'] if 'type' in conf.keys() else None,
            logic=conf['logic'] if 'logic' in conf.keys() else None,
            fallBack=conf['fallBack'] if 'fallBack' in conf.keys() else None,
            arg=conf['arg'] if 'arg' in conf.keys() else None,
            syncMsg=conf['syncMsg'] if 'syncMsg' in conf.keys() else None,
            description=conf['description'] if 'description' in conf.keys() else None,
            example=conf['example'] if 'example' in conf.keys() else None,
        )
    # execute command logic
    async def run(self, event: DiscordEvent):
        await event.context['message_object'].channel.send(self.response)

class LambdaMessageCommand(Command):
    def __init__(self, conf: {}):
        super().__init__(
            command=conf['command'] if 'command' in conf.keys() else None,
            responseMsg=conf['responseMsg'] if 'responseMsg' in conf.keys() else None,
            type=conf['type'] if 'type' in conf.keys() else None,
            logic=conf['logic'] if 'logic' in conf.keys() else None,
            fallBack=conf['fallBack'] if 'fallBack' in conf.keys() else None,
            arg=conf['arg'] if 'arg' in conf.keys() else None,
            syncMsg=conf['syncMsg'] if 'syncMsg' in conf.keys() else None,
            description=conf['description'] if 'description' in conf.keys() else None,
            example=conf['example'] if 'example' in conf.keys() else None,
        )
    # execute command logic
    async def run(self, event: DiscordEvent):
        services: {} = ServiceFactory.SERVICES
        if self.sync_msg is not None:
            await event.context['message_object'].channel.send(self.sync_msg)
        await eval(self.command_logic)(event.parsed_message, event)

class StaticCommand(Command):
    def __init__(self, conf: {}):
        super().__init__(
            command=conf['command'] if 'command' in conf.keys() else None,
            responseMsg=conf['responseMsg'] if 'responseMsg' in conf.keys() else None,
            type=conf['type'] if 'type' in conf.keys() else None,
            logic=conf['logic'] if 'logic' in conf.keys() else None,
            fallBack=conf['fallBack'] if 'fallBack' in conf.keys() else None,
            arg=conf['arg'] if 'arg' in conf.keys() else None,
            syncMsg=conf['syncMsg'] if 'syncMsg' in conf.keys() else None,
            description=conf['description'] if 'description' in conf.keys() else None,
            example=conf['example'] if 'example' in conf.keys() else None,
        )
    # execute command logic
    async def run(self, event: DiscordEvent):
        services: {} = ServiceFactory.SERVICES
        if self.sync_msg is not None:
            await event.context['message_object'].channel.send(self.sync_msg)
        await eval(self.command_logic)

class DiscordCommandMiddleware(CommandFactory):
    def __init__(self, conf: {}):
        super().__init__(conf=conf)

    async def execute_cmd(self, event: DiscordEvent, eventConfig: EventConfig):
        await self._COMMAND_CONFIGS[eventConfig.lookup].run(event)