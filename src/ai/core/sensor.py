from abc import ABC, abstractmethod

from ai.core.environment import Environment
from ai.core.state import State


class Perception(State):
    def __str__(self):
        return f"Percezione: l'agente si trova in {self}"

class Sensor(ABC):
    @abstractmethod
    def percept(self, environment: Environment) -> Perception:
        pass


class StateSensor(Sensor):
    """Sensore semplice che restituisce lo stato corrente dell'ambiente"""

    def percept(self, environment: Environment) -> State:
        return environment.currentState
