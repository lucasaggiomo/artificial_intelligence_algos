from src.agentPackage.perception import Perception
from src.agentPackage.environment import Environment


class Sensor:
    def percept(self, environment: Environment) -> Perception:
        return Perception(environment.getCurrentState())
