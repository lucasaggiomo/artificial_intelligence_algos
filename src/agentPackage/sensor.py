from .perception import Perception
from .environment import Environment

class Sensor:
    def getPerception(self, environment: Environment) -> Perception:
        return Perception(environment.getCurrentState())
