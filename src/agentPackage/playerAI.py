from abc import ABC, abstractmethod
from typing import Generic

from src.agentPackage.action import A
from src.agentPackage.agent import Agent
from src.agentPackage.player import Player
from src.agentPackage.state import S
from src.agentPackage.tasks.game import Game
from src.agentPackage.taskSolvers.gameTheory import DecisionAlgorithmType


class PlayerAI(Generic[S, A], Player[S, A], ABC):
    def __init__(
        self,
        sensor,
        name: str,
        decisionAlgorithm: DecisionAlgorithmType,
        limit: float = float("+inf"),
    ):
        super().__init__(sensor, name)
        self.name = name
        self.decisionAlgorithm = decisionAlgorithm
        self.limit = limit

    def chooseAction(self, game: Game[S, A]):
        return self.decisionAlgorithm(game, self, self.limit)

    def __str__(self) -> str:
        return self.name
