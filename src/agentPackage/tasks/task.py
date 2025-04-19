from abc import ABC, abstractmethod

from src.agentPackage.action import Action
from src.agentPackage.state import State
from src.agentPackage.environment import Environment
from src.agentPackage.customTypes import (
    ActionsPerStateType,
    TransitionModelType,
)


class Task(ABC):
    @abstractmethod
    def __init__(
        self,
        initialState: State,
        environment: Environment,
        actionsPerState: ActionsPerStateType,
        transitionModel: TransitionModelType,
    ):
        """
        **initialState**: *State*                                     - stato di partenza\\
        **environment**: *Environment*                                - ambiente del sistema\\
        **actionsPerState**: *ActionsPerStateType*                    - associa ad ogni stato l'insieme delle possibili azioni\\
        **transitionModel**: *TransitionModelType*                    - associa ad ogni azione, a partire da uno stato, lo stato successivo\\
        """
        self.initialState = initialState
        self.environment = environment
        self.actionsPerState = actionsPerState
        self.transitionModel = transitionModel

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

    def __str__(self) -> str:
        return f"Parto da:\n{self.initialState}\n"
