from zdiscord.util.logging.LogFactory import LogFactory
import logging

class Service:

    def __init__(self, name: str):
        self._logger: logging._loggerClass = LogFactory.get_logger(logName=f"{name}")