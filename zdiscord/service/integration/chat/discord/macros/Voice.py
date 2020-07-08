from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.messaging.Events import IEvent

async def connect_to_a_channel(channel: str, event: IEvent):
    await event.context['message_object'].channel.send(f"Connecting to {channel}")

    await ServiceFactory.SERVICES['voice'].connect_voice_channel_routine(channel, event.context['message_object'])

async def disconnect_from_a_channel(event: IEvent):
    if ServiceFactory.SERVICES['voice'].current_voice_channel is None:
        event.context['message_object'].channel.send("Not currently in a channel")
    else:
        await event.context['message_object'].channel.send(f"Disconnecting from {ServiceFactory.SERVICES['voice'].current_voice_channel}")

        await ServiceFactory.SERVICES['voice'].disconnect_voice()

async def stream_random_audio(event: IEvent):
    await ServiceFactory.SERVICES['voice'].random_audio()