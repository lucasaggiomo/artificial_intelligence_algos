from __future__ import annotations

from typing import Generic, Self

from src.agentPackage.nodes.node import Node
from src.agentPackage.tasks.problem import Problem
from src.agentPackage.typeVars import A, S


class ProblemNode(Generic[S, A], Node[S, A, Problem[S, A]]):
    def __init__(
        self,
        parent: Self,
        state: S,
        action: A,
        pathCost: float,
        heuristicDist: float,
    ):
        """
        **parent**: *Node*                        - il nodo padre (None se è la radice)
        **children**: *list[Node]*                - i nodi figli associati
        **state**: *State*                        - lo stato associato al nodo
        **action**: *Action*                      - l'azione che ha portato a generare il nodo
        **pathCost**: *float*                       - costo per raggiungere il nodo a partire dalla radice
        **heuristicDist**: *float*                   - distanza heuristica dalla/e destinazione/i
        """
        super().__init__(parent, state, action)
        self.pathCost = pathCost
        self.heuristicDist = heuristicDist

    def createChild(self, newState: S, action: A, problem: Problem[S, A]) -> Self:
        return ProblemNode[S, A](
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
