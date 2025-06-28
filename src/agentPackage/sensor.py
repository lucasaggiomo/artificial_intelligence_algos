from abc import ABC, abstractmethod

from agentPackage.environment import Environment
from agentPackage.perception import Perception
from agentPackage.state import State


class Sensor(ABC):
    @abstractmethod
    def percept(self, environment: Environment) -> Perception:
        pass


class StateSensor(Sensor):
    """Sensore semplice che restituisce lo stato corrente dell'ambiente"""

    def percept(self, environment: Environment) -> State:
        return environment.getCurrentState()
