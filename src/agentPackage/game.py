from .task import Task

from .state import State

from .customTypes import (
    ActionsPerStateType,
    TransitionModelType,
    UtilityFunctionType,
    TerminalTestFunctionType,
)


class Game(Task):

    def __init__(
        self,
        initialState: State,
        actionsPerState: ActionsPerStateType,
        transitionModel: TransitionModelType,
        utilityFunction: UtilityFunctionType,
        terminalTest: TerminalTestFunctionType,
    ):
        """
        initialState: State                                     # stato di partenza\\
        actionsPerState: ActionsPerStateType                    # associa ad ogni stato l'insieme delle possibili azioni\\
        transitionModel: TransitionModelType                    # associa ad ogni azione, a partire da uno stato, lo stato successivo\\
        goal: Goal                                              # obiettivo\\
        pathCostFunction: PathFunctionType                      # funzione del costo di un percorso, dato stato e azione\\
        heuristicDistFunction: HeuristicStateOnlyFunctionType   # funzione heuristica della distanza di uno stato dalla/e destinazione/i\\
        """
        super().__init__(initialState, actionsPerState, transitionModel)
        self.utilityFunction = utilityFunction
        self.terminalTest = terminalTest
