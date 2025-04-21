from test.gameFormulations.ticTacToe import (
    Symbol,
    TicTacToeAction,
    TicTacToeEnvironment,
    TicTacToeGame,
    TicTacToePlayer,
    TicTacToeState,
    TicTacToeUser,
    generateInitialState,
)

from src.agentPackage.taskSolvers.gameTheory import GameTheory

initialState = generateInitialState()
environment = TicTacToeEnvironment(initialState)

# player1 è X perché tocca prima a X
player1 = TicTacToePlayer(Symbol.X)
player2 = TicTacToeUser(Symbol.O)

game = TicTacToeGame(initialState, environment, [player1, player2])

solver = GameTheory[TicTacToeState, TicTacToeAction](game)

solver.startGame()
