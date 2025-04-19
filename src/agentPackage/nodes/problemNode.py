from __future__ import annotations

from src.agentPackage.nodes.node import Node
from src.agentPackage.tasks.problem import Problem
from src.agentPackage.state import State
from src.agentPackage.action import Action


class ProblemNode(Node[Problem]):
    def __init__(
        self,
        parent: ProblemNode,
        state: State,
        action: Action,
        pathCost: float,
        heuristicDist: float,
    ):
        """
        parent: Node                        # il nodo padre (None se è la radice)
        children: list[Node]                # i nodi figli associati
        state: State                        # lo stato associato al nodo
        action: Action                      # l'azione che ha portato a generare il nodo
        pathCost: float                       # costo per raggiungere il nodo a partire dalla radice
        heuristicDist: float                   # distanza heuristica dalla/e destinazione/i
        """
        super().__init__(parent, state, action)
        self.pathCost = pathCost
        self.heuristicDist = heuristicDist

    def createChild(
        self, newState: State, action: Action, problem: Problem
    ) -> ProblemNode:
        return ProblemNode(
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

    # operators (by pathCost)
    def comparisonValue(self):
        return self.pathCost
