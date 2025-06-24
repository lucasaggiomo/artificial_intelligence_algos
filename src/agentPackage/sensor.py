from typing import Generic

from agentPackage.action import TAction
from agentPackage.environment import Environment
from agentPackage.perception import Perception
from agentPackage.state import TState


class Sensor(Generic[TState, TAction]):
    def percept(self, environment: Environment[TState, TAction]) -> Perception:
        return environment.getCurrentState()
