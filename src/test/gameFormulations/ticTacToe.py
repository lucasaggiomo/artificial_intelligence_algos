from __future__ import annotations

from abc import ABC, abstractmethod
from enum import StrEnum
from functools import lru_cache

from agentPackage.action import Action
from agentPackage.environment import Environment
from agentPackage.player import Player
from agentPackage.playerAI import PlayerAI
from agentPackage.sensor import Sensor
from agentPackage.state import State
from agentPackage.tasks.game import Game
from agentPackage.taskSolvers.gameTheory import DecisionAlgorithmType, GameTheory


class Symbol(StrEnum):
    X = "X"  # Agente
    O = "O"  # Avversario
    EMPTY = " "


class TicTacToeState(State):
    def __init__(self, board: list[list[Symbol]], turn: Symbol):
        self.board = board
        self.turn = turn
        self.size = len(board)

    def getDepth(self) -> int:
        return sum(cell != Symbol.EMPTY for row in self.board for cell in row)

    def copy(self) -> TicTacToeState:
        return TicTacToeState([row.copy() for row in self.board], self.turn)

    def __eq__(self, other):
        return (
            isinstance(other, TicTacToeState)
            and self.board == other.board
            and self.turn == other.turn
        )

    def __str__(self):
        max_index = self.size - 1
        index_width = len(str(max_index))  # es. 2 se max_index=13
        cell_width = 3  # larghezza della cella (es. ' X ', ' O ', '   ')

        # Header con i numeri di colonna, ben allineati
        header = " " * (index_width + 1) + " ".join(f"{i:^{cell_width}}" for i in range(self.size))

        # Corpo della griglia
        rows = []
        for i, row in enumerate(self.board):
            row_str = f"{i:>{index_width}} " + "|".join(
                f"{cell.value:^{cell_width}}" for cell in row
            )
            rows.append(row_str)

        return "\n\n".join([header] + rows)

    def __hash__(self) -> int:
        return hash((str(self.board), self.turn))


class TicTacToeAction(Action):
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return (
            isinstance(other, TicTacToeAction) and self.row == other.row and self.col == other.col
        )

    def __repr__(self):
        return f"Place at ({self.row}, {self.col})"

    def __str__(self):
        return f"Place at ({self.row}, {self.col})"

    def __hash__(self):
        return hash((self.row, self.col))


class TicTacToeEnvironment(Environment[TicTacToeState, TicTacToeAction]):
    def transitionModel(self, state: TicTacToeState, action: TicTacToeAction) -> TicTacToeState:
        return _transitionModel(state, action)


class TicTacToeGame(Game[TicTacToeState, TicTacToeAction]):
    def __init__(
        self,
        initialState: TicTacToeState,
        environment: Environment[TicTacToeState, TicTacToeAction],
        players: list[TicTacToePlayer],
        required: int,
    ):
        super().__init__(initialState, environment, players)
        self.required = required
        for p in players:
            p.required = required

    def terminalTest(self, state: TicTacToeState) -> bool:
        return _terminalTest(state, self.required)  # global function

    def getActionsFromState(self, state: TicTacToeState) -> list[TicTacToeAction]:
        return _actionsPerState(state)  # global function

    def transitionModel(self, state: TicTacToeState, action: TicTacToeAction) -> TicTacToeState:
        return _transitionModel(state, action)


class TicTacToePlayerAI(PlayerAI[TicTacToeState, TicTacToeAction]):
    def __init__(
        self,
        symbol: Symbol,
        decisionAlgorithm: DecisionAlgorithmType,
        limit: float = float("+inf"),
        required: int = 3,
    ):
        super().__init__(
            Sensor[TicTacToeState, TicTacToeAction](), symbol.name, decisionAlgorithm, limit
        )
        self.symbol = symbol
        self.required = required

    # @lru_cache(maxsize=100000)
    def getUtility(self, state: TicTacToeState) -> float:
        return _getUtility(state, self.symbol, self.required)


class TicTacToePlayer(Player[TicTacToeState, TicTacToeAction]):
    def __init__(self, symbol: Symbol, printOptions: bool = True):
        super().__init__(Sensor[TicTacToeState, TicTacToeAction](), symbol.name)
        self.symbol = symbol
        self.printOptions = printOptions

    def chooseAction(self, game: Game[TicTacToeState, TicTacToeAction]) -> TicTacToeAction:
        currentState: TicTacToeState = self.percept(game.environment)

        # Calcola le azioni valide
        validActions = _actionsPerState(currentState)
        validPositions = [(a.row, a.col) for a in validActions]
        positionOutput = " - ".join(map(lambda t: f"{t[0]}, {t[1]}", validPositions))

        # Richiede input finché l'utente non fornisce una posizione valida
        while True:
            try:
                row, col = tuple(
                    map(
                        int,
                        (
                            (
                                input(
                                    f"Scegli una mossa tra le seguenti (riga, colonna):\n{positionOutput}\n"
                                )
                                if self.printOptions
                                else input(f"Scegli una mossa (riga, colonna)\n")
                            ).split(",")
                        ),
                    )
                )
                if (row, col) in validPositions:
                    return TicTacToeAction(row, col)
                else:
                    print("Mossa non valida. Riprova.")
            except ValueError:
                print(
                    'Input non valido. Inserisci una coppia del tipo "riga, colonna", separati da una virgola'
                )

    def getUtility(self, state: TicTacToeState) -> float:
        return _getUtility(state, self.symbol, self.required)


class TicTacToeGameTheory(GameTheory[TicTacToeState, TicTacToeAction]):
    pass


# FUNZIONI DI COMODO
def generateInitialState(size: int = 3) -> TicTacToeState:
    board = [[Symbol.EMPTY for _ in range(size)] for _ in range(size)]
    return TicTacToeState(board, Symbol.X)


# FUNZIONI "PRIVATE"


def _getUtility(state: TicTacToeState, symbol: Symbol, required: int) -> float:
    winner = _checkWinner(state, required)

    if winner is None:
        if _terminalTest(state, required):
            return 0

        # viene restituita stima dell'utilità
        # il codice arriva a questo punto se e solo se viene invocato getUtility su uno stato non terminale, il che induce la stima
        return _heuristic(state, symbol, required)

    points = 1 - state.getDepth() / 1000

    return points if winner == symbol else -points


def _actionsPerState(state: TicTacToeState) -> list[TicTacToeAction]:
    return [
        TicTacToeAction(row, col)
        for row in range(state.size)
        for col in range(state.size)
        if state.board[row][col] == Symbol.EMPTY
    ]


def _terminalTest(state: TicTacToeState, required: int) -> bool:
    return _checkWinner(state, required) is not None or _isDraw(state, required)


# def _checkWinner(state: TicTacToeState) -> Symbol | None:
#     size = state.size
#     lines = []

#     # Righe e colonne
#     lines.extend(state.board)
#     lines.extend([[state.board[r][c] for r in range(size)] for c in range(size)])

#     # Diagonali
#     lines.append([state.board[i][i] for i in range(size)])
#     lines.append([state.board[i][size - 1 - i] for i in range(size)])

#     for line in lines:
#         if line[0] != Symbol.EMPTY and all(cell == line[0] for cell in line):
#             return line[0]
#     return None


def _checkWinner(state: TicTacToeState, required: int) -> Symbol | None:
    size = state.size

    def check_line(line: list[Symbol]) -> Symbol | None:
        for i in range(len(line) - required + 1):
            window = line[i : i + required]
            if window[0] != Symbol.EMPTY and all(cell == window[0] for cell in window):
                return window[0]
        return None

    # Controlla righe
    for row in state.board:
        winner = check_line(row)
        if winner:
            return winner

    # Controlla colonne
    for col in range(size):
        column = [state.board[row][col] for row in range(size)]
        winner = check_line(column)
        if winner:
            return winner

    # Controlla diagonali principali e secondarie (con finestre di 3)
    for r in range(size - required + 1):
        for c in range(size - required + 1):
            # Diagonale principale (↘)
            diag1 = [state.board[r + i][c + i] for i in range(required)]
            winner = check_line(diag1)
            if winner:
                return winner
            # Diagonale secondaria (↙)
            diag2 = [state.board[r + i][c + required - 1 - i] for i in range(required)]
            winner = check_line(diag2)
            if winner:
                return winner

    return None


def _isDraw(state: TicTacToeState, required: int) -> bool:
    return (
        all(cell != Symbol.EMPTY for row in state.board for cell in row)
        and _checkWinner(state, required) is None
    )


def _transitionModel(state: TicTacToeState, action: TicTacToeAction) -> TicTacToeState:
    new_state = state.copy()
    if new_state.board[action.row][action.col] != Symbol.EMPTY:
        raise ValueError("Invalid action: cell is not empty.")
    new_state.board[action.row][action.col] = state.turn
    new_state.turn = Symbol.O if state.turn == Symbol.X else Symbol.X
    return new_state


def _heuristic(state: TicTacToeState, player_symbol: Symbol, required: int) -> float:
    opponent_symbol = Symbol.X if player_symbol == Symbol.O else Symbol.O
    board = state.board
    size = len(board)

    def evaluate_line(line: list[Symbol]) -> float:
        score = 0.0
        for i in range(len(line) - required + 1):
            window = line[i : i + required]
            player_count = window.count(player_symbol)
            opponent_count = window.count(opponent_symbol)

            if opponent_count == 0 and player_count > 0:
                score += 10**player_count
            elif player_count == 0 and opponent_count > 0:
                score -= 10**opponent_count

        return score

    total_score = 0.0

    for row in board:
        total_score += evaluate_line(row)
    for col in range(size):
        column = [board[row][col] for row in range(size)]
        total_score += evaluate_line(column)
    for row in range(size - required + 1):
        for col in range(size - required + 1):
            diag = [board[row + k][col + k] for k in range(min(required, size - max(row, col)))]
            total_score += evaluate_line(diag)
    for row in range(size - required + 1):
        for col in range(required - 1, size):
            anti_diag = [board[row + k][col - k] for k in range(min(required, size - row, col + 1))]
            total_score += evaluate_line(anti_diag)

    # Normalizzazione
    max_score = 10**required * (2 * size)  # valore massimo plausibile
    return max(-1, min(1, total_score / max_score))
