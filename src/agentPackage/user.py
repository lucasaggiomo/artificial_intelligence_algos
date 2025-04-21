from abc import ABC, abstractmethod
from typing import Generic

from src.agentPackage.action import A
from src.agentPackage.player import Player
from src.agentPackage.state import S
from src.agentPackage.tasks.game import Game


class User(Generic[S, A], Player[S, A], ABC):
    @abstractmethod
    def chooseAction(self, game: Game[S, A]):
        pass
