from zdiscord.service.messaging.Events import IEvent

async def send_message(msg: str,event: IEvent):
    await event.context['message_object'].channel.send(msg)