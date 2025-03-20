from .state import State

class Perception:
    state: State
    
    def __init__(self, state: State):
        self.state = state

    def __str__(self):
        return f"Percezione: l'agente si trova in {self.state}"
