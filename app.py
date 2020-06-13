# TODO: package & organize
# TODO: containerize
# TODO: install on rpi
# TODO: upload ghe
from zdiscord.util.logging.LogFactory import LogFactory
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.App import App

# TODO CLI configuration for app.json
# TODO If app crashes, restart discord bot?

app = App(config_path="./zdiscord/app.json")

if __name__ == "__main__":
    try:
        main_log=LogFactory.get_logger(logName="main")
        main_log.info('Init main')
        app = App(config_path="./zdiscord/app.json")
    except Exception as e:
        main_log.error(f"CRITICAL ERROR IN MAIN APP!!! {errorStackTrace(e)}")
        exit(-1)
exit(0)
