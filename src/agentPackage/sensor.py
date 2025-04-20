from typing import Generic

from src.agentPackage.environment import Environment
from src.agentPackage.perception import Perception
from src.agentPackage.typeVars import A, S


class Sensor(Generic[S, A]):
    def percept(self, environment: Environment[S, A]) -> Perception:
        return environment.getCurrentState()
