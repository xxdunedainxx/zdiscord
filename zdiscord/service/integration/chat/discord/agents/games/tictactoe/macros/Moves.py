from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.messaging.Events import IEvent

from zdiscord.service.integration.chat.discord.agents.games.tictactoe.TicTacToeDiscordGameboard import AIPlayer,DiscordPlayer

async def tic_tac_toe_move(event: IEvent):
    await ServiceFactory.SERVICES['TicTacToe'].discord_event(event)

async def quit_game(event: IEvent):
    await ServiceFactory.SERVICES['TicTacToe'].player_one.interact("The game has ended!")
    if type(ServiceFactory.SERVICES['TicTacToe'].player_two) is not AIPlayer:
        await ServiceFactory.SERVICES['TicTacToe'].player_two.interact("The game has ended!")
    exit(0)