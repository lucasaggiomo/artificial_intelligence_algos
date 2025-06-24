from abc import ABC, abstractmethod

from agentPackage.action import Action
from agentPackage.state import State


class Environment(ABC):
    def __init__(self, initialState: State):
        self.currenState = initialState

    @abstractmethod
    def transitionModel(self, state: State, action: Action) -> State:
        """Associa ad ogni azione di tipo A, a partire da uno stato di tipo S, lo stato successivo"""
        pass

    def evolveState(self, action: Action) -> State:
        self.currenState = self.transitionModel(self.currenState, action)
        return self.currenState

    def getCurrenState(self) -> State:
        return self.currenState

    def render(self):
        print(f"Ambiente attuale:\n{self.currenState}\n")
