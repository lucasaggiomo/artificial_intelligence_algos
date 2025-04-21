from abc import ABC, abstractmethod
from typing import Generic

from src.agentPackage.action import A
from src.agentPackage.agent import Agent
from src.agentPackage.state import S


class Player(Generic[S, A], Agent[S, A], ABC):
    @abstractmethod
    def __init__(self, sensor, name):
        super().__init__(sensor)
        self.name = name

    @abstractmethod
    def getUtility(self, state: S) -> float:
        """Restituisce il valore di utilità relativo al player rispetto allo stato in ingresso"""
        pass

    def __str__(self) -> str:
        return self.name
