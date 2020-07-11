from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.messaging.Events import IEvent

async def tic_tac_toe_move(event: IEvent):
    await ServiceFactory.SERVICES['TicTacToe'].discord_event(event)