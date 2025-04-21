from abc import ABC, abstractmethod
from typing import Generic

from src.agentPackage.action import A
from src.agentPackage.environment import Environment
from src.agentPackage.player import Player
from src.agentPackage.state import S
from src.agentPackage.tasks.task import Task


class Game(Generic[S, A], Task[S, A, Player[S, A]], ABC):
    """A Game is a Task whose agents are players"""

    @abstractmethod
    def __init__(
        self,
        initialState: S,
        environment: Environment[S, A],
        players: list[Player[S, A]],
    ):
        """
        **initialState**: *State*                                     - stato di partenza\\
        **environment**: *Environment*                                - ambiente del sistema\\
        **players**: *list[Player]*                                   - players presenti nel sistema\\
        """
        super().__init__(initialState, environment, players)

    @abstractmethod
    def terminalTest(self, state: S) -> bool:
        """
        Restituisce `True` se lo stato **state** è di terminazione (cioè uno stato di *GameOver*)
        """
        pass
