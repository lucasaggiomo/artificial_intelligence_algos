from abc import ABC, abstractmethod
from typing import Generic

from agentPackage.action import TAction
from agentPackage.agent import Agent
from agentPackage.state import TState


class Player(Generic[TState, TAction], Agent[TState, TAction], ABC):
    def __init__(self, sensor, name: str):
        super().__init__(sensor)
        self.name = name

    @abstractmethod
    def getUtility(self, state: TState) -> float:
        """Restituisce il valore di utilità relativo al player rispetto allo stato in ingresso"""
        pass

    @abstractmethod
    def chooseAction(self, game: "Game[TState, TAction]") -> TAction:  # type: ignore
        pass

    def __str__(self) -> str:
        return self.name
