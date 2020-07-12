from zdiscord.service.integration.chat.discord.agents.DiscordAgent import DiscordAgent
from zdiscord.service.integration.chat.discord.agents.games.tictactoe.TicTacToeMiddleware import DiscordTicTacToeMiddleware

class PollAgent(DiscordAgent):
    def __init__(self, conf: {}):
        DiscordAgent.__init__(self, conf=conf)

        self.context: {} = conf['context']
        self.bootstrap(conf=conf)

    def bootstrap(self, conf):
        self.middleware: DiscordTicTacToeMiddleware = DiscordTicTacToeMiddleware(conf)