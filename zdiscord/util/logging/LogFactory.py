import logging
from zdiscord.util.general.Singleton import Singletone
import os

class LogFactory():
    loggers: {} = {}
    log_dir: str = ''

    @staticmethod
    def get_logger(logName: str) -> logging._loggerClass:
        # TODO helper to update log_dir and put this there
        if LogFactory.log_dir != '' and  not os.path.exists(LogFactory.log_dir):
            os.makedirs(LogFactory.log_dir)

        if logName not in LogFactory.loggers:
            LogFactory.loggers[logName] = logging.getLogger(logName)
            handler: logging.FileHandler=logging.FileHandler(f"{LogFactory.log_dir}{os.sep}{logName}.log")
            formatter: logging.Formatter = logging.Formatter('[%(asctime)s %(levelname)s]: %(message)s')
            handler.setFormatter(formatter)
            LogFactory.loggers[logName].addHandler(handler)
        return LogFactory.loggers[logName]
