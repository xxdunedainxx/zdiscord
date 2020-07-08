from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.messaging.Events import IEvent

async def get_giphy_and_send_it(query: str, event: IEvent):
    giphy: str = ServiceFactory.SERVICES['giphy'].get_giphy(query)

    await event.context['message_object'].channel.send(giphy)

