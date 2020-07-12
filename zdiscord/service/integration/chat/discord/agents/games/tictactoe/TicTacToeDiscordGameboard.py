from zdiscord.service.integration.chat.discord.agents.games.tictactoe.TicTacToeGameboard import TicTacToeGameboard,AIPlayer,RealPlayer, Player, Move
from zdiscord.service.integration.chat.discord.DiscordEvents import DiscordEvent
import discord

class DiscordPlayer(RealPlayer):
  def __init__(self, name: str, symbol: str, discordUser: discord.User):
    RealPlayer.__init__(self, name, symbol=symbol)

    self.discord_user = discordUser

  # Discord API interaction
  async def interact(self, msg: str):
    await self.discord_user.send(msg)

class DiscordTicTacToeGameboard(TicTacToeGameboard):

  def __init__(self, playerOne: Player, playerTwo: Player, channel: discord.abc.Messageable):
    TicTacToeGameboard.__init__(self, playerOne, playerTwo)

    self.current_player: Player = playerOne
    self.channel = channel

  async def discord_event(self, event: DiscordEvent):
    if type(self.current_player) is not DiscordPlayer:
      return

    if event.serialized_context['User']['id'] == self.current_player.discord_user.id:
      move=Move(event.parsed_message, owner=self.current_player)
      await self.interact(move)
    else:
      return
      # DM user that its not their turn

  async def swap_players(self):
    if self.current_player == self.player_one:
      self.current_player = self.player_two
    else:
      self.current_player = self.player_one

    if type(self.current_player) is AIPlayer:
      move=self.current_player.input()
      await self.interact(move)
    else:
      await self.current_player.interact(f"Your move! current board:\n{self.print_board()}")

  async def interact(self, move: Move) -> str:

    if self._is_valid_move(move) is False:
      if type(move.owner) is not AIPlayer:
        await self.current_player.interact(f"Invalid move provided! Please provide input in the form X,Y, and in an empty space.\n{self.print_board()}")
        return
      else:
        move = self.current_player.input()
        while self._is_valid_move(move) == False:
          move = self.current_player.input()

    self._move(move=move)
    game_result: str = self._evaluate_game(player=self.player_one)

    if self.game_is_live == False:
      await self.channel.send(f"Winner! {game_result}\n{self.print_board()}")
      exit(0)

    game_result: str = self._evaluate_game(player=self.player_two)

    if self.game_is_live == False:
      await self.channel.send(f"Winner! {game_result}")
      exit(0)

    if type(move.owner) is not AIPlayer:
      await self.channel.send(f"**{self.player_one.name} vs {self.player_two.name}**\nCurrent Board\n{self.print_board()}")

    await self.swap_players()

