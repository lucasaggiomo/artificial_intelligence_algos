from abc import ABC, abstractmethod
from typing import Sequence

from agentPackage.environment import Environment
from agentPackage.player import Player
from agentPackage.state import State
from agentPackage.tasks.task import Task


class Game(Task, ABC):
    """A Game is a Task whose agents are players"""

    @abstractmethod
    def __init__(
        self,
        initialState: State,
        environment: Environment,
        players: Sequence[Player],
    ):
        """
        **initialState**: *State*                                     - stato di partenza\\
        **environment**: *Environment*                                - ambiente del sistema\\
        **players**: *list[Player]*                                   - players presenti nel sistema\\
        """
        super().__init__(initialState, environment, players)
        self.players = players

    @abstractmethod
    def terminalTest(self, state: State) -> bool:
        """
        Restituisce `True` se lo stato **state** è di terminazione (cioè uno stato di *GameOver*)
        """
        pass
