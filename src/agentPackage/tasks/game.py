from abc import ABC, abstractmethod
from typing import Generic

from agentPackage.action import TAction
from agentPackage.environment import Environment
from agentPackage.player import Player
from agentPackage.state import TState
from agentPackage.tasks.task import Task


class Game(Generic[TState, TAction], Task[TState, TAction, Player[TState, TAction]], ABC):
    """A Game is a Task whose agents are players"""

    @abstractmethod
    def __init__(
        self,
        initialState: TState,
        environment: Environment[TState, TAction],
        players: list[Player[TState, TAction]],
    ):
        """
        **initialState**: *State*                                     - stato di partenza\\
        **environment**: *Environment*                                - ambiente del sistema\\
        **players**: *list[Player]*                                   - players presenti nel sistema\\
        """
        super().__init__(initialState, environment, players)

    @abstractmethod
    def terminalTest(self, state: TState) -> bool:
        """
        Restituisce `True` se lo stato **state** è di terminazione (cioè uno stato di *GameOver*)
        """
        pass
