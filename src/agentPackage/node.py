from __future__ import annotations

from .state import State
from .action import Action
from .task import Task

from abc import ABC, abstractmethod


class Node(ABC):

    def __init__(
        self,
        parent: Node,
        state: State,
        action: Action,
    ):
        """
        parent: Node                        # il nodo padre (None se è la radice)
        children: list[Node]                # i nodi figli associati
        state: State                        # lo stato associato al nodo
        action: Action                      # l'azione che ha portato a generare il nodo
        """
        self.parent = parent
        self.children = []
        self.state = state
        self.action = action

    def addChild(self, child: Node) -> None:
        self.children.append(child)
        child.parent = self

    def childNode(self, task: Task, action: Action) -> Node:
        """
        Crea un nodo figlio usando il metodo astratto `create_child` che ogni sottoclasse deve implementare.
        """
        newState = task.getNextState(self.state, action)

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
    def comparison_value(self):
        # unreachable
        pass

    def __lt__(self, other) -> bool:
        """self < other."""
        return (
            isinstance(other, Node)
            and self.comparison_value() < other.comparison_value()
        )

    def __le__(self, other) -> bool:
        """self <= other."""
        return (
            isinstance(other, Node)
            and self.comparison_value() <= other.comparison_value()
        )

    def __eq__(self, other) -> bool:
        """self == other."""
        return (
            isinstance(other, Node)
            and self.comparison_value() == other.comparison_value()
        )

    def __ne__(self, other) -> bool:
        """self != other."""
        return (
            isinstance(other, Node)
            and self.comparison_value() != other.comparison_value()
        )

    def __gt__(self, other) -> bool:
        """self > other."""
        return (
            isinstance(other, Node)
            and self.comparison_value() > other.comparison_value()
        )

    def __ge__(self, other) -> bool:
        """self >= other."""
        return (
            isinstance(other, Node)
            and self.comparison_value() >= other.comparison_value()
        )
