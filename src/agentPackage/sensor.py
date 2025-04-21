from typing import Generic

from src.agentPackage.action import A
from src.agentPackage.environment import Environment
from src.agentPackage.perception import Perception
from src.agentPackage.state import S


class Sensor(Generic[S, A]):
    def percept(self, environment: Environment[S, A]) -> Perception:
        return environment.getCurrentState()
