from .perception import Perception
from .sensor import Sensor
from .environment import Environment
from .action import Action
from .state import State


class Agent:
    def __init__(self, environment: Environment, sensor: Sensor):
        self.environment = environment
        self.sensor = sensor

    def percept(self) -> Perception:
        return self.sensor.getPerception(self.environment)

    def executeAction(self, action: Action) -> State:
        """Esegue l'azione sull'ambiente e restituisce lo stato successivo dell'ambiente"""
        return self.environment.evolveState(action)
        # self.environment.render()
