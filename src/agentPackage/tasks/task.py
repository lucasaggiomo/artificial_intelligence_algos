from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from agentPackage.action import TAction
from agentPackage.agent import TAgent
from agentPackage.environment import Environment
from agentPackage.state import TState

TTask = TypeVar("TTask", bound="Task", covariant=True)


class Task(Generic[TState, TAction, TAgent], ABC):
    @abstractmethod
    def __init__(self, initialState: TState, environment: Environment[TState, TAction], agents: list[TAgent]):
        """
        **initialState**: *State*                                     - stato di partenza\\
        **environment**: *Environment*                                - ambiente del sistema\\
        **agents**: *list[Agent]*                                     - agenti presenti nel sistema\\
        """
        self.initialState = initialState
        self.environment = environment
        self.agents = agents

    @abstractmethod
    def getActionsFromState(self, state: TState) -> list[TAction]:
        """
        **ACTIONS** nel libro\n
        Restituisce l'insieme delle azioni possibili da un certo stato
        """
        pass

    @abstractmethod
    def transitionModel(self, state: TState, action: TAction) -> TState:
        """
        **RESULT** nel libro\n
        Restituisce lo stato ottenuto eseguendo un'azione a partire da un certo stato
        """
        pass

    def __str__(self) -> str:
        return f"Task = \n{self.environment}\nStato iniziale: \n{self.initialState}\n"
