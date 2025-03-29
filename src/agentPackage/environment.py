from .state import State
from .action import Action

from .customTypes import TransitionModelType


class Environment:

    def __init__(self, initialState: State, transitionModel: TransitionModelType):
        self.state = initialState
        self.transitionModel = transitionModel  # associa ad ogni azione, a partire da uno stato, lo stato successivo

    def evolveState(self, action: Action) -> State:
        self.state = self.transitionModel(self.state, action)
        return self.state

    def getCurrentState(self) -> State:
        return self.state

    def render(self):
        print(f"Ambiente attuale: l'agente si trova in\n{self.state}")
