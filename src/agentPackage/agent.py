from src.agentPackage.perception import Perception
from src.agentPackage.sensor import Sensor
from src.agentPackage.environment import Environment
from src.agentPackage.action import Action


class Agent:
    def __init__(self, sensor: Sensor):
        self.sensor = sensor

    def percept(self, environment: Environment) -> Perception:
        """Restituisce una **Perception** a partire da un **environment**, utilizzando il suo **self.sensor**"""
        return self.sensor.percept(environment)

    def executeAction(self, action: Action, environment: Environment):
        """Esegue l'azione **action** sull'ambiente **environment**"""
        environment.evolveState(action)
