from abc import ABC, abstractmethod
from typing import Sequence

from ai.core.environment import Environment
from ai.core.state import State
from ai.core.task import Task
from ai.games.player import Player


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
