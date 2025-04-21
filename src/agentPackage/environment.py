from abc import ABC, abstractmethod
from typing import Generic

from src.agentPackage.action import A
from src.agentPackage.state import S


class Environment(Generic[S, A], ABC):
    def __init__(self, initialState: S):
        self.currentState = initialState

    @abstractmethod
    def transitionModel(self, state: S, action: A) -> S:
        """Associa ad ogni azione di tipo A, a partire da uno stato di tipo S, lo stato successivo"""
        pass

    def evolveState(self, action: A) -> S:
        self.currentState = self.transitionModel(self.currentState, action)
        return self.currentState

    def getCurrentState(self) -> S:
        return self.currentState

    def render(self):
        print(f"Ambiente attuale:\n{self.currentState}\n")
