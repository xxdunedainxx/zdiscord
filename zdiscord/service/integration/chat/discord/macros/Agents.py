from zdiscord.service.ThreadQ import ThreadQueue, ThreadQueueObject
from zdiscord.service.messaging.Events import IEvent

async def queue_up_agent(agent_name: str, event: IEvent):
    ThreadQueue.add_thread(ThreadQueueObject(name=agent_name, context=event.serialize()))