from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.messaging.Events import IEvent

async def get_stock_and_send_it(STOCK: str, event: IEvent):
    stock_info: str = ServiceFactory.SERVICES['alphav'].get_stock_info(STOCK)

    await event.context['message_object'].channel.send(stock_info)

