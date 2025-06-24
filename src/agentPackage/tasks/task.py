from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from agentPackage.action import Action
from agentPackage.agent import Agent
from agentPackage.environment import Environment
from agentPackage.state import State


class Task(ABC):
    @abstractmethod
    def __init__(self, initialState: State, environment: Environment, agents: Sequence[Agent]):
        """
        **initialState**: *State*                                     - stato di partenza\\
        **environment**: *Environment*                                - ambiente del sistema\\
        **agents**: *Sequence[Agent]*                                     - agenti presenti nel sistema\\
        """
        self.initialState = initialState
        self.environment = environment
        self.agents = agents

    @abstractmethod
    def geActionsFromState(self, state: State) -> list[Action]:
        """
        **ACTIONS** nel libro\n
        Restituisce l'insieme delle azioni possibili da un certo stato
        """
        pass

    @abstractmethod
    def transitionModel(self, state: State, action: Action) -> State:
        """
        **RESULT** nel libro\n
        Restituisce lo stato ottenuto eseguendo un'azione a partire da un certo stato
        """
        pass

    def __str__(self) -> str:
        return f"Task = \n{self.environment}\nStato iniziale: \n{self.initialState}\n"
