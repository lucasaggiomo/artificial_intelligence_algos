from abc import ABC, abstractmethod

from ai.action import Action
from ai.agent import Agent
from ai.sensor import Sensor
from ai.state import State


class Player(Agent, ABC):
    def __init__(self, sensor: Sensor, name: str):
        super().__init__(sensor)
        self.name = name

    @abstractmethod
    def getUtility(self, state: State) -> float:
        """Restituisce il valore di utilità relativo al player rispetto allo stato in ingresso"""
        pass

    @abstractmethod
    def chooseAction(self, game: "Game") -> Action:  # type: ignore
        pass

    def __str__(self) -> str:
        return self.name
