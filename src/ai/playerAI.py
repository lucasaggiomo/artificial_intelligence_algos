from abc import ABC, abstractmethod

from ai.player import Player
from ai.sensor import Sensor
from ai.tasks.game import Game
from ai.taskSolvers.gameTheory import DecisionAlgorithmType


class PlayerAI(Player, ABC):
    def __init__(
        self,
        sensor: Sensor,
        name: str,
        decisionAlgorithm: DecisionAlgorithmType,
        limit: float = float("+inf"),
    ):
        Player.__init__(self, sensor, name)
        self.name = name
        self.decisionAlgorithm = decisionAlgorithm
        self.limit = limit
        self.visited = set()

    def chooseAction(self, game: Game):
        return self.decisionAlgorithm(
            game,
            self,
            self.visited,
            self.limit,
        )

    def __str__(self) -> str:
        return self.name
