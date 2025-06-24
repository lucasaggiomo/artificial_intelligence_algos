from abc import ABC, abstractmethod
from typing import TypeVar

TAction = TypeVar("TAction", bound="Action")


class Action(ABC):
    """Classe astratta per rappresentare un'azione generica."""

    @abstractmethod
    def __str__(self) -> str:
        """Rappresentazione leggibile dell'azione."""
        pass

    def __repr__(self) -> str:
        return self.__str__()

    @abstractmethod
    def __hash__(self) -> int:
        """Rende lo stato hashabile (utile per set e dizionari)."""
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass
