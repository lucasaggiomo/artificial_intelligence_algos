from abc import ABC, abstractmethod

from agentPackage.player import Player
from agentPackage.sensor import Sensor
from agentPackage.tasks.game import Game
from agentPackage.taskSolvers.gameTheory import DecisionAlgorithmType


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

    def chooseAction(self, game: Game):
        return self.decisionAlgorithm(game, self, self.limit)

    def __str__(self) -> str:
        return self.name
