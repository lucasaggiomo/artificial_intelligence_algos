import random
from typing import Callable, Generic

from src.agentPackage.action import A, Action
from src.agentPackage.nodes.gameNode import GameNode
from src.agentPackage.player import Player
from src.agentPackage.state import S, State
from src.agentPackage.tasks.game import Game
from src.agentPackage.taskSolvers.taskSolver import TaskSolver

type DecisionAlgorithmType[S: State, A: Action] = Callable[[Game[S, A], Player[S, A], float], A]


class GameTheory(Generic[S, A], TaskSolver[S, A, Game[S, A]]):
    def __init__(self, game: Game[S, A]):
        super().__init__(game)
        self.game = game
        self.currentState = game.initialState

    def startGame(self) -> bool:
        gameOver: bool = False
        print("STATO INIZIALE:\n")
        self.game.environment.render()
        print("Inizia il gioco\n")
        turn = 0
        while not gameOver:
            turn += 1
            for player in self.game.agents:
                print(f"Turno di {player}")

                # SCELTA
                action = player.chooseAction(self.game)
                if action is None:
                    raise ValueError("action was None")

                # ESECUZIONE
                player.executeAction(action, self.game.environment)
                self.currentState = self.game.environment.getCurrentState()

                # STAMPA
                self.game.environment.render()

                # CONTEROLLO DI GAME OVER
                if self.game.terminalTest(self.currentState):
                    gameOver = True
                    break

        print("GAME OVER")

        dict = {player.name: player.getUtility(self.currentState) for player in self.game.agents}
        print("\nUtility:")
        print("\n".join(f"{k}: {v}" for k, v in dict.items()))

        utilities = {
            player.name: player.getUtility(self.currentState) for player in self.game.agents
        }

        # Trova il valore massimo
        max_value = max(utilities.values())

        # Trova i giocatori che hanno quel valore
        winners = [name for name, value in utilities.items() if value == max_value]

        if len(winners) == 1:
            print(f"Vincitore: {winners[0]} con punteggio {max_value}")
        else:
            print(f"Pareggio tra: {', '.join(winners)} con punteggio {max_value}")

    @staticmethod
    def minimaxDecision(
        game: Game[S, A], player: Player[S, A], state: S, limit: float = float("+inf")
    ) -> A:
        """
        Sceglie l'azione da effettuare a partire dallo stato **state** con algoritmo *minimax*
        """
        maxUtility = float("-inf")
        maxUtilityAction = None

        # tra tutte le azioni possibili dallo stato state, sceglie quella con massima minUtility (ovvero per massimizzare l'utility peggiore)
        # print("\n\n####################################")
        # print("####################################")
        for action in game.getActionsFromState(state):
            nextState = game.transitionModel(state, action)
            currUtility = GameTheory[S, A].minUtility(game, player, nextState, limit)
            # print(f"{nextState}\nminUtility = {currUtility}\n")
            if currUtility > maxUtility:
                maxUtility = currUtility
                maxUtilityAction = action

        # print("------------------------------------")
        # print(
        #     f"[AGENT]: Ho scelto lo stato\n{game.transitionModel(state, maxUtilityAction)}\nutility = {maxUtility}"
        # )
        # print("####################################")
        # print("####################################\n\n")
        return maxUtilityAction

    @staticmethod
    def maxUtility(
        game: Game[S, A], player: Player[S, A], state: S, limit: float = float("+inf")
    ) -> float:
        """
        Per ogni stato possibile raggiungibile da **state**, restituisce l'utilità maggiore tra i minUtility (ovvero tra i casi peggiori).
        In questo modo simula l'azione dell'agent, in quanto tra tutte le azioni sceglie l'azione A con il miglior "esito peggiore" associato ad A,
        dove l'esito peggiore associato all'azione A corrisponde all'utility che ha l'agent se accade che:
        - l'agent sceglie l'azione A
        - l'agent avversario sceglie la mossa B che minimizza l'utility per l'agent (quindi la mossa migliore che possa giocare, in modo da massimizzare la *sua* utility)

        Nota: l'utilità e l'output sono riferiti all'agent e si assume *utilità migliore per l'agent* = *utilità peggiore per l'agent avversario*
        """
        if limit <= 0 or game.terminalTest(state):
            return player.getUtility(state)

        maxUtility = float("-inf")
        for action in game.getActionsFromState(state):
            maxUtility = max(
                maxUtility,
                GameTheory[S, A].minUtility(
                    game, player, game.transitionModel(state, action), limit - 1
                ),
            )

        return maxUtility

    @staticmethod
    def minUtility(
        game: Game[S, A], player: Player[S, A], state: S, limit: float = float("+inf")
    ) -> float:
        """
        Per ogni stato possibile raggiungibile da **state**, restituisce l'utilità minore tra i maxUtility (ovvero tra i casi migliori).
        In questo modo simula l'azione dell'agent avversario (se gioca in maniera ottimale), in quanto tra tutte le azioni sceglie l'azione B con il
        peggior "esito migliore" associato a B, dove l'esito migliore associato all'azione B corrisponde all'utility che ha l'agent se accade che:
        - l'agent avversario sceglie l'azione B
        - l'agent sceglie la mossa A che massimizza l'utility per l'agent (quindi la mossa migliore che possa giocare, in modo da massimizzare la *sua* utility)

        Nota: l'utilità e l'output sono riferiti all'agent e si assume *utilità migliore per l'agent* = *utilità peggiore per l'agent avversario*
        """
        if limit <= 0 or game.terminalTest(state):
            return player.getUtility(state)

        minUtility = float("+inf")
        for action in game.getActionsFromState(state):
            minUtility = min(
                minUtility,
                GameTheory[S, A].maxUtility(
                    game, player, game.transitionModel(state, action), limit - 1
                ),
            )

        return minUtility

    @staticmethod
    def minimaxAlphaBetaDecision(
        game: Game[S, A], player: Player[S, A], limit: float = float("+inf")
    ) -> A:
        """
        Sceglie l'azione da effettuare a partire dallo stato **state** con algoritmo *minimax* con la *potatura alpha-beta* (ovvero non espande nodi superflui)
        """

        state = player.percept(game.environment)

        maxUtility = float("-inf")
        maxUtilityAction = None
        maxSoFar = float("-inf")
        minSoFar = float("+inf")

        for action in game.getActionsFromState(state):
            currUtility = GameTheory[S, A].minUtilityAlphaBeta(
                game, player, game.transitionModel(state, action), maxSoFar, minSoFar, limit - 1
            )

            if currUtility > maxUtility:
                maxUtility = currUtility
                maxUtilityAction = action

            maxSoFar = max(maxSoFar, maxUtility)

        print(f"[{player.name}]: Max utility = {maxUtility}")

        return maxUtilityAction

    @staticmethod
    def maxUtilityAlphaBeta(
        game: Game[S, A],
        player: Player[S, A],
        state: S,
        maxSoFar: float,
        minSoFar: float,
        limit: float = float("+inf"),
    ) -> float:
        if limit <= 0 or game.terminalTest(state):
            return player.getUtility(state)

        maxUtility = float("-inf")
        for action in game.getActionsFromState(state):
            maxUtility = max(
                maxUtility,
                GameTheory[S, A].minUtilityAlphaBeta(
                    game,
                    player,
                    game.transitionModel(state, action),
                    maxSoFar,
                    minSoFar,
                    limit - 1,
                ),
            )

            if maxUtility >= minSoFar:
                return maxUtility

            maxSoFar = max(maxSoFar, maxUtility)

        return maxUtility

    @staticmethod
    def minUtilityAlphaBeta(
        game: Game[S, A],
        player: Player[S, A],
        state: S,
        maxSoFar: float,
        minSoFar: float,
        limit: float = float("+inf"),
    ) -> float:
        if limit <= 0 or game.terminalTest(state):
            return player.getUtility(state)

        minUtility = float("+inf")
        for action in game.getActionsFromState(state):
            minUtility = min(
                minUtility,
                GameTheory[S, A].maxUtilityAlphaBeta(
                    game,
                    player,
                    game.transitionModel(state, action),
                    maxSoFar,
                    minSoFar,
                    limit - 1,
                ),
            )

            if minUtility <= maxSoFar:
                return minUtility

            minSoFar = min(minSoFar, minUtility)

        return minUtility
