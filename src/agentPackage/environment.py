from src.agentPackage.state import State
from src.agentPackage.action import Action
from src.agentPackage.customTypes import TransitionModelType


class Environment:
    def __init__(self, initialState: State, transitionModel: TransitionModelType):
        self.currentState = initialState
        self.transitionModel = transitionModel  # associa ad ogni azione, a partire da uno stato, lo stato successivo

    def evolveState(self, action: Action) -> State:
        self.currentState = self.transitionModel(self.currentState, action)
        return self.currentState

    def getCurrentState(self) -> State:
        return self.currentState

    def render(self):
        print(f"Ambiente attuale: l'agente si trova in\n{self.currentState}")
