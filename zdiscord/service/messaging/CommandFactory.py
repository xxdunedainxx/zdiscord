from zdiscord.service.Service import Service
from zdiscord.service.ServiceFactory import ServiceFactory
import importlib
import json
from typing import Any

COMMANDS: {} = {}

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

# NOTE THESE ARE ALL PLACEHOLDERS AND MUST BE OVERRIDDEN BY CHAT CLIENT SPECIFIC LOGIC

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

class CommandFactory(Service):
    # For dynamic command import to run via string


    def __init__(self, confLocation: str):
        super().__init__(name='CommandFactory')
        self.COMMAND_IMPORTER = importlib.import_module(self.__module__)
        self._logger.info(f"Start up command factory... with module context {self.__module__}")
        self.services_ref = ServiceFactory.SERVICES

    def execute_cmd(self, command: str, *args, **kwargs):
        pass
"""
getattr(module, class_name)
            if self.__MSG_CONFIGS[cmd].type == 'lambda':
                # assume method if not a string
                return self.__MSG_CONFIGS[cmd].main(msg)
            elif self.__MSG_CONFIGS[cmd].type == 'static_method':
                return self.__MSG_CONFIGS[cmd].main(self.__MSG_CONFIGS[cmd].arg)
            # plain string response: ex: 'ping' --> resp 'pong'
            else:
def __init_config(self, confLocation: str):
        conf: {} = json.load(open(confLocation))
        self.__RAW_CONFIG = conf

        for c in conf.keys():
            self.__MSG_CONFIGS[c] = Command(
                userMsg=c,
                responseMsg=conf[c]['resp'],
                fallBack=conf[c]['fallback'] if 'fallback' in conf[c].keys() else None,
                type=conf[c]['type'],
                main=eval(conf[c]['main']) if 'main' in conf[c].keys() else None,
                arg=conf[c]['arg'] if 'arg' in conf[c].keys() else '',
                syncMsg=conf[c]['syncMsg'] if 'syncMsg' in conf[c].keys() else None,
                description=conf[c]['description'] if 'description' in conf[c].keys() else None,
                example=conf[c]['example'] if 'example' in conf[c].keys() else None,
            )

        self._logger.info("init message config")"""