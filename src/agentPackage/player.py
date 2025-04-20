from abc import ABC, abstractmethod
from typing import Generic

from src.agentPackage.agent import Agent
from src.agentPackage.typeVars import A, S


class Player(Generic[S, A], Agent[S, A], ABC):
    @abstractmethod
    def __init__(self, sensor, name):
        super().__init__(sensor)
        self.name = name

    @abstractmethod
    def utilityFunction(self, state: S) -> float:
        pass

    def __str__(self) -> str:
        return self.name
