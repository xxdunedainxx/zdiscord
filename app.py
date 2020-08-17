from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.App import App
# https://discordpy.readthedocs.io/en/latest/api.html#discord-api-events
# https://stackoverflow.com/questions/42999961/ffmpeg-binary-not-found-python
from zdiscord.util.general.AgentFactory import AgentFactory


AppRunner: AgentFactory = AgentFactory

if __name__ == '__main__':
    try:
        AppRunner: AgentFactory = AgentFactory('./zdiscord/app.json')
        AppRunner.main()
    except Exception as e:
        print(errorStackTrace(e))
        exit(-1)
