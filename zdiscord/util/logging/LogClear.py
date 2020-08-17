from zdiscord.util.logging.LogFactory import LogFactory

import os
import datetime
import random
import shutil

# TODO code could be enhanced & cleaned up

class LogClear:
    Logger = None
    LogDir = None
    LogZipDestination = None
    LogMegabyteTop = None

    def __init__(self):
        pass

    @staticmethod
    def init(logName='LogClear', log_dir=LogFactory.log_dir, LogZipDestination='LOCAL', LogMegabyteTop=5):
        LogClear.Logger = LogFactory.get_logger(logName='LogClear')
        LogClear.LogDir = LogFactory.log_dir
        LogClear.LogZipDestination: str = 'LOCAL'
        LogClear.LogMegabyteTop: int = 5

    @staticmethod
    def clean_up_logs():
        LogClear.Logger.info("Running log clean up!")

        logs_to_zip:[str] = []

        for file in os.listdir(LogClear.LogDir):
            if file.endswith(".log"):
                # print(os.path.join(directory, filename))
                LogClear.Logger.info(f"Checking log {file}")

                file_info = os.stat(f"{LogClear.LogDir}{os.sep}{file}")
                if(datetime.datetime.now() - datetime.datetime.fromtimestamp(file_info.st_birthtime)).days > 1:
                    logs_to_zip.append(file)
                    LogClear.Logger.info(f"File {file}, is old!")
                elif file_info.st_size * .000001 > LogClear.LogMegabyteTop:
                    LogClear.Logger.info(f"File {file}, is too large!")
                    logs_to_zip.append(file)
                else:
                    continue

        if len(logs_to_zip) > 2:
            zip_folder = f"{LogClear.LogDir}{os.sep}tmp{os.sep}{datetime.datetime.now().toordinal()}-files"

            os.makedirs(f"{zip_folder}", exist_ok=True)

            for file in logs_to_zip:
                shutil.move(f"{LogClear.LogDir}{os.sep}{file}",f"{zip_folder}{os.sep}{file}")
                LogFactory.touch_file(path=f"{LogClear.LogDir}{os.sep}{file}")

            shutil.make_archive(f"{zip_folder}z", 'zip', zip_folder)
            shutil.rmtree(zip_folder)