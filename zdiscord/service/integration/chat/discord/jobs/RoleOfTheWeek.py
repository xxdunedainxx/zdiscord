from zdiscord.util.general.Job import Job
from zdiscord.service.integration.chat.discord.DiscordClient import DiscordBot
from zdiscord.service.Service import Service
import time
from multiprocessing import Process
from zdiscord.util.general.JobQ import RUNNING_JOBS
from zdiscord.util.logging.LogFactory import LogFactory
import discord
import random
import asyncio

class RoleOfTheWeekJob(Job):

    @staticmethod
    def run_role_of_the_week_job(conf: {}):
        print("running role of the week job!")

        LogFactory.log_dir = conf['log_dir'] if 'log_dir' in conf.keys() else LogFactory.log_dir
        LogFactory.log_level = conf['log_level'] if 'log_level' in conf.keys() else LogFactory.log_level
        LogFactory.log_stdout = conf['log_stdout'] if 'log_stdout' in conf.keys() else LogFactory.log_stdout

        bot: RoleOfTheWeekBot = RoleOfTheWeekBot(conf['channel'], conf['roles'])
        bot.run(conf['token'])

    def __init__(self, name: str, interval: str, length: int, conf: {}, enabled: bool):
        Job.__init__(self, name, interval, length, conf, enabled)
        asyncio.set_event_loop(asyncio.new_event_loop())

    def execute_job(self,conf):
        print("running role of the week job!")

        LogFactory.log_dir = conf['log_dir'] if 'log_dir' in conf.keys() else LogFactory.log_dir
        LogFactory.log_level = conf['log_level'] if 'log_level' in conf.keys() else LogFactory.log_level
        LogFactory.log_stdout = conf['log_stdout'] if 'log_stdout' in conf.keys() else LogFactory.log_stdout

        bot: RoleOfTheWeekBot = RoleOfTheWeekBot(conf['channel'], conf['roles'])
        bot.run(conf['token'])


    def job_is_alive(self) -> bool:
        return self.job_reference.is_alive()

    def kill_job(self) -> None:
        if self.job_reference.is_alive():
            self.job_reference.kill()

class Role:
    def __init__(self, name: str):
        self.name = name

class UserRole:
    def __init__(self, role: Role, user: discord.User):
        self.role = role
        self.user = user


class RoleOfTheWeekBot(DiscordBot, Service):

    __HARD_CODED_ROUTINES: dict

    def __init__(self, channel_to_send: str, roles: [str] = None):
        Service.__init__(self, name=self.__class__.__name__)
        DiscordBot.__init__(self, eventPusher=None)

        self.channel = channel_to_send
        self.roles: [Role] = []

        self.__init_roles(roles=roles)

    def __init_roles(self, roles: str):
        for role in roles:
            self.roles.append(Role(name=role))

    async def end_job(self):
      self._logger.info("Ending job")
      exit(0)

    async def role_of_the_week_message(self, roles: [UserRole], channel: discord.TextChannel):
        for role in roles:
            await channel.send(f"And the \'{role.role.name}\' goes to...")
            #time.sleep(3)
            await channel.send(f"{role.user.mention}!! :partying_face:")

    async def on_ready(self) -> None:
        self._logger.info(f"Logged on as {self.user}")
        await self.role_of_the_week()
        await self.end_job()

    async def role_of_the_week(self) -> None:
        users: [discord.User] = self.users
        self._logger.info("will randomly call out roles")

        roles_assigned: [UserRole] = []

        for role in self.roles:
            roles_assigned.append(UserRole(role=role, user=users[random.randint(0, len(users) - 1)]))
        self._logger.info(f"Roles: {roles_assigned}")

        genChannel: discord.TextChannel = None
        targetChannel: discord.TextChannel = None

        for channel in self.get_all_channels():
            if channel.name == self.channel:
                targetChannel = channel
            elif channel.name == 'general':
                genChannel = channel
            else:
                continue
        if targetChannel is not None:
            await self.role_of_the_week_message(roles_assigned, targetChannel)
        elif genChannel is not None:
            await self.role_of_the_week_message(roles_assigned, genChannel)


    async def on_message(self, message: discord.Message):
        pass