from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.agentPackage.customTypes import ActionsPerStateType, TransitionModelType
from src.agentPackage.environment import Environment
from src.agentPackage.typeVars import A, S

T = TypeVar("T", bound="Task", covariant=True)


class Task(Generic[S, A], ABC):
    @abstractmethod
    def __init__(
        self,
        initialState: S,
        environment: Environment[S, A],
        actionsPerState: ActionsPerStateType[S, A],
        transitionModel: TransitionModelType[S, A],
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

    def getActionsFromState(self, state: S) -> list[A]:
        """
        **ACTIONS** nel libro\n
        Restituisce l'insieme delle azioni possibili da un certo stato
        """
        return self.actionsPerState(state)

    def getNextState(self, state: S, action: A) -> S:
        """
        **RESULT** nel libro\n
        Restituisce lo stato ottenuto eseguendo un'azione a partire da un certo stato
        """
        return self.transitionModel(state, action)

    def __str__(self) -> str:
        return f"Parto da:\n{self.initialState}\n"
