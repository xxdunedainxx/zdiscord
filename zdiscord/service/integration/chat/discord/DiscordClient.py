from zdiscord.service.integration.chat.IChatClient import IChatClient
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.service.integration.chat.discord.DiscordEventMiddleware import DiscordEvent
import discord


class DiscordBot(discord.Client, IChatClient):

    __HARD_CODED_ROUTINES: dict

    def __init__(self, eventPusher):
        IChatClient.__init__(self, name='DiscordBot')
        discord.Client.__init__(self)

        # Push events to client middleware
        self.event_pusher = eventPusher

    def clean_message(self, message: discord.Message) -> discord.Message:
        message.content = message.content.lower()
        return message

    async def on_ready(self):
        #self.__voice_client = DiscordVoice(bot=self, ffmpeg=self.__vf.ffmpeg)
        self._logger.info(f"Logged on as {self.user}")
        await self.event_pusher(DiscordEvent(type='on_ready'))


    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        else:
            try:
                message=self.clean_message(message)
                await self.event_pusher(DiscordEvent(type='on_message', context={'message_object' : message}, serialized_context={'User': self._serialize_user(message.author), 'message_id': message.id, 'channel': message.channel.id}))
            except Exception as e:
                self._logger.error(msg=f"BAD ERROR \n{errorStackTrace(e)}")

    async def on_voice_state_update(self, member, before, after):
        if member.name == self.user or member.bot is True:
            return
        else:
            await self.event_pusher(DiscordEvent(type='on_voice_state_update', context={'member': member, 'before': before, 'after': after}))

    async def on_reaction_add(self, reaction, user):
        return

    async def on_reaction_remove(self, reaction, user):
        return

    def _serialize_user(self, user: discord.User) -> {}:
        return {
            'name': user.name,
            'id' : user.id,
        }

