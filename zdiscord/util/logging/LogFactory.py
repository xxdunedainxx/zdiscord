import logging
import sys
from zdiscord.util.general.Singleton import Singletone
import os

class LogFactory():
    loggers: {} = {}
    log_dir: str = ''
    log_level: str = 'INFO'
    log_stdout: bool = True

    @staticmethod
    def get_logger(logName: str) -> logging._loggerClass:
        if LogFactory.log_dir != '' and  not os.path.exists(LogFactory.log_dir):
            os.makedirs(LogFactory.log_dir)

        if logName not in LogFactory.loggers:
            if os.path.isfile(f"{LogFactory.log_dir}{os.sep}{logName}.log") is False:
                LogFactory.touch_file(f"{LogFactory.log_dir}{os.sep}{logName}.log")

            LogFactory.loggers[logName] = logging.getLogger(logName)
            LogFactory.loggers[logName].setLevel(logging.getLevelName(LogFactory.log_level))
            handler: logging.FileHandler=logging.FileHandler(f"{LogFactory.log_dir}{os.sep}{logName}.log", encoding='utf-8')
            formatter: logging.Formatter = logging.Formatter('[%(asctime)s %(levelname)s]: %(message)s')
            handler.setFormatter(formatter)

            # create console handler with a higher log level
            if LogFactory.log_stdout:
                stdhandler = logging.StreamHandler(sys.stdout)
                stdhandler.setLevel(logging.getLevelName(LogFactory.log_level))
                stdhandler.setFormatter(formatter)
                LogFactory.loggers[logName].addHandler(stdhandler)

            LogFactory.loggers[logName].addHandler(handler)
        return LogFactory.loggers[logName]

    @staticmethod
    def touch_file(path):
        with open(path, 'a'):
            os.utime(path, None)