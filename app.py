# TODO: package & organize
# TODO: containerize
# TODO: install on rpi
# TODO: upload ghe
from zdiscord.util.logging.LogFactory import LogFactory
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.App import App
# https://discordpy.readthedocs.io/en/latest/api.html#discord-api-events
# TODO CLI configuration for app.json
# TODO If app crashes, restart discord bot?
# TODO Health check on voice client
# TODO :Error handling for uneeded things like voice factory creation
# https://stackoverflow.com/questions/42999961/ffmpeg-binary-not-found-python

if __name__ == "__main__":
    try:
        app = App(config_path="./zdiscord/app.json")
        main_log=LogFactory.get_logger(logName="main")
        main_log.info('Init main')
        app.run()
    except Exception as e:
        main_log.error(f"CRITICAL ERROR IN MAIN APP!!! {errorStackTrace(e)}")
        exit(-1)
exit(0)

