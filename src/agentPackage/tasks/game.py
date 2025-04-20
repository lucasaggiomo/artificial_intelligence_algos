from typing import Generic

from src.agentPackage.customTypes import (
    ActionsPerStateType,
    TerminalTestFunctionType,
    TransitionModelType,
    UtilityFunctionType,
)
from src.agentPackage.environment import Environment
from src.agentPackage.tasks.task import Task
from src.agentPackage.typeVars import A, S


class Game(Generic[S, A], Task[S, A]):
    def __init__(
        self,
        initialState: S,
        environment: Environment[S, A],
        actionsPerState: ActionsPerStateType[S, A],
        transitionModel: TransitionModelType[S, A],
        terminalTest: TerminalTestFunctionType[S],
    ):
        """
        **initialState**: *State*                                     - stato di partenza\\
        **environment**: *Environment*                                - ambiente del sistema\\
        **actionsPerState**: *ActionsPerStateType*                    - associa ad ogni stato l'insieme delle possibili azioni\\
        **transitionModel**: *TransitionModelType*                    - associa ad ogni azione, a partire da uno stato, lo stato successivo\\
        **terminalTest**: *TerminalTestFunctionType*                  - restituisce True se lo stato in ingresso è di GameOver, False altrimenti\\
        """
        super().__init__(initialState, environment, actionsPerState, transitionModel)
        self.terminalTest = terminalTest
