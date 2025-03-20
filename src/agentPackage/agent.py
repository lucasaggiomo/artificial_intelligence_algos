from .perception import Perception
from .sensor import Sensor
from .environment import Environment
from .action import Action

class Agent:
    sensor: Sensor
    environment: Environment
    
    def __init__(self, environment: Environment, sensor : Sensor):
        self.environment = environment
        self.sensor = sensor
    
    def percept(self) -> Perception:
        return self.sensor.getPerception(self.environment)
    
    def executeAction(self, action: Action):
        print(f"Eseguo azione: {action}")
        new_state = self.environment.evolveState(action)
        self.environment.render()