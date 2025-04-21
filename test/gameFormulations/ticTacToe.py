from __future__ import annotations

from enum import StrEnum

from src.agentPackage.action import Action
from src.agentPackage.environment import Environment
from src.agentPackage.player import Player
from src.agentPackage.sensor import Sensor
from src.agentPackage.state import State
from src.agentPackage.tasks.game import Game
from src.agentPackage.user import User


class Symbol(StrEnum):
    X = "X"  # Agente
    O = "O"  # Avversario
    EMPTY = " "


class TicTacToeState(State):
    def __init__(self, board: list[list[Symbol]], turn: Symbol):
        self.board = board
        self.turn = turn  # Il giocatore che deve muovere

    def getDepth(self) -> int:
        countOfSymbols = 0
        for row in self.board:
            for item in row:
                if item != Symbol.EMPTY:
                    countOfSymbols += 1
        return countOfSymbols

    def copy(self) -> TicTacToeState:
        return TicTacToeState([row.copy() for row in self.board], self.turn)

    def __eq__(self, other):
        return (
            isinstance(other, TicTacToeState)
            and self.board == other.board
            and self.turn == other.turn
        )

    def __str__(self):
        header = "  " + "   ".join(map(str, range(len(self.board[0]))))
        rows = [
            f"{i} " + " | ".join(cell.value for cell in row) for i, row in enumerate(self.board)
        ]
        return "\n".join([header] + rows)

    def __str__(self):
        header = "  " + "   ".join(map(str, range(len(self.board[0]))))
        rows = [
            f"{i} " + " | ".join(cell.value for cell in row) for i, row in enumerate(self.board)
        ]
        return "\n".join([header] + rows)


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
    ):
        super().__init__(initialState, environment, players)

    def terminalTest(self, state: TicTacToeState) -> bool:
        return _terminalTest(state)  # global function

    def getActionsFromState(self, state: TicTacToeState) -> list[TicTacToeAction]:
        return _actionsPerState(state)  # global function

    def transitionModel(self, state: TicTacToeState, action: TicTacToeAction) -> TicTacToeState:
        return _transitionModel(state, action)


class TicTacToePlayer(Player[TicTacToeState, TicTacToeAction]):
    def __init__(self, symbol: Symbol):
        super().__init__(Sensor[TicTacToeState, TicTacToeAction](), symbol.name)
        self.symbol = symbol

    def getUtility(self, state: TicTacToeState) -> float:
        winner = _checkWinner(state)

        if winner is None:
            if _terminalTest(state):
                return 0
            return 0

        points = 1 - state.getDepth() / 1000

        return points if winner == self.symbol else -points


class TicTacToeUser(TicTacToePlayer, User[TicTacToeState, TicTacToeAction]):
    def chooseAction(self, game: Game[TicTacToeState, TicTacToeAction]):
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
                        input(
                            f"Scegli una mossa tra le seguenti (riga, colonna):\n{positionOutput}\n"
                        ).split(","),
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


# FUNZIONI DI COMODO
def generateInitialState() -> TicTacToeState:
    board = [
        list(map(Symbol, row))
        for row in [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "],
        ]
    ]
    return TicTacToeState(
        board,
        turn=Symbol.X,
    )
    # return TicTacToeState(
    #     [[Symbol.EMPTY for _ in range(3)] for _ in range(3)], Symbol.X
    # )


# FUNZIONI "PRIVATE"


def _actionsPerState(state: TicTacToeState) -> list[TicTacToeAction]:
    return [
        TicTacToeAction(row, col)
        for row in range(3)
        for col in range(3)
        if state.board[row][col] == Symbol.EMPTY
    ]


def _terminalTest(state: TicTacToeState) -> bool:
    return _checkWinner(state) is not None or _isDraw(state)


def _checkWinner(state: TicTacToeState) -> Symbol | None:
    lines = []

    # Righe e colonne
    lines.extend(state.board)
    lines.extend([[state.board[r][c] for r in range(3)] for c in range(3)])

    # Diagonali
    lines.append([state.board[i][i] for i in range(3)])
    lines.append([state.board[i][2 - i] for i in range(3)])

    for line in lines:
        if line[0] != Symbol.EMPTY and all(cell == line[0] for cell in line):
            return line[0]
    return None


def _isDraw(state: TicTacToeState) -> bool:
    return all(cell != Symbol.EMPTY for row in state.board for cell in row)


def _transitionModel(state: TicTacToeState, action: TicTacToeAction) -> TicTacToeState:
    new_state = state.copy()
    if new_state.board[action.row][action.col] != Symbol.EMPTY:
        raise ValueError("Invalid action: cell is not empty.")
    new_state.board[action.row][action.col] = state.turn
    new_state.turn = Symbol.O if state.turn == Symbol.X else Symbol.X
    return new_state
