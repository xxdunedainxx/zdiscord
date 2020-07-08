from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.messaging.Events import IEvent

async def get_weather_and_send_it(town: str, event: IEvent):
    weather_info: str = ServiceFactory.SERVICES['weather'].get_and_format(town)

    await event.context['message_object'].channel.send(weather_info)

