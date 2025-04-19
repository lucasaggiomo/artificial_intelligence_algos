from src.agentPackage.state import State


class Perception(State):
    def __str__(self):
        return f"Percezione: l'agente si trova in {self.state}"
