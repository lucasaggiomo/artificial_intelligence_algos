from typing import Generic, TypeVar

from agentPackage.action import TAction
from agentPackage.environment import Environment
from agentPackage.perception import Perception
from agentPackage.sensor import Sensor
from agentPackage.state import TState

TAgent = TypeVar("TAgent", bound="Agent")


class Agent(Generic[TState, TAction]):
    def __init__(self, sensor: Sensor):
        self.sensor = sensor

    def percept(self, environment: Environment[TState, TAction]) -> Perception:
        """Restituisce una **Perception** a partire da un **environment**, utilizzando il suo **self.sensor**"""
        return self.sensor.percept(environment)

    def executeAction(self, action: TAction, environment: Environment[TState, TAction]):
        """Esegue l'azione **action** sull'ambiente **environment**"""
        environment.evolveState(action)
