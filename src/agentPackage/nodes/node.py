from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from agentPackage.action import Action
from agentPackage.state import State
from agentPackage.tasks.task import Task


class Node(ABC):
    @abstractmethod
    def __init__(
        self,
        parent: Optional[Node],
        state: State,
        action: Optional[Action],
    ):
        """
        **parent**: *Optional[Node]*              - il nodo padre (None se è la radice)
        **children**: *list[Node]*                - i nodi figli associati
        **state**: *State*                        - lo stato associato al nodo
        **action**: *Optional[Action]*            - l'azione che ha portato a generare il nodo
        """
        self.parent = parent
        self.children: list[Node] = []
        self.state = state
        self.action = action

    def addChild(self, child: Node) -> None:
        self.children.append(child)
        child.parent = self

    def childNode(self, task: Task, action: Action) -> Node:
        """
        Crea un nodo figlio usando il metodo astratto `createChild` che ogni sottoclasse deve implementare.
        """
        newState = task.transitionModel(self.state, action)

        # metodo astratto per creare un nodo figlio
        newNode = self.createChild(newState, action, task)

        self.addChild(newNode)
        return newNode

    @abstractmethod
    def createChild(self, newState: State, action: Action, task: Task) -> Node:
        """
        Metodo che ogni sottoclasse deve implementare per restituire una nuova istanza del proprio tipo.
        """
        pass

    # operators by comparison value
    @abstractmethod
    def comparisonValue(self) -> int | float:
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
