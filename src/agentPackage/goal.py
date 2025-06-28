from abc import ABC, abstractmethod

from agentPackage.state import State


class Goal(ABC):
    """Obiettivo da perseguire"""

    @abstractmethod
    def isGoalAchieved(self, state: State) -> bool:
        """Dato uno stato, restituisce `True` se ha raggiunto l'obiettivo prefissato, `False` altrimenti"""
        pass
