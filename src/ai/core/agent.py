from ai.core.action import Action
from ai.core.environment import Environment
from ai.core.sensor import Perception, Sensor


class Agent:
    def __init__(self, sensor: Sensor):
        self.sensor = sensor

    def percept(self, environment: Environment) -> Perception:
        """Restituisce una **Perception** a partire da un **environment**, utilizzando il suo **self.sensor**"""
        return self.sensor.percept(environment)

    def executeAction(self, action: Action, environment: Environment):
        """Esegue l'azione **action** sull'ambiente **environment**"""
        environment.evolveState(action)
