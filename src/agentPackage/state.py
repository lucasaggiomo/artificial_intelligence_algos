from abc import ABC, abstractmethod
from typing import TypeVar

TState = TypeVar("TState", bound="State")


class State(ABC):
    """Classe astratta per rappresentare uno stato generico."""

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Definisce l'uguaglianza tra stati."""
        pass

    @abstractmethod
    def __hash__(self) -> int:
        """Rende lo stato hashabile (utile per set e dizionari)."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Rappresentazione leggibile dello stato."""
        pass

    def __repr__(self) -> str:
        return self.__str__()
