from zdiscord.service.integration.chat.IChatClient import IChatClient
from zdiscord.service.messaging.MessageFactory import MessageFactory
from zdiscord.service.messaging.VoiceFactory import VoiceFactory
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.service.integration.chat.discord.voice.DiscordVoice import DiscordVoice
import requests
import discord

class DiscordBot(discord.Client, IChatClient):

    __HARD_CODED_ROUTINES: dict

    def __init__(self, messager: MessageFactory, voice: VoiceFactory ):
        IChatClient.__init__(self, name='DiscordBot')
        discord.Client.__init__(self)

        self.__mf: MessageFactory = messager
        self.__vf: VoiceFactory = voice
        self.__voice_client: DiscordVoice = None
        self.__current_voice_channel: discord.VoiceChannel = None

        self.__HARD_CODED_ROUTINES: dict = {
            'connect': {
                'description': 'Connect the voice bot to a voice channel. It will play a random video once it joins',
                'example': 'connect Team Rheem',
                'method': self.connect_voice_channel_routine,
            },
            'disconnect': {
                'description': 'disconnects bot from voice',
                'example': 'disconnect',
                'method':   self.disconnect_voice,
            },
            'help': {
                'method': self.help_msg
            },
        }
    # TODO : 'init_voice_client()'

    async def on_ready(self):
        self.__voice_client = DiscordVoice(bot=self, ffmpeg=self.__vf.ffmpeg)
        print(f"Logged on as {self.user}")
        self._logger.info(f"Logged on as {self.user}")

    async def on_message(self, message: discord.Message):
        message_crafter: str = ''
        # don't respond to ourselves
        if message.author == self.user:
            return
        #else:
        else:
            try:
                await self.process_msg(message)
            except Exception as e:
                await message.channel.send(f"Something really bad happened :(")
                self._logger.error(msg=f"{errorStackTrace(e)}")

    # TODO 'onjoin' python config
    async def on_voice_state_update(self, member, before, after):
        if member.name == self.user or member.bot is True or self.__current_voice_channel is None:
            return
        else:
            busters: discord.Guild = self.guilds[0]
            await self.__voice_client.stream(ctx=busters, url=self.__vf.fetch_stream_link())
    async def process_msg(self, message: discord.Message):
        if self.is_at_mention(message.content):
            parsed_msg: str = message.content.split(f"{self.get_at_mention()}")[1].strip(' ')
        elif type(message.channel) is discord.DMChannel:
            parsed_msg: str = message.content
        else:
            return
        self._logger.info(parsed_msg)
        # TODO do pre process msg better
        cmd: str = self.parse_cmd(message=message)
        parsed_msg: str = self.parse_msg(cmd, message.content)
        if cmd == '':
            return
        elif cmd in self.__HARD_CODED_ROUTINES.keys():
            await self.__HARD_CODED_ROUTINES[cmd]['method'](parsed_msg, message)
        elif cmd not in self.__mf.fetch_config().keys():
            await message.channel.send(f"{self.__mf.fetch_config()['default'].rmsg}\n\n Please type \'{self.get_at_mention()} help\' for more information on how to properly utilize my functions.")
        else:
            pre_process_msg: str = self.__mf.send_await_msg(cmd=cmd, msg=parsed_msg)
            if pre_process_msg is not None:
                await message.channel.send(pre_process_msg)
            await message.channel.send(self.__mf.process_response(cmd=cmd, msg=parsed_msg))

    def parse_cmd(self, message: discord.Message) -> str:
        try:
            if self.is_at_mention(msg=message.content):
                message.content=message.content.replace(f"{self.get_at_mention()} ", '')

            if ' ' in message.content:
                return message.content.split(' ')[0]
            else:
                return message.content
        except Exception as e:
            return 'default'

    def parse_msg(self,cmd: str, msg: str) -> str:
        try:
            return msg.replace(f"{cmd} ",'')
        except Exception as e:
            return 'default'

    def get_at_mention(self) -> str:
        return f"<@!{str(self.user.id)}>"

    def is_at_mention(self, msg: str) -> bool:
        return f"{self.get_at_mention()} " in msg

    async def connect_voice_channel_routine(self, channel: str, message: discord.Message):
        if self.__voice_client is None:
            self._logger.warn("Voice client is not configured, sending msg back to user..")
            message.channel.send("I am not configured properly to use voice!!")

        print("request to join channel")
        busters: discord.Guild = self.guilds[0]
        channel_to_join: discord.VoiceChannel = self.get_voice_channel(channel)
        if channel_to_join:
            self.__current_voice_channel = channel_to_join
            await message.channel.send(f"Joining channel...")
            await self.__voice_client.join(ctx=busters, channel=channel_to_join)
            await self.__voice_client.stream(ctx=busters, url=self.__vf.fetch_stream_link())
        else:
            await message.channel.send(f"Unable to join voice channel \"{channel}\"")

    async def disconnect_voice(self, channel: str, message: discord.Message):
        busters: discord.Guild = self.guilds[0]
        if self.__current_voice_channel:
            await self.__voice_client.leave(busters)
            await message.channel.send(f"Disconnected from {self.__current_voice_channel.name}")
            self.__current_voice_channel = None
        else:
            await message.channel.send(f"Not currently connected to a voice channel.")

    async def help_msg(self, no_op, message: discord.Message):
        self._logger.info(f"User \'{message.author.name}\' does not know what to do :(")

        help_msg_builder: str = 'See the below supported commands and their usage:\n'
        message_config: dict = self.__mf.fetch_config()

        help_msg_builder+='\nCUSTOM BUILT COMMANDS:\n'

        for msg in message_config.keys():
            if msg == 'default':
                continue
            elif message_config[msg].description is not None and message_config[msg].example is not None:
                help_msg_builder+=f"\n--- {msg}  ---\n"
                help_msg_builder+=f"Description: {message_config[msg].description}\n"
                help_msg_builder+=f"Example Usage: {message_config[msg].example}\n"

        help_msg_builder += '\nPRE BUILT COMMANDS:\n'
        for cmd in self.__HARD_CODED_ROUTINES.keys():
            if cmd == 'help':
                continue
            else:
                help_msg_builder += f"\n--- {cmd}  ---\n"
                help_msg_builder += f"Description: {self.__HARD_CODED_ROUTINES[cmd]['description']}\n"
                help_msg_builder += f"Example Usage: {self.__HARD_CODED_ROUTINES[cmd]['example']}\n"

        help_msg_builder+=f"\nNote: for channels you must '@' mention the bot to get any of the above commands to work. For example \'{self.get_at_mention()} ping\'\n"
        help_msg_builder+="If you direct message the bot, you do not have to '@' mention the bot."

        await message.channel.send(help_msg_builder)

    def get_voice_channel(self, channel: str) -> discord.VoiceChannel:
        busters: discord.Guild = self.guilds[0]
        print("getting channels")
        channels: [discord.VoiceChannel] = busters.voice_channels
        chan: discord.VoiceChannel = None
        for ch in channels:
            print("checking channel...")
            if ch.name == channel:
                return ch
        return None
