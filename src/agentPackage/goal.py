from abc import ABC, abstractmethod
from typing import Generic

from agentPackage.state import TState


class Goal(Generic[TState], ABC):
    """Obiettivo da perseguire"""

    @abstractmethod
    def isGoalAchieved(self, state: TState) -> bool:
        """Dato uno stato, restituisce `True` se ha raggiunto l'obiettivo prefissato, `False` altrimenti"""
        pass
