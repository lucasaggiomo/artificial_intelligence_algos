import sys
from test.games.ticTacToe.ticTacToe import (
    Symbol,
    TicTacToeEnvironment,
    TicTacToeGame,
    TicTacToeGameTheory,
    TicTacToePlayerAI,
    generateInitialState,
)


def getFromArgvOrDefault(index: int, default) -> int:
    try:
        return int(sys.argv[index])
    except:
        return default


def main():
    DIMENSION = getFromArgvOrDefault(1, 3)
    REQUIRED = getFromArgvOrDefault(2, 3) # numero di simboli in fila per vincere

    initialState = generateInitialState(DIMENSION)
    environment = TicTacToeEnvironment(initialState)

    # player1 è X perché tocca prima a X
    player1 = TicTacToePlayerAI(Symbol.X, TicTacToeGameTheory.minimaxAlphaBetaDecision, 2, REQUIRED)
    player2 = TicTacToePlayerAI(Symbol.O, TicTacToeGameTheory.minimaxAlphaBetaDecision, 3, REQUIRED)
    # player2 = TicTacToePlayer(Symbol.O, printOptions=False)

    game = TicTacToeGame(initialState, environment, [player1, player2], REQUIRED)

    solver = TicTacToeGameTheory(game)

    solver.startGame()
    if hasattr(TicTacToePlayerAI.getUtility, "cache_info"):
        print(TicTacToePlayerAI.getUtility.cache_info())


if __name__ == "__main__":
    main()
