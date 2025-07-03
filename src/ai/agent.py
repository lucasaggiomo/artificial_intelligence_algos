from ai.action import Action
from ai.environment import Environment
from ai.sensor import Perception, Sensor


class Agent:
    def __init__(self, sensor: Sensor):
        self.sensor = sensor

    def percept(self, environment: Environment) -> Perception:
        """Restituisce una **Perception** a partire da un **environment**, utilizzando il suo **self.sensor**"""
        return self.sensor.percept(environment)

    def executeAction(self, action: Action, environment: Environment):
        """Esegue l'azione **action** sull'ambiente **environment**"""
        environment.evolveState(action)
