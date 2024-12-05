# Player (name: str, id: str)
# Move: (x: int, y: int, player: smallint (-1, 1))
# Board (_moves: set[move] / dict[(x , y), player], _gameWon: bool, _boardEmpty: bool, _rowSum: list[int], _colsum: list[int], _diagsum: int, _crossdiagsum: int, _emptyCells: int)
# Game: (_board: Board, _Player1: Player, _Player2: Player)
from typing import Dict

class Player:
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id

class Move:
    def __init__(self, x: int, y: int, player: int):
        self.x = x
        self.y = y
        self.player = player

# State Pattern in managing board states (Game won / board full)
class Board:
    def __init__(self, n: int):
        self._moves: Dict[(int, int), int] = {}
        self._gameWon = False
        self._boardFull = False
        self._rowSum  = [0] * n
        self._colSum  = [0] * n
        self._diagSum = 0
        self._crossdiagSum = 0
        self._n = n

    def _inBounds(self, i) -> bool:
        return 0<= i < self._n

    def _isValidMove(self, move: Move) -> bool:
        x = move.x
        y = move.y
        if self._inBounds(x) and self._inBounds(y) and (x, y) not in self._moves:
            return True
        else:
            return False

    def _putMove(self, move: Move):
        self._moves[(move.x, move.y)] = move.player

    def gameWon(self):
        return self._gameWon

    def boardFull(self):
        return self._boardFull

    def makeMove(self, move: Move):

        if not self._isValidMove(move):
            raise ValueError("Error: invalid move!")
        n = self._n
        self._putMove(move)
        if len(self._moves) == n * n:
            self._boardFull = True

        x, y, p = move.x, move.y, move.player
        self._rowSum[x] += p
        self._colSum[y] += p
        if x == y:
            self._diagSum += p

        if x + y + 1 == n:
            self._crossdiagSum += p

        if (abs(self._rowSum[x]) == n or abs(self._colSum[y]) == n
                or abs(self._crossdiagSum) == n or abs(self._diagSum) == n):
            self._gameWon = True

        return

# State Pattern in managing current_player state
class Game:
    def __init__(self, p1: Player, p2: Player, n: int):
        self.p1 = p1
        self.p2 = p2
        self._board = Board(n)
        self._player = p1
        self._n = n

    def resetBoard(self):
        self._board = Board(self._n)

    def togglePlayer(self):
        self._player = self.p1 if self._player == self.p2 else self.p2

    def currPlayerStr(self) -> str:
        return self._player.name

    def currPlayer(self) -> int:
        return 1 if self._player == self.p1 else -1

    def makeMove(self, move: Move):
        if move.player != self.currPlayer():
            raise ValueError("Error: Not this Player's move")

        self._board.makeMove(move)
        p = self.currPlayerStr()

        if self._board.gameWon():
            return f"Player {p} won!"

        elif self._board.boardFull():
            return "Stalemate: Board Full!"

        else:
            self.togglePlayer()
            return "Accepted Move"

    def play(self):

        print("Welcome to Tic Tac Toe!")
        print("Enter 'exit' at any time to quit the game.")

        while not (self._board.gameWon() or self._board.boardFull()):
            try:
                print(f"Player {self.currPlayerStr()}'s turn")
                # Get row input
                x_input = input("Enter row number: ")
                if x_input.lower() == "exit":
                    print("Thanks for playing!")
                    return
                x = int(x_input)

                # Get column input
                y_input = input("Enter column number: ")
                if y_input.lower() == "exit":
                    print("Thanks for playing!")
                    return
                y = int(y_input)

                # Make the move
                p = self.currPlayer()
                status = self.makeMove(Move(x, y, p))
                print(status)
                # Check if the game is over based on the move's result
                if "won" in status or "Stalemate" in status:
                    print("Game Over!")
                    self.resetBoard()
                    return

            except ValueError as e:
                print(f"Invalid input or move: {e}")
            except Exception as e:
                print(f"Unexpected error occurred: {e}")
