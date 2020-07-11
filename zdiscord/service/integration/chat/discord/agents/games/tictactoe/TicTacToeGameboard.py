import random

class Player:
  def __init__(self, name: str, symbol: str):
    self.name = name
    self.symbol = symbol

  # Cli input
  def input(self):
    m=Move(input=input("Please provide a move:"), owner=self)
    return m
  # Cli interaction
  def interact(self, msg: str):
    print(msg)

class AIPlayer(Player):
  def __init__(self, symbol: str):
    Player.__init__(self, name='ALL_POWERFULE_AI', symbol=symbol)

  # Cli interaction
  def interact(self, msg: str):
    # No-op for bots
    pass

  # randomized
  def input(self):
    return Move(input=f"{random.randint(0, 2)},{random.randint(0, 2)}", owner=self)

class RealPlayer(Player):
  def __init__(self, name: str, symbol: str):
    Player.__init__(self, name, symbol=symbol)

class Move:

  def __init__(self, input: str, owner: Player):
    self.x_quadrant: int = int(input.split(',')[0]) if ',' in input else -1
    self.y_quadrant: int = int(input.split(',')[1]) if ',' in input else -1

    self.symbol: str = owner.symbol
    self.owner: Player = owner

class TicTacToeGameboard:

  @staticmethod
  def game_loop(game):
    game.start_game()
    user_input=input("Keep playing?[Y/N]")

    while user_input.lower() != 'n':
      if user_input.lower() != 'y':
        user_input = input("Keep playing?[Y/N]")
      else:
        game.clear_board()
        game.start_game()

  @staticmethod
  def start_two_player_game(playerOne, playerTwo):
    game=TicTacToeGameboard(
      playerOne=RealPlayer(name=playerOne, symbol=TicTacToeGameboard.X_MOVE),
      playerTwo=RealPlayer(name=playerTwo, symbol=TicTacToeGameboard.X_MOVE)
    )

    TicTacToeGameboard.game_loop(game)

  @staticmethod
  def start_ai_game(username: str):
    game=TicTacToeGameboard(
      playerOne=RealPlayer(name=username, symbol=TicTacToeGameboard.X_MOVE),
      playerTwo=AIPlayer(symbol=TicTacToeGameboard.O_MOVE)
    )

    TicTacToeGameboard.game_loop(game)

  X_MOVE = 'x'
  O_MOVE = 'O'
  BLANK = '+'

  def __init__(self, playerOne: Player, playerTwo: Player):
    self.player_one: Player = playerOne
    self.player_two: Player = playerTwo

    self.game_is_live: bool = True

    self.ORIGINAL_GAME_BOARD: [] = [
      [TicTacToeGameboard.BLANK, TicTacToeGameboard.BLANK, TicTacToeGameboard.BLANK],
      [TicTacToeGameboard.BLANK, TicTacToeGameboard.BLANK, TicTacToeGameboard.BLANK],
      [TicTacToeGameboard.BLANK, TicTacToeGameboard.BLANK, TicTacToeGameboard.BLANK],
    ]

    self.GAME_BOARD: [] = self.ORIGINAL_GAME_BOARD.copy()

  def clear_board(self):
    self.GAME_BOARD: [] = self.ORIGINAL_GAME_BOARD.copy()

  def print_board(self):
    return (
      f""".-------.\n"""\
      f"""| {'-'.join(self.GAME_BOARD[0])} |\n""" \
      f"""| {'-'.join(self.GAME_BOARD[1])} |\n""" \
      f"""| {'-'.join(self.GAME_BOARD[2])} |\n"""\
      f""".-------."""
      )

  def start_game(self):
    while self.game_is_live:
      self.player_one.interact(msg=f"Current board\n{self.print_board()}")

      move_one=self.player_one.input()

      self.interact(move_one)

      self.player_two.interact(msg=f"Current board\n{self.print_board()}")

      move_two=self.player_two.input()

      self.interact(move_two)

  def interact(self, move: Move) -> str:

    while self._is_valid_move(move) is False:
      move.owner.interact(f"Invalid move provided! Please provide input in the form X,Y, and in an empty space.\n{self.print_board()}")
      move = move.owner.input()

    self._move(move=move)
    game_result: str = self._evaluate_game(player=self.player_one)

    if self.game_is_live == False:
      move.owner.interact(f"Winner! {game_result}\n{self.print_board()}")
      return

    game_result: str = self._evaluate_game(player=self.player_two)

    if self.game_is_live == False:
      move.owner.interact(f"Winner! {game_result}")
      return


  def _move(self, move: Move):
    self.GAME_BOARD[move.y_quadrant][move.x_quadrant] = move.symbol

  def _is_valid_move(self, move: Move) -> bool:
    return(
      (0 <= move.x_quadrant <= 2) and
      (0 <= move.y_quadrant <= 2) and
      (move.symbol == TicTacToeGameboard.X_MOVE or move.symbol == TicTacToeGameboard.O_MOVE) and
      self.GAME_BOARD[move.y_quadrant][move.x_quadrant] == TicTacToeGameboard.BLANK
    )

  def _evaluate_game(self, player: Player) -> str:
    # Test paths from every corner

    # top left
    eval=self.__evaluate_all_paths(0, 0, player.symbol)
    if eval != '':
      return player.name

    eval=self.__evaluate_all_paths(0, 2,player.symbol)
    if eval != '':
      return player.name

    eval=self.__evaluate_all_paths(2, 0,player.symbol)
    if eval != '':
      return player.name

    eval=self.__evaluate_all_paths(2, 2,player.symbol)
    if eval != '':
      return player.name

  def __bound_check(self, x, y):
    c1=(x >= 0 and y >= 0)
    c2=x < len(self.GAME_BOARD) and y < len(self.GAME_BOARD)
    return c1 and c2

  def __eval_for_last_position(self,posX, posY, charToSearch: str) -> bool:
    # reached bound, found winner
      return (
              self.GAME_BOARD[posY][posX] == charToSearch
              )

  def __evaluate_all_paths(self, x, y, character_to_eval) -> str:
    if self.GAME_BOARD[y][x] == TicTacToeGameboard.BLANK:
      return ''
    else:
      current_x = x
      current_y = y

      # Check right
      eval=(self.GAME_BOARD[current_y][current_x] == character_to_eval)
      current_char=self.GAME_BOARD[current_y][current_x]
      valid_checks = 0
      while self.__bound_check(current_x, current_y) and self.GAME_BOARD[current_y][current_x] == character_to_eval:
        if self.__eval_for_last_position(current_x, current_y, character_to_eval) and valid_checks == len(self.GAME_BOARD[0]) - 1:
          self.game_is_live = False
          return character_to_eval
        else:
          valid_checks+=1
          current_x+=1
      # check up
      current_x = x
      current_y = y
      valid_checks = 0
      while self.__bound_check(current_x, current_y) and self.GAME_BOARD[current_y][current_x] == character_to_eval:
        if self.__eval_for_last_position(current_x, current_y, character_to_eval) and valid_checks == len(self.GAME_BOARD[0]) - 1:
          self.game_is_live = False
          return character_to_eval
        else:
          valid_checks += 1
          current_y-=1

      # check down
      current_x = x
      current_y = y
      valid_checks = 0
      while self.__bound_check(current_x, current_y) and self.GAME_BOARD[current_y][current_x] == character_to_eval:
        if self.__eval_for_last_position(current_x, current_y, character_to_eval) and valid_checks == len(self.GAME_BOARD[0]) - 1:
          self.game_is_live = False
          return character_to_eval
        else:
          valid_checks += 1
          current_y+=1

      # check left?
      current_x = x
      current_y = y
      valid_checks = 0
      while self.__bound_check(current_x, current_y) and self.GAME_BOARD[current_y][current_x] == character_to_eval:
        if self.__eval_for_last_position(current_x, current_y, character_to_eval) and valid_checks == len(self.GAME_BOARD[0]) - 1:
          self.game_is_live = False
          return character_to_eval
        else:
          valid_checks += 1
          current_x-=1

      # check diagonal
      current_x = x
      current_y = y
      valid_checks = 0
      while self.__bound_check(current_x, current_y) and self.GAME_BOARD[current_y][current_x] == character_to_eval:
        if self.__eval_for_last_position(current_x, current_y, character_to_eval) and valid_checks == len(self.GAME_BOARD[0]) - 1:
          self.game_is_live = False
          return character_to_eval
        else:
          valid_checks += 1
          current_y+=1
          current_x+= 1
