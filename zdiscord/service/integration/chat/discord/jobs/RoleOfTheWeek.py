from zdiscord.util.general.Job import Job
from zdiscord.service.integration.chat.discord.DiscordClient import DiscordBot
import time
import discord

class RoleOfTheWeekJob(Job):

    def __init__(self, name: str, interval: str, length: int):
        Job.__init__(self, name, interval, length)

    def execute_job(self):
        bot: RoleOfTheWeekBot = RoleOfTheWeekBot(self.context['channel'])
        bot.run(self.context['token'])


class RoleOfTheWeekBot(DiscordBot):

    __HARD_CODED_ROUTINES: dict

    def __init__(self, channel_to_send: str):
        DiscordBot.__init__(self, eventPusher=None)
        self.channel = channel_to_send


    async def on_ready(self):
        self._logger("Start up role of the week bot!")

    async def on_message(self, message: discord.Message):
        pass

    async def on_voice_state_update(self, member, before, after):
        pass

    async def on_reaction_add(self, reaction, user):
        return

    async def on_reaction_remove(self, reaction, user):
        return
