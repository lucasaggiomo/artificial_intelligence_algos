from abc import ABC, abstractmethod
from typing import Optional

from ai.core.action import Action
from ai.core.agent import Agent
from ai.core.sensor import Sensor
from ai.core.state import State


class Player(Agent, ABC):
    def __init__(self, sensor: Sensor, name: str):
        super().__init__(sensor)
        self.name = name

    @abstractmethod
    def getUtility(self, state: State) -> float:
        """Restituisce il valore di utilità relativo al player rispetto allo stato in ingresso"""
        pass

    @abstractmethod
    def chooseAction(self, game: "Game") -> Optional[Action]:  # type: ignore
        pass

    def __str__(self) -> str:
        return self.name


class PlayerAI(Player, ABC):
    def __init__(
        self,
        sensor: Sensor,
        name: str,
        decisionAlgorithm: "DecisionAlgorithmType",  # type: ignore
        limit: float = float("+inf"),
    ):
        Player.__init__(self, sensor, name)
        self.name = name
        self.decisionAlgorithm = decisionAlgorithm
        self.limit = limit
        self.visited = set()

    def chooseAction(self, game: "Game") -> Optional[Action]:  # type: ignore
        return self.decisionAlgorithm(
            game,
            self,
            self.visited,
            self.limit,
        )

    def __str__(self) -> str:
        return self.name
