from zdiscord.service.integration.chat.discord.DiscordClient import DiscordBot
from zdiscord.service.integration.chat.IChatClient import IChatClient
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.service.integration.chat.discord.DiscordEventMiddleware import DiscordEvent
import discord

class TicTacToeDiscordClient(DiscordBot):

    __HARD_CODED_ROUTINES: dict

    def __init__(self, eventPusher, context: {} = None):
      DiscordBot.__init__(self, eventPusher=eventPusher)

      # Push events to client middleware
      self.event_pusher = eventPusher
      self.event_pusher(DiscordEvent(type='test'))
      self.context = context
      self.player_one: discord.User
      self.player_two: discord.User
      self.original_msg: discord.Message

      self.is_ready = False

    async def on_ready(self):
      self._logger.info(f"Logged on as {self.user}")
      self.player_one =  await self.fetch_user(user_id=self.context['context']['User']['id'])

      if 'player_two' in self.context['context'].keys():
        await self.fetch_user(self.context['context']['player_two'])
      else:
        self.player_two = None

      try:
        self.channel = await self.fetch_channel(channel_id=self.context['context']['channel'])
      except Exception as e:
        self.channel = discord.utils.get(self.get_all_channels(), id=self.context['context']['channel'])

      await self.channel.send('Game has started!')

      event_to_push: DiscordEvent = DiscordEvent(type='on_ready')

      event_to_push.context = {
        'players':{
          'player_one' : self.player_one,
          'player_two' : self.player_two
        }
      }
      await self.event_pusher(event_to_push)

      self.is_ready = True

    async def on_message(self, message: discord.Message):
      if self.is_ready == False:
        return
      
      message = self.clean_message(message)

      # Only interact w/ game owner
      if message.author != self.player_one or (self.player_two is not None and message.author != self.player_two):
        return
      else:
        try:
          await self.event_pusher(DiscordEvent(
            type='on_message',
            context={'message_object' : message},
            serialized_context={
              'User': self._serialize_user(message.author),
              'message_id': message.id,
              'channel': message.channel.id})
          )
        except Exception as e:
          self._logger.error(msg=f"BAD ERROR \n{errorStackTrace(e)}")

