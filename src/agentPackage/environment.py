from typing import Generic

from src.agentPackage.customTypes import TransitionModelType
from src.agentPackage.typeVars import A, S


class Environment(Generic[S, A]):
    def __init__(self, initialState: S, transitionModel: TransitionModelType[S, A]):
        self.currentState = initialState
        self.transitionModel = transitionModel  # Associa ad ogni azione di tipo A, a partire da uno stato di tipo S, lo stato successivo

    def evolveState(self, action: A) -> S:
        self.currentState = self.transitionModel(self.currentState, action)
        return self.currentState

    def getCurrentState(self) -> S:
        return self.currentState

    def render(self):
        print(f"Ambiente attuale:\n{self.currentState}\n")
