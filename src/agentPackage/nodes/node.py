from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Self

from src.agentPackage.action import A
from src.agentPackage.state import S
from src.agentPackage.tasks.task import T


class Node(Generic[S, A, T], ABC):
    @abstractmethod
    def __init__(
        self,
        parent: Self,
        state: S,
        action: A,
    ):
        """
        **parent**: *Self*                        - il nodo padre (None se è la radice)
        **children**: *list[Self]*                - i nodi figli associati
        **state**: *State*                        - lo stato associato al nodo
        **action**: *Action*                      - l'azione che ha portato a generare il nodo
        """
        self.parent = parent
        self.children: list[Self] = []
        self.state = state
        self.action = action

    def addChild(self, child: Self) -> None:
        self.children.append(child)
        child.parent = self

    def childNode(self, task: T, action: A) -> Self:
        """
        Crea un nodo figlio usando il metodo astratto `createChild` che ogni sottoclasse deve implementare.
        """
        newState = task.transitionModel(self.state, action)

        # metodo astratto per creare un nodo figlio
        newNode = self.createChild(newState, action, task)

        self.addChild(newNode)
        return newNode

    @abstractmethod
    def createChild(self, newState: S, action: A, task: T) -> Self:
        """
        Metodo che ogni sottoclasse deve implementare per restituire una nuova istanza del proprio tipo.
        """
        pass

    # operators by comparison value
    @abstractmethod
    def comparisonValue(self):
        # unreachable
        pass

    def __lt__(self, other) -> bool:
        """self < other."""
        return isinstance(other, type(self)) and self.comparisonValue() < other.comparisonValue()

    def __le__(self, other) -> bool:
        """self <= other."""
        return isinstance(other, type(self)) and self.comparisonValue() <= other.comparisonValue()

    def __eq__(self, other) -> bool:
        """self == other."""
        return isinstance(other, type(self)) and self.comparisonValue() == other.comparisonValue()

    def __ne__(self, other) -> bool:
        """self != other."""
        return isinstance(other, type(self)) and self.comparisonValue() != other.comparisonValue()

    def __gt__(self, other) -> bool:
        """self > other."""
        return isinstance(other, type(self)) and self.comparisonValue() > other.comparisonValue()

    def __ge__(self, other) -> bool:
        """self >= other."""
        return isinstance(other, type(self)) and self.comparisonValue() >= other.comparisonValue()
