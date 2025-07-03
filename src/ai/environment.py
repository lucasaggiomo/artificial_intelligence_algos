import textwrap
from abc import ABC, abstractmethod

from ai.action import Action
from ai.state import State


class Environment(ABC):
    def __init__(self, initialState: State):
        self.currentState = initialState

    @abstractmethod
    def transitionModel(self, state: State, action: Action) -> State:
        """Associa ad ogni azione, a partire da uno stato di partenza, lo stato successivo"""
        pass

    def evolveState(self, action: Action) -> State:
        """Evolve lo stato corrente, eseguendo l'azione richiesta"""
        self.currentState = self.transitionModel(self.currentState, action)
        return self.currentState

    def getCurrentState(self) -> State:
        return self.currentState

    def render(self):
        print(f"Ambiente attuale:\n{textwrap.indent(str(self.currentState), "\t")}\n")
