from .state import State
from .action import Action

from .customTypes import TransitionModelType

class Environment:
    state: State
    transitionModel: TransitionModelType                # associa ad ogni azione, a partire da uno stato, lo stato successivo
    
    def __init__(self, initialState: State, transitionModel: TransitionModelType):
        self.state = initialState
        self.transitionModel = transitionModel

    def evolveState(self, action: Action) -> State:
        if (self.state, action) in self.transitionModel:
            self.state = self.transitionModel[(self.state, action)]
        return self.state

    def getCurrentState(self) -> State:
        return self.state

    def render(self):
        print(f"Ambiente attuale: l'agente si trova in {self.state}")