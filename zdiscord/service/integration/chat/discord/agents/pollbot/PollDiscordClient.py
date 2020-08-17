from zdiscord.service.integration.chat.discord.DiscordClient import DiscordBot
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.service.integration.chat.discord.DiscordEventMiddleware import DiscordEvent
import discord
import base64

class VotingOption:
  def __init__(self, emoji: str, sentiment: str, raw_value: str):
    self.emoji = emoji
    self.sentiment = sentiment
    self.raw_value: str = raw_value


class PollDiscordClient(DiscordBot):

    __HARD_CODED_ROUTINES: dict

    def __init__(self, eventPusher, context: {} = None, options: {} = None):
      DiscordBot.__init__(self, eventPusher=eventPusher)

      # Push events to client middleware
      self.event_pusher = eventPusher
      self.event_pusher(DiscordEvent(type='test'))
      self.context = context
      self.raw_options = options
      self.owner: discord.User
      self.options: [VotingOption] = {}
      self.__POLL_MESSAGE: discord.Message

      # Used to track number of reactions
      self.submissions: {} = {}
      self.uid_submissions: [int] = []

    def poll_start_message(self) -> str:
      msg: str= (
        f"""--------------\n"""\
        f"""**Poll \'{self.name}\'**\n"""\
        f"""Started by: {self.owner.name}\n"""\
        f"""--------------\n"""\
        f"""Below are valid options:\n"""
      )

      i = 1
      for option in self.options.keys():
        msg+=f"{i}) {self.options[option].emoji}={self.options[option].sentiment}\n"
        i+=1

      return msg

    def poll_end_message(self):
      msg: str = (
        f"""--------------\n"""\
        f"""**\'{self.name}\' POLL RESULTS**\n"""\
        f"""\n"""\
      )
      for submission in self.submissions.keys():
        msg+=f"{self.options[submission].emoji} SCORED A TOTAL OF {self.submissions[submission]}\n"

      return msg


    async def close_out(self):
      await self.channel.send(f"{self.poll_end_message()}")

      exit(0)

    async def on_ready(self):
      self._logger.info(f"Logged on as {self.user}")
      self.owner =  await self.fetch_user(user_id=self.context['context']['User']['id'])
      self.name = self.context['parsed_message']

      # Set up options
      for option in self.raw_options:
        self.options[option['raw_value']]=VotingOption(emoji=option['emoji'], sentiment=option['sentiment'], raw_value=option['raw_value'])
        self.submissions[option['raw_value']] = 0

      try:
        self.channel = await self.fetch_channel(channel_id=self.context['context']['channel'])
      except Exception as e:
        self.channel = discord.utils.get(self.get_all_channels(), id=self.context['context']['channel'])

      self.__POLL_MESSAGE: discord.Message = await self.channel.send(f"{self.poll_start_message()}")
      return

    async def on_message(self, message: discord.Message):
      # Only interact w/ poll owner
      if message.author != self.owner:
        return
      else:
        try:
          message = self.clean_message(message)
          if 'close poll' in message.content.lower():
            self._logger.info("ending poll and printing results")
            await self.close_out()
        except Exception as e:
          self._logger.error(msg=f"BAD ERROR \n{errorStackTrace(e)}")

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
      try:
        eval_reaction: str = self.eval_reaction(discordReaction=payload)

        message: discord.Message = await self.http.get_message(channel_id=self.__POLL_MESSAGE.channel.id, message_id=self.__POLL_MESSAGE.id)

        if payload.user_id in self.uid_submissions:
          await self.http.remove_reaction(channel_id=self.__POLL_MESSAGE.channel.id, message_id=self.__POLL_MESSAGE.id, emoji=payload.emoji.name, member_id=payload.user_id)

        if eval_reaction != '':
          self.submissions[eval_reaction]+=1
          self.uid_submissions.append(payload.user_id)

      except Exception as e:
        self._logger.warning(f"Issue parsing emoji: {errorStackTrace(e)}")

    async def on_raw_reaction_remove(self,  payload: discord.RawReactionActionEvent):
      try:
        eval_reaction: str = self.eval_reaction(discordReaction=payload)

        if eval_reaction != '':
          self.submissions[eval_reaction] -= 1
          if payload.user_id in self.uid_submissions:
            self.uid_submissions.remove(payload.user_id)

      except Exception as e:
        self._logger.warning(f"Issue parsing emoji: {errorStackTrace(e)}")

    def eval_reaction(self, discordReaction: discord.RawReactionActionEvent) -> str:
      reaction: str = str(discordReaction.emoji.name.encode('utf-8'), encoding='utf-8')
      if discordReaction.message_id != self.__POLL_MESSAGE.id:
        return ''
      else:
        if reaction in self.options.keys():
          self._logger.info('Valid emoji added.')
          return reaction
        else:
          return ''