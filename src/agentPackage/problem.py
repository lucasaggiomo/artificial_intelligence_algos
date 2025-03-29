from .goal import Goal
from .action import Action
from .state import State

from .customTypes import (
    ActionsPerStateType,
    TransitionModelType,
    PathFunctionType,
    HeuristicFunctionType,
    HeuristicStateOnlyFunctionType,
)


class Problem:

    def __init__(
        self,
        initialState: State,
        actionsPerState: ActionsPerStateType,
        transitionModel: TransitionModelType,
        goal: Goal,
        pathCostFunction: PathFunctionType,
        heuristicDistFunction: HeuristicFunctionType = None,
    ):
        """
        initialState: State                                     # stato di partenza
        actionsPerState: ActionsPerStateType                    # associa ad ogni stato l'insieme delle possibili azioni
        transitionModel: TransitionModelType                    # associa ad ogni azione, a partire da uno stato, lo stato successivo
        goal: Goal                                              # obiettivo
        pathCostFunction: PathFunctionType                      # funzione del costo di un percorso, dato stato e azione
        heuristicDistFunction: HeuristicStateOnlyFunctionType   # funzione heuristica della distanza di uno stato dalla/e destinazione/i
        """
        self.initialState = initialState
        self.actionsPerState = actionsPerState
        self.transitionModel = transitionModel
        self.goal = goal
        self.pathCostFunction = pathCostFunction
        self.heuristicDistFunction = lambda state: heuristicDistFunction(
            state, self.goal
        )

    def getActionsFromState(self, state: State) -> list[Action]:
        """
        ACTIONS\n
        Restituisce l'insieme delle azioni possibili da un certo stato
        """
        return self.actionsPerState(state)

    def getNextState(self, state: State, action: Action) -> State:
        """
        RESULT\n
        Restituisce lo stato ottenuto eseguendo un'azione a partire da un certo stato
        """
        return self.transitionModel(state, action)

    def isGoalAchieved(self, state: State) -> bool:
        return self.goal.isGoalAchieved(state)

    def __str__(self) -> str:
        return f"Parto da:\n{self.initialState}\nDevo raggiungere l'obiettivo:\n{self.goal}\n"
