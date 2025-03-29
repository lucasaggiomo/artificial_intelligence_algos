from __future__ import annotations

from .state import State
from .action import Action
from .problem import Problem


class Node:

    def __init__(
        self,
        parent: Node,
        state: State,
        action: Action,
        pathCost: int,
        heuristicDist: int,
    ):
        """
        parent: Node                        # il nodo padre (None se è la radice)
        children: list[Node]                # i nodi figli associati
        state: State                        # lo stato associato al nodo
        action: Action                      # l'azione che ha portato a generare il nodo
        pathCost: int                       # costo per raggiungere il nodo a partire dalla radice
        heuristicDist: int                   # distanza heuristica dalla/e destinazione/i
        """
        self.parent = parent
        self.children = []
        self.state = state
        self.action = action
        self.pathCost = pathCost
        self.heuristicDist = heuristicDist

    def addChild(self, child: Node) -> None:
        self.children.append(child)
        child.parent = self

    def childNode(self, problem: Problem, action: Action) -> Node:
        """
        Restituisce il nodo figlio ottenuto eseguendo un'azione sul nodo corrente, relativo ad un problema.
        Inoltre aggiunge il nodo figlio ottenuto alla lista dei nodi figli del nodo corrente.
        """

        newState = problem.getNextState(self.state, action)

        newNode = Node(
            parent=self,
            action=action,
            state=newState,
            pathCost=self.pathCost + problem.pathCostFunction(self.state, action),
            heuristicDist=(
                problem.heuristicDistFunction(newState)
                if problem.heuristicDistFunction is not None
                else 0
            ),
        )
        self.addChild(newNode)
        return newNode

    # operators (by pathCost)
    def __comparison_value(self):
        return self.pathCost

    def __lt__(self, other) -> bool:
        """self < other."""
        return (
            isinstance(other, Node)
            and self.__comparison_value() < other.__comparison_value()
        )

    def __le__(self, other) -> bool:
        """self <= other."""
        return (
            isinstance(other, Node)
            and self.__comparison_value() <= other.__comparison_value()
        )

    def __eq__(self, other) -> bool:
        """self == other."""
        return (
            isinstance(other, Node)
            and self.__comparison_value() == other.__comparison_value()
        )

    def __ne__(self, other) -> bool:
        """self != other."""
        return (
            isinstance(other, Node)
            and self.__comparison_value() != other.__comparison_value()
        )

    def __gt__(self, other) -> bool:
        """self > other."""
        return (
            isinstance(other, Node)
            and self.__comparison_value() > other.__comparison_value()
        )

    def __ge__(self, other) -> bool:
        """self >= other."""
        return (
            isinstance(other, Node)
            and self.__comparison_value() >= other.__comparison_value()
        )
