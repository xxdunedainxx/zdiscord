from zdiscord.service.Service import Service
from zdiscord.util.error.ErrorFactory import errorStackTrace
import json
from typing import Any

# TODO : more advanced msg config
# TODO : intake message templates from files for more advanced messaging
# Ex:
"""
'=============================\n\n༼ つ ◕_◕ ༽つ\n\nOMEED SUCKS ASS\n\n༼ つ ◕_◕ ༽つ\n\n============================='

AND 

⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢰⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿
⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⣿
⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿
"""

class MessageConfig:
    def __init__(self, userMsg: str, responseMsg: str, type, main: Any = None, fallBack = None, arg: str = '', syncMsg: str = None,description: str = None, example: str = None, cmdRetries: int = 3 ):
        self.umsg = userMsg
        self.rmsg = responseMsg
        self.main = main
        self.fallback_logic: Any = fallBack
        self.type=type
        self.arg = arg
        self.sync_msg: str = syncMsg
        self.description = description
        self.example = example
        self.retries = cmdRetries


class MessageFactory(Service):
    FALL_BACK_VALUE: str = 'Failed to process response'

    def __init__(self, confLocation: str, servicesRefeence: {Service}):
        super().__init__(name='MessageFactory')
        self._logger.info("Start up message factory...")
        self.__MSG_CONFIGS: {} = {}
        self.services_ref = servicesRefeence
        self.__init_config(confLocation)

    def __init_config(self, confLocation: str):
        conf: {} = json.load(open(confLocation))

        for c in conf.keys():
            self.__MSG_CONFIGS[c] = MessageConfig(
                userMsg=c,
                responseMsg=conf[c]['resp'],
                fallBack=conf[c]['fallback'] if 'fallback' in conf[c].keys() else None,
                type=conf[c]['type'],
                main=eval(conf[c]['main']) if 'main' in conf[c].keys() else None,
                arg=conf[c]['arg'] if 'arg' in conf[c].keys() else '',
                syncMsg=conf[c]['syncMsg'] if 'syncMsg' in conf[c].keys() else None,
                description=conf[c]['description'] if 'description' in conf[c].keys() else None,
                example=conf[c]['example'] if 'example' in conf[c].keys() else None,
                cmdRetries=conf[c]['retries'] if 'retries' in conf[c].keys() else 3,
            )

        self._logger.info("init message config")

    def fetch_config(self) -> dict:
        return self.__MSG_CONFIGS

    def send_await_msg(self,cmd: str, msg: str) -> str:
        if cmd in self.__MSG_CONFIGS.keys():
            return self.__MSG_CONFIGS[cmd].sync_msg
        else:
            return None

    def process_response(self,cmd: str, msg: str) -> [str]:
        # TODO Contains vs cmd logic
        if cmd in self.__MSG_CONFIGS.keys():

            if self.__MSG_CONFIGS[cmd].type == 'lambda':
                retries = self.__MSG_CONFIGS[cmd].retries
                while retries > 0:
                    try:
                        # assume method if not a string
                        return self.__MSG_CONFIGS[cmd].main(msg)
                    except Exception as e:
                        self._logger.error(f"Fatal while processing main for {cmd}: {errorStackTrace(e)}")
                        retries-=1
            elif self.__MSG_CONFIGS[cmd].type == 'static_method':
                retries = self.__MSG_CONFIGS[cmd].retries
                while retries > 0:
                    try:
                        # assume method if not a string
                        return self.__MSG_CONFIGS[cmd].main(self.__MSG_CONFIGS[cmd].arg)
                    except Exception as e:
                        self._logger.error(f"Fatal while processing main for {cmd}: {errorStackTrace(e)}")
                        retries-=1
            # plain string response: ex: 'ping' --> resp 'pong'
            else:
                return self.__MSG_CONFIGS[cmd].rmsg
        elif 'default' in self.__MSG_CONFIGS.keys():
            return self.__MSG_CONFIGS['default'].rmsg
        else:
            self._logger.warn("FAILED TO PROCESS ANY OF THE MESSAGES PROVIDED IN CONFIG")
            return MessageFactory.FALL_BACK_VALUE

    #def add_config(self,key: str, value: Any):
    #    if key not in self.__MSG_CONFIGS.keys():
    #        self.__MSG_CONFIGS[key] = value
    #    else:
    #        # TODO: custom exception in error factory
    #        raise Exception('NO CANT OVERRIDE')

    # TODO Supported commands? Help command?

    # TODO Help per config