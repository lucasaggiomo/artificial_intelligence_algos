import random
import textwrap
import threading as th
from typing import Callable, Optional

from agentPackage.action import Action
from agentPackage.player import Player
from agentPackage.state import State
from agentPackage.tasks.game import Game
from agentPackage.taskSolvers.taskSolver import TaskSolver

type DecisionAlgorithmType = Callable[[Game, Player, set[State], float], Optional[Action]]


class GameTheory(TaskSolver):
    def __init__(self, game: Game, waitTurnEvent: Optional[th.Event] = None):
        super().__init__(game)
        self.game = game
        self.currentState = game.initialState
        self.waitTurnEvent = waitTurnEvent

    def startGame(self):
        gameOver = False
        print("STATO INIZIALE:\n")
        self.game.environment.render()
        print("Inizia il gioco\n")
        turn = 0
        while not gameOver:
            turn += 1
            for player in self.game.players:

                print("Attendo il prossimo turno...")
                if self.waitTurnEvent:
                    self.waitTurnEvent.wait()
                    self.waitTurnEvent.clear()

                print("#######################################################")
                print(f"Turno di {player.name}")

                # SCELTA
                print("SCELTA DEL PLAYER: " + player.name)
                action = player.chooseAction(self.game)
                if action is None:
                    raise ValueError("action was None")

                print("AZIONE SCELTA: " + str(action))

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

        dict = {player.name: player.getUtility(self.currentState) for player in self.game.players}
        print("\nUtility:")
        print("\n".join(f"{k}: {v}" for k, v in dict.items()))

        utilities = {
            player.name: player.getUtility(self.currentState) for player in self.game.players
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
        game: Game,
        player: Player,
        limit: float = float("+inf"),
    ) -> Optional[Action]:
        """
        Sceglie l'azione da effettuare a partire dallo stato **state** con algoritmo *minimax*
        """
        maxUtility = float("-inf")
        maxUtilityAction = None

        state = player.percept(game.environment)

        # tra tutte le azioni possibili dallo stato state, sceglie quella con massima minUtility (ovvero per massimizzare l'utility peggiore)
        print("\n\n####################################")
        print("####################################")
        for action in game.getActionsFromState(state):
            nextState = game.transitionModel(state, action)
            currUtility = GameTheory.minUtility(game, player, nextState, limit)
            print(f"[[\n{textwrap.indent(str(nextState), "\t")}\n]]\nminUtility = {currUtility}\n")
            print("------------------------------------")
            if currUtility > maxUtility:
                maxUtility = currUtility
                maxUtilityAction = action

        print(
            f"[{player.name}]: Max utility = {maxUtility} con la mossa: [[\n{textwrap.indent(str(maxUtilityAction), "\t")}\n]]"
        )
        print("####################################")
        print("####################################\n\n")
        return maxUtilityAction

    @staticmethod
    def maxUtility(
        game: Game,
        player: Player,
        state: State,
        limit: float = float("+inf"),
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
                GameTheory.minUtility(game, player, game.transitionModel(state, action), limit - 1),
            )

        return maxUtility

    @staticmethod
    def minUtility(
        game: Game,
        player: Player,
        state: State,
        limit: float = float("+inf"),
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
                GameTheory.maxUtility(game, player, game.transitionModel(state, action), limit - 1),
            )

        return minUtility

    @staticmethod
    def minimaxAlphaBetaDecision(
        game: Game,
        player: Player,
        visited: set[State],  # tiene traccia degli stati visitati
        limit: float = float("+inf"),
    ) -> Optional[Action]:
        """
        Sceglie l'azione da effettuare a partire dallo stato **state** con algoritmo *minimax* con la *potatura alpha-beta* (ovvero non espande nodi superflui)
        """

        state = player.percept(game.environment)

        maxUtility = float("-inf")
        maxUtilityActions: list[Action] = []
        maxSoFar = float("-inf")
        minSoFar = float("+inf")
        visited.add(state)

        validActions = game.getActionsFromState(state)

        # print("\n\n####################################")
        # print("####################################")
        for action in validActions:
            nextState = game.transitionModel(state, action)
            currUtility = GameTheory.minUtilityAlphaBeta(
                game,
                player,
                nextState,
                maxSoFar,
                minSoFar,
                visited,
                limit - 1,
            )
            # print(f"[[\n{textwrap.indent(str(nextState), "\t")}\n]]\nminUtility = {currUtility}\n")
            # print("------------------------------------")

            if currUtility == maxUtility:
                maxUtilityActions.append(action)
            elif currUtility > maxUtility:
                maxUtility = currUtility
                maxUtilityActions = [action]

            maxSoFar = max(maxSoFar, maxUtility)

        # se ci sono più azioni con la stessa massima utilità, ne sceglie una basandosi sull'euristica
        # se ancora dovessero esserci mosse con utilità pari, sceglie casualmente
        if len(maxUtilityActions) > 1:
            print(
                f"Parità tra {len(maxUtilityActions)} azioni. Applicazione criterio secondario..."
            )

            # funzione da usare nel sort (sorteggia per utility rispetto al player)
            def heuristic(action: Action) -> float:
                nextState = game.transitionModel(state, action)
                return player.getUtility(nextState)

            # calcola il massimo tra le utilità delle mosse trovate
            heuristicValues = [(action, heuristic(action)) for action in maxUtilityActions]
            maxHeuristic = max(heuristic for _, heuristic in heuristicValues)

            # prende solo le azioni che hanno quell'utilità
            maxHeuristicActions = [
                action for action, heuristic in heuristicValues if heuristic == maxHeuristic
            ]

            # sceglie casualmente se ce n'è più di una con valore massimo
            selectedAction = random.choice(maxHeuristicActions)
        else:
            # sceglie direttamente l'azione maggiore (cioè la prima della lista se presente)
            selectedAction = maxUtilityActions[0] if maxUtilityActions else None

        # print(
        #     f"[{player.name}]: Max utility = {maxUtility} con la mossa: [[\n{textwrap.indent(str(selectedAction), "\t")}\n]]"
        # )
        # print("####################################")
        # print("####################################\n\n")

        # qualora per qualche motivo l'azione dovesse essere None (probabile errore), sceglie a caso
        if selectedAction is None:
            print("L'AZIONE ERA NONE, PROBABILE ERRORE")
            selectedAction = random.choice(validActions)

        return selectedAction

    @staticmethod
    def maxUtilityAlphaBeta(
        game: Game,
        player: Player,
        state: State,
        maxSoFar: float,
        minSoFar: float,
        visited: set[State],
        limit: float = float("+inf"),
    ) -> float:

        # tronca l'esplorazione dell'albero se:
        # - ha raggiunto il limite di profondità prefissata
        # - lo stato è terminale
        # - lo stato è già stato visitato
        if limit == 0 or game.terminalTest(state) or state in visited:
            # if state in visited:
            #     input("TROVATO, continua...")
            return player.getUtility(state)

        # riassegna visited per non modificare il set passatogli dal chiamante
        visited.add(state)
        maxUtility = float("-inf")
        for action in game.getActionsFromState(state):
            maxUtility = max(
                maxUtility,
                GameTheory.minUtilityAlphaBeta(
                    game,
                    player,
                    game.transitionModel(state, action),
                    maxSoFar,
                    minSoFar,
                    visited,
                    limit - 1,
                ),
            )

            if maxUtility >= minSoFar:
                return maxUtility

            maxSoFar = max(maxSoFar, maxUtility)

        return maxUtility

    @staticmethod
    def minUtilityAlphaBeta(
        game: Game,
        player: Player,
        state: State,
        maxSoFar: float,
        minSoFar: float,
        visited: set[State],
        limit: float = float("+inf"),
    ) -> float:

        # tronca l'esplorazione dell'albero se:
        # - ha raggiunto il limite di profondità prefissata
        # - lo stato è terminale
        # - lo stato è già stato visitato
        if limit == 0 or game.terminalTest(state) or state in visited:
            return player.getUtility(state)

        # riassegna visited per non modificare il set passatogli dal chiamante
        visited.add(state)
        minUtility = float("+inf")
        for action in game.getActionsFromState(state):
            minUtility = min(
                minUtility,
                GameTheory.maxUtilityAlphaBeta(
                    game,
                    player,
                    game.transitionModel(state, action),
                    maxSoFar,
                    minSoFar,
                    visited,
                    limit - 1,
                ),
            )

            if minUtility <= maxSoFar:
                return minUtility

            minSoFar = min(minSoFar, minUtility)

        return minUtility
