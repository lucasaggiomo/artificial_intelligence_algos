from collections.abc import Callable
from test.gameFormulations.ticTacToe import (
    Symbol,
    TicTacToeAction,
    TicTacToeEnvironment,
    TicTacToeGame,
    TicTacToePlayer,
    TicTacToeState,
    actionsPerState,
    generateInitialState,
    terminalTest,
    transitionModel,
)
from threading import Event, Thread

from src.agentPackage.agent import Agent
from src.agentPackage.customTypes import (
    ActionsPerStateType,
    TerminalTestFunctionType,
    UtilityFunctionType,
)
from src.agentPackage.environment import Environment
from src.agentPackage.sensor import Sensor
from src.agentPackage.tasks.game import Game
from src.agentPackage.taskSolvers.gameTheory import GameTheory

initialState = generateInitialState()
environment = TicTacToeEnvironment(initialState, transitionModel)

game = TicTacToeGame(
    initialState,
    environment,
    actionsPerState,
    transitionModel,
    terminalTest,
)

player1 = TicTacToePlayer(Symbol.O)
player2 = TicTacToePlayer(Symbol.X)

solver = GameTheory[TicTacToeState, TicTacToeAction]([player1, player2], game)

solver.startGame()
