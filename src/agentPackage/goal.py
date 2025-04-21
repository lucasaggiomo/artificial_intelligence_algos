from abc import ABC, abstractmethod
from typing import Generic

from src.agentPackage.state import S


class Goal(Generic[S], ABC):
    """Obiettivo da perseguire"""

    @abstractmethod
    def __init__(self, context=None):
        self.context = context

    @abstractmethod
    def isGoalAchieved(self, state: S) -> bool:
        """Dato uno stato, restituisce `True` se ha raggiunto l'obiettivo prefissato, `False` altrimenti"""
        pass
