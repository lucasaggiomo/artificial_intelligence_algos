from abc import ABC, abstractmethod
from typing import Generic

from agentPackage.action import TAction
from agentPackage.state import TState


class Environment(Generic[TState, TAction], ABC):
    def __init__(self, initialState: TState):
        self.currentState = initialState

    @abstractmethod
    def transitionModel(self, state: TState, action: TAction) -> TState:
        """Associa ad ogni azione di tipo A, a partire da uno stato di tipo S, lo stato successivo"""
        pass

    def evolveState(self, action: TAction) -> TState:
        self.currentState = self.transitionModel(self.currentState, action)
        return self.currentState

    def getCurrentState(self) -> TState:
        return self.currentState

    def render(self):
        print(f"Ambiente attuale:\n{self.currentState}\n")
