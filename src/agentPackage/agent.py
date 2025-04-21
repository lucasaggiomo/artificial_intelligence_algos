from typing import Generic, TypeVar

from src.agentPackage.action import A
from src.agentPackage.environment import Environment
from src.agentPackage.perception import Perception
from src.agentPackage.sensor import Sensor
from src.agentPackage.state import S

AG = TypeVar("AG", bound="Agent")


class Agent(Generic[S, A]):
    def __init__(self, sensor: Sensor):
        self.sensor = sensor

    def percept(self, environment: Environment[S, A]) -> Perception:
        """Restituisce una **Perception** a partire da un **environment**, utilizzando il suo **self.sensor**"""
        return self.sensor.percept(environment)

    def executeAction(self, action: A, environment: Environment[S, A]):
        """Esegue l'azione **action** sull'ambiente **environment**"""
        environment.evolveState(action)
