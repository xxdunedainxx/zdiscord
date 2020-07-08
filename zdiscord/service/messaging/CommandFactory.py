from zdiscord.service.Service import Service
from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.messaging.EventFactory import IEvent, EventConfig
from zdiscord.service.integration.chat.discord.macros.General import help_msg
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
    HELP_MSG: str

    def __init__(self, conf:{}):
        super().__init__(name=self.__class__.__name__)
        self.COMMAND_IMPORTER = importlib.import_module(self.__module__)
        self._logger.info(f"Start up command factory... with module context {self.__module__}")
        self.services_ref = ServiceFactory.SERVICES
        self._COMMAND_CONFIGS: {} = {}
        self.__init_config(conf)

        self.__build_help_msg()


    def __init_config(self, conf: {}):
        for command_config in conf.keys():
            self._COMMAND_CONFIGS[command_config] = getattr(self.COMMAND_IMPORTER, conf[command_config]['type'])(conf=conf[command_config]['conf'])

        self._logger.info("init message config")
        self._logger.info(f"Understood commands: {self._COMMAND_CONFIGS}")

    def execute_cmd(self, event: IEvent, eventConfig: EventConfig):
        self._COMMAND_CONFIGS[eventConfig.lookup].run(event)

    def __build_help_msg(self) -> None:
        help_msg_builder: str = 'See the below supported commands and their usage:\n'
        help_msg_builder += '\nCUSTOM BUILT COMMANDS:\n'

        for cmd in self._COMMAND_CONFIGS.keys():
            if self._COMMAND_CONFIGS[cmd].description is not None and self._COMMAND_CONFIGS[cmd].example is not None and self._COMMAND_CONFIGS[cmd].command is not None:
                help_msg_builder += f"\n--- {self._COMMAND_CONFIGS[cmd].command}  ---\n"
                help_msg_builder += f"Description: {self._COMMAND_CONFIGS[cmd].description}\n"
                help_msg_builder += f"Example Usage: {self._COMMAND_CONFIGS[cmd].example}\n"

        #help_msg_builder += '\nPRE BUILT COMMANDS:\n'
        #for cmd in self.__HARD_CODED_ROUTINES.keys():
        #    if cmd == 'help':
        #        continue
        #    else:
        #        help_msg_builder += f"\n--- {cmd}  ---\n"
        #        help_msg_builder += f"Description: {self.__HARD_CODED_ROUTINES[cmd]['description']}\n"
        #        help_msg_builder += f"Example Usage: {self.__HARD_CODED_ROUTINES[cmd]['example']}\n"

        # Override value here
        CommandFactory.HELP_MSG = help_msg_builder
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