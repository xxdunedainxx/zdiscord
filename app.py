from zdiscord.util.logging.LogFactory import LogFactory
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.App import App
# https://discordpy.readthedocs.io/en/latest/api.html#discord-api-events
# https://stackoverflow.com/questions/42999961/ffmpeg-binary-not-found-python
from multiprocessing import Process
from zdiscord.service.ThreadQ import ThreadQueue
from zdiscord.util.general.Main import MainUtil
from zdiscord.util.general.Redis import RedisConfig
import time
import json
PROC_MAP: {} = {}



def appMain(config):
    try:
        app = App(config=config)
        main_log=LogFactory.get_logger(logName="main")
        main_log.info('Init main')
        app.run_wrapper(main_log)
    except Exception as e:
        print(errorStackTrace(e))
        main_log.error(f"CRITICAL ERROR IN MAIN APP!!! {errorStackTrace(e)}")
        exit(-1)
if __name__ == '__main__':
    try:
        MainUtil.init_threadq()

        # Start main worker
        PROC_MAP['main'] = Process(target=appMain, args=('./zdiscord/app.json',))
        PROC_MAP['main'].start()

        while PROC_MAP['main'].is_alive():
            print("still up...")
            if (ThreadQueue.has_thread()):
                print("New thread q item...")
                thread_config = ThreadQueue.get_thread_off_queue()
                if thread_config is not None:
                    PROC_MAP['test'] = Process(target=appMain, args=(thread_config,))
                    PROC_MAP['test'].start()
            time.sleep(5)
        exit(0)
    except Exception as e:
        print(errorStackTrace(e))
        exit(-1)

