# contains connectors between discord api logic && command logic
from zdiscord.service.messaging.CommandFactory import CommandFactory
from zdiscord.service.Service import Service
from zdiscord.service.ServiceFactory import ServiceFactory
import importlib
import json
from typing import Any

class Command:
    def __init__(self, command: str, responseMsg: str, type, logic: Any = None, fallBack = None, arg: str = '', syncMsg: str = None,description: str = None, example: str = None):
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
    def run(self):
        # no-op, must ber overridden
        raise Exception('THIS METHOD MUST BE OVERRIDDEN!!')

    def send_await_msg(self,cmd: str, msg: str) -> str:
        if cmd in self.__MSG_CONFIGS.keys():
            return self.__MSG_CONFIGS[cmd].sync_msg
        else:
            return None

class SimpleStringCommand:
    pass

    # execute command logic
    def run(self):
        pass

class LambdaCommand:
    pass

    # execute command logic
    def run(self):
        pass

class StaticCommand:
    pass

    # execute command logic
    def run(self):
        pass


class DiscordCommandMiddleware(CommandFactory):
    pass
# except AttributeError:
# c=getattr(self.COMMAND_IMPORTER, 'StaticCommand')
# return