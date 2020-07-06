from zdiscord.service.messaging.MessageFactory import MessageFactory

class DiscordMessageMiddleware(MessageFactory):
    def __init__(self, confLocation: str):
        super().__init__(confLocation=confLocation)

    # TODO maybe do some of the message parsing in message factory???
    def parse_cmd(self, message: discord.Message) -> str:
        try:
            if self.is_at_mention(msg=message.content):
                message.content = message.content.replace(f"{self.get_at_mention()} ", '')

            if ' ' in message.content:
                return message.content.split(' ')[0]
            else:
                return message.content
        except Exception as e:
            return 'default'


    # TODO maybe do some of the message parsing in message factory???
    def parse_msg(self, cmd: str, msg: str) -> str:
        try:
            return msg.replace(f"{cmd} ", '')
        except Exception as e:
            return 'default'


    def get_at_mention(self) -> str:
        return f"<@!{str(self.user.id)}>"


    def is_at_mention(self, msg: str) -> bool:
        return f"{self.get_at_mention()} " in msg

    async def process_msg(self, message: discord.Message):
        # TODO maybe do some of the message parsing in message factory???
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