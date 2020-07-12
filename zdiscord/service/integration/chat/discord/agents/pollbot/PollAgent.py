from zdiscord.service.integration.chat.discord.agents.games.GameAgent import GameAgent
from zdiscord.service.integration.chat.discord.agents.games.tictactoe.TicTacToeMiddleware import DiscordTicTacToeMiddleware

class PollAgent(GameAgent):
    def __init__(self, conf: {}):
        GameAgent.__init__(self, conf=conf)
        self.context: {} = conf['context']
        self.bootstrap(conf=conf)

    def bootstrap(self, conf):
        self.middleware: DiscordTicTacToeMiddleware = DiscordTicTacToeMiddleware(conf)