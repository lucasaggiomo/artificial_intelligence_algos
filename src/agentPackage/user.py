from abc import ABC, abstractmethod
from typing import Generic

from src.agentPackage.player import Player
from src.agentPackage.typeVars import A, S


class User(Generic[S, A], Player[S, A], ABC):
    @abstractmethod
    def chooseAction(self):
        pass
