from zdiscord.service.integration.chat.discord.DiscordClient import DiscordBot
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.service.integration.chat.discord.DiscordEventMiddleware import DiscordEvent
import discord

class VotingOption:
  def __init__(self, emoji: str, sentiment: str):
    self.emoji = emoji
    self.sentiment = sentiment


class PollDiscordClient(DiscordBot):

    __HARD_CODED_ROUTINES: dict

    def __init__(self, eventPusher, context: {} = None):
      DiscordBot.__init__(self, eventPusher=eventPusher)

      # Push events to client middleware
      self.event_pusher = eventPusher
      self.event_pusher(DiscordEvent(type='test'))
      self.context = context
      self.owner: discord.User
      self.options: [VotingOption] = []

    def poll_start_message(self) -> str:
      msg: str= (
        f"""**Poll \'{self.name}\', started by {self.owner.name}\n"""\
        f"""Below are valid options"""
      )

      for option in self.options:
        msg+=f"{option.emoji}={option.sentiment}"

      return msg

    async def on_ready(self):
      self._logger.info(f"Logged on as {self.user}")
      self.owner =  await self.fetch_user(user_id=self.context['context']['User']['id'])
      self.name = self.context['context']['pollname']

      # Set up options
      for option in self.context['context']['options']:
        self.options+=VotingOption(emoji=option['emoji'], sentiment=option['sentiment'])

      try:
        self.channel = await self.fetch_channel(channel_id=self.context['context']['channel'])
      except Exception as e:
        self.channel = discord.utils.get(self.get_all_channels(), id=self.context['context']['channel'])

      await self.channel.send(f"{self.poll_start_message()}")

    async def on_message(self, message: discord.Message):
      # Only interact w/ poll owner
      if message.author != self.owner:
        return
      else:
        try:
          if 'poll close' in message.content.lower():
            print("ending poll and printing results")
        except Exception as e:
          self._logger.error(msg=f"BAD ERROR \n{errorStackTrace(e)}")

      async def on_reaction_add(self, reaction, user):
        pass

      async def on_reaction_remove(self, reaction, user):
        pass

