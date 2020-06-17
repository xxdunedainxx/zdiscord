from zdiscord.service.integration.chat.IChatClient import IChatClient
from zdiscord.service.messaging.MessageFactory import MessageFactory
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.service.integration.chat.discord.voice.DiscordVoice import DiscordVoice
import requests
import discord

class DiscordBot(discord.Client, IChatClient):

    def __init__(self, messager: MessageFactory ):
        IChatClient.__init__(self, name='DiscordBot')
        discord.Client.__init__(self)

        self.__mf: MessageFactory = messager
        self.__voice_client: DiscordVoice = None
    # TODO : 'init_voice_client()'

    async def on_ready(self):
        busters: discord.Guild = self.guilds[0]
        print("getting channels")
        channels: [discord.VoiceChannel] = busters.voice_channels
        chan: discord.VoiceChannel = None
        for ch in channels:
            print("checking channel...")
            if ch.name == 'Team Rheem':
                chan = ch
                break

        self.__voice_client = DiscordVoice(bot=self)
        await self.__voice_client.join(ctx=busters, channel=chan)

        print(f"Logged on as {self.user}")
        self._logger.info(f"Logged on as {self.user}")

    async def on_message(self, message: discord.Message):
        message_crafter: str = ''
        # don't respond to ourselves
        # TODO : configurable routing logic
        if message.author == self.user:
            return
        elif type(message.channel) is discord.DMChannel:
            self._logger.info(message.content)
            pre_process_msg: str = self.__mf.send_await_msg(msg=message.content)
            if pre_process_msg is not None:
                await message.channel.send(pre_process_msg)
            await message.channel.send(self.__mf.process_response(message.content))
        #else:
        elif f"<@!{str(self.user.id)}>" in message.content:
            # TODO Make message parsing less shity
            try:
                parsed_msg: str = message.content.split(f"<@!{str(self.user.id)}>")[1].strip(' ')
                print(parsed_msg)
                self._logger.info(parsed_msg)
                # TODO do pre process msg better
                pre_process_msg: str = self.__mf.send_await_msg(msg=parsed_msg)
                if pre_process_msg is not None:
                    await message.channel.send(pre_process_msg)
                await message.channel.send(self.__mf.process_response(parsed_msg))
            except Exception as e:
                await message.channel.send(f"Something reall bad happened :(")
                self._logger.error(msg=f"{errorStackTrace(e)}")
        else:
            self._logger.info("not mentioned. Skipping")
            print("not mentioned. Skipping")

    # TODO 'onjoin' python config
    async def on_voice_state_update(self, member, before, after):
        if member.name == self.user or member.bot is True:
            return
        if after.channel != None:
            busters: discord.Guild = self.guilds[0]
            await self.__voice_client.stream(ctx=busters, url="https://www.youtube.com/embed/kYXRfwXfz5A")  # "https://youtu.be/EBudj01e9OY")