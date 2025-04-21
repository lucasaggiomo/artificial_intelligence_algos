from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.agentPackage.action import A
from src.agentPackage.agent import AG
from src.agentPackage.environment import Environment
from src.agentPackage.state import S

T = TypeVar("T", bound="Task", covariant=True)


class Task(Generic[S, A, AG], ABC):
    @abstractmethod
    def __init__(self, initialState: S, environment: Environment[S, A], agents: list[AG]):
        """
        **initialState**: *State*                                     - stato di partenza\\
        **environment**: *Environment*                                - ambiente del sistema\\
        **agents**: *list[Agent]*                                     - agenti presenti nel sistema\\
        """
        self.initialState = initialState
        self.environment = environment
        self.agents = agents

    @abstractmethod
    def getActionsFromState(self, state: S) -> list[A]:
        """
        **ACTIONS** nel libro\n
        Restituisce l'insieme delle azioni possibili da un certo stato
        """
        pass

    @abstractmethod
    def transitionModel(self, state: S, action: A) -> S:
        """
        **RESULT** nel libro\n
        Restituisce lo stato ottenuto eseguendo un'azione a partire da un certo stato
        """
        pass

    def __str__(self) -> str:
        return f"Task = \n{self.environment}\nStato iniziale: \n{self.initialState}\n"
