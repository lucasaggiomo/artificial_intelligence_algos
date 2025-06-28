from __future__ import annotations

from collections.abc import Callable

from agentPackage.action import Action
from agentPackage.agent import Agent
from agentPackage.environment import Environment
from agentPackage.goal import Goal
from agentPackage.sensor import StateSensor
from agentPackage.state import State
from agentPackage.tasks.problem import Problem
from agentPackage.taskSolvers.problemSolving import ProblemSolving


class NPuzzleState(State):
    BLANK = 0

    def __init__(self, board: tuple[int, ...], dimension: int):
        if dimension <= 0:
            raise ValueError(f"Dimension must be positive: {dimension}")

        if len(board) != dimension * dimension:
            raise ValueError(f"Board length {len(board)} does not match {dimension}x{dimension}")

        self.board = board
        self.dimension = dimension

    def __str__(self) -> str:
        output = ""
        for i in range(self.dimension):
            output += (
                " ".join(map(str, self.board[i * self.dimension : (i + 1) * self.dimension])) + "\n"
            )
        return output

    def __eq__(self, other) -> bool:
        return isinstance(other, NPuzzleState) and self.board == other.board

    def __hash__(self) -> int:
        return hash(self.board)

    def index(self, value: int) -> tuple[int, int]:
        try:
            flat_index = self.board.index(value)  # Ricerca efficiente
            return divmod(flat_index, self.dimension)  # Conversione a (riga, colonna)
        except ValueError:
            raise ValueError(f"Value {value} not found in the board")

    def find_blank(self) -> tuple[int, int]:
        return self.index(NPuzzleState.BLANK)

    def createGoalMap(self) -> dict[int, tuple[int, int]]:
        goalMap = {}
        for i in range(self.dimension):
            for j in range(self.dimension):
                value = i * self.dimension + j
                goalMap[value] = (i, j)
        return goalMap


class NPuzzleAction(Action):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    ACTION_LABELS = {RIGHT: "Right", UP: "Up", LEFT: "Left", DOWN: "Down"}

    def __init__(self, value: int):
        if value not in NPuzzleAction.ACTION_LABELS:
            raise ValueError(f"Invalid move: {value}")
        self.value = value

    def __str__(self) -> str:
        return f"{NPuzzleAction.ACTION_LABELS[self.value]}"

    def __eq__(self, other):
        return isinstance(other, NPuzzleAction) and self.value == other.value

    def __hash__(self):
        return hash(self.value)


class NPuzzleEnvironment(Environment):
    def transitionModel(self, state: NPuzzleState, action: NPuzzleAction) -> NPuzzleState:
        return _transitionModel(state, action)


class NPuzzleGoal(Goal):
    def __init__(self, stateToReach):
        self.stateToReach = stateToReach

    def isGoalAchieved(self, state: NPuzzleState) -> bool:
        return state == self.stateToReach

    def __str__(self):
        return f"Stato finale:\n{self.stateToReach}\n"


class NPuzzleAgent(Agent):
    def __init__(self):
        super().__init__(StateSensor())


class NPuzzleProblem(Problem):
    def __init__(
        self,
        initialState: NPuzzleState,
        environment: NPuzzleEnvironment,
        agents: list[NPuzzleAgent],
        goal: NPuzzleGoal,
        heuristic: Callable[[NPuzzleState, NPuzzleGoal, dict[int, tuple[int, int]]], int],
    ):
        super().__init__(initialState, environment, agents, goal)
        self.goal = goal  # type checking
        self.heuristic = heuristic  # type checking
        self.goalMap = self.goal.stateToReach.createGoalMap()

    def pathCostFunction(self, state: NPuzzleState, action: NPuzzleAction):
        return _pathCostFunction(state, action)

    def heuristicDistFunction(self, state: NPuzzleState):
        return _heuristicDistFunction(state, self.goal, self.goalMap, self.heuristic)

    def getActionsFromState(self, state: NPuzzleState):
        return _geActionsFromState(state)

    def transitionModel(self, state: NPuzzleState, action: NPuzzleAction):
        return _transitionModel(state, action)


class NPuzzleProblemSolving(ProblemSolving):
    pass


def _geActionsFromState(state: NPuzzleState) -> list[NPuzzleAction]:
    blank_row, blank_col = state.find_blank()
    valid_actions = []

    if blank_col < state.dimension - 1:
        valid_actions.append(NPuzzleAction(NPuzzleAction.RIGHT))
    if blank_row > 0:
        valid_actions.append(NPuzzleAction(NPuzzleAction.UP))
    if blank_col > 0:
        valid_actions.append(NPuzzleAction(NPuzzleAction.LEFT))
    if blank_row < state.dimension - 1:
        valid_actions.append(NPuzzleAction(NPuzzleAction.DOWN))

    return valid_actions


actions = [
    NPuzzleAction(NPuzzleAction.RIGHT),
    NPuzzleAction(NPuzzleAction.UP),
    NPuzzleAction(NPuzzleAction.LEFT),
    NPuzzleAction(NPuzzleAction.DOWN),
]


def actionsPerState(state: NPuzzleState) -> list[NPuzzleAction]:
    return actions


def _transitionModel(state: NPuzzleState, action: NPuzzleAction) -> NPuzzleState:
    blank_index = state.board.index(NPuzzleState.BLANK)
    blank_row, blank_col = divmod(blank_index, state.dimension)

    newBoard = list(state.board)

    if action.value == NPuzzleAction.RIGHT and blank_col < state.dimension - 1:
        swap_index = blank_index + 1
    elif action.value == NPuzzleAction.UP and blank_row > 0:
        swap_index = blank_index - state.dimension
    elif action.value == NPuzzleAction.LEFT and blank_col > 0:
        swap_index = blank_index - 1
    elif action.value == NPuzzleAction.DOWN and blank_row < state.dimension - 1:
        swap_index = blank_index + state.dimension
    else:
        return state

    newBoard[blank_index], newBoard[swap_index] = (
        newBoard[swap_index],
        NPuzzleState.BLANK,
    )

    return NPuzzleState(tuple(newBoard), state.dimension)


# Costo del percorso (ogni mossa ha costo 1)
def _pathCostFunction(state: NPuzzleState, action: NPuzzleAction) -> int:
    return 1


# Funzione heuristica: somma delle distanze di Manhattan
def manhattanDistance(
    start: NPuzzleState, goal: NPuzzleGoal, goalMap: dict[int, tuple[int, int]]
) -> int:
    total_distance = 0
    dimension = start.dimension

    for index, value in enumerate(start.board):
        if value == NPuzzleState.BLANK:
            continue

        # Ottieni la posizione attuale (row, col) dall'indice
        current_row, current_col = divmod(index, dimension)

        # Ottieni la posizione desiderata dal goalMap
        goal_row, goal_col = goalMap[value]

        # Somma la distanza di Manhattan
        total_distance += abs(current_row - goal_row) + abs(current_col - goal_col)

    return total_distance


def _heuristicDistFunction(
    state: NPuzzleState,
    goal: NPuzzleGoal,
    goalMap: dict[int, tuple[int, int]],
    heuristic: Callable[[NPuzzleState, NPuzzleGoal, dict[int, tuple[int, int]]], int],
) -> int:
    return heuristic(state, goal, goalMap)


import random


def isSolvable(board: tuple[int, ...], dimension: int) -> bool:
    """
    Verifica se una configurazione dell'n-puzzle è risolvibile.
    """
    # Conta le inversioni: coppie (i, j) tali che i < j e board[i] > board[j]
    inversions = sum(
        1
        for i, value_i in enumerate(board)
        for value_j in board[i + 1 :]
        if value_i != NPuzzleState.BLANK and value_j != NPuzzleState.BLANK and value_i > value_j
    )

    if dimension % 2 == 1:
        # Dimensione dispari: il numero di inversioni deve essere pari
        return inversions % 2 == 0
    else:
        # Dimensione pari: conta la riga del blank (da 0 in su)
        blankIndex = board.index(NPuzzleState.BLANK)
        blankRow = blankIndex // dimension
        # Deve essere dispari: (inversions + blankRow)
        return (inversions + blankRow) % 2 == 1


def generateRandomSquareMatrix(dimension: int) -> tuple[int, ...]:
    """
    Genera una configurazione casuale valida dell'n-puzzle come tupla piatta.
    """
    numbers = list(range(dimension * dimension))
    while True:
        random.shuffle(numbers)
        if isSolvable(tuple(numbers), dimension):
            return tuple(numbers)


def generateSortedSquareMatrix(dimension: int) -> tuple[int, ...]:
    """
    Genera lo stato obiettivo ordinato dell'n-puzzle.
    """
    return tuple(range(1, dimension * dimension)) + (NPuzzleState.BLANK,)


def generateRandomState(dimension: int) -> NPuzzleState:
    """
    Genera un'istanza NPuzzleState con una configurazione casuale valida.
    """
    return NPuzzleState(generateRandomSquareMatrix(dimension), dimension)


def generateSortedState(dimension: int) -> NPuzzleState:
    """
    Genera un'istanza NPuzzleState con lo stato obiettivo ordinato.
    """
    return NPuzzleState(generateSortedSquareMatrix(dimension), dimension)
