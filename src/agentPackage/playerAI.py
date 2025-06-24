from abc import ABC, abstractmethod
from typing import Generic

from agentPackage.action import TAction
from agentPackage.agent import Agent
from agentPackage.player import Player
from agentPackage.state import TState
from agentPackage.tasks.game import Game
from agentPackage.taskSolvers.gameTheory import DecisionAlgorithmType


class PlayerAI(Generic[TState, TAction], Player[TState, TAction], ABC):
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

    def chooseAction(self, game: Game[TState, TAction]):
        return self.decisionAlgorithm(game, self, self.limit)

    def __str__(self) -> str:
        return self.name
