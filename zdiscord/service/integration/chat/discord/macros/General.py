from zdiscord.service.messaging.Events import IEvent

async def help_msg(help_msg: str,event: IEvent):
    await event.context['message_object'].channel.send(help_msg)