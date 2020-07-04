from zdiscord.util.logging.LogFactory import LogFactory
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.App import App
# https://discordpy.readthedocs.io/en/latest/api.html#discord-api-events
# https://stackoverflow.com/questions/42999961/ffmpeg-binary-not-found-python

if __name__ == "__main__":
    try:
        app = App(config_path="./zdiscord/app.json")
        main_log=LogFactory.get_logger(logName="main")
        main_log.info('Init main')
        app.run_wrapper(main_log)
    except Exception as e:
        print(errorStackTrace(e))
        main_log.error(f"CRITICAL ERROR IN MAIN APP!!! {errorStackTrace(e)}")
        exit(-1)
exit(0)

