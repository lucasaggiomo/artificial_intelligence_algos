from __future__ import annotations

from typing import Optional, cast

from ai.action import Action
from ai.nodes.node import Node
from ai.state import State
from ai.tasks.problem import Problem
from ai.tasks.task import Task


class ProblemNode(Node):
    def __init__(
        self,
        parent: Optional[ProblemNode],
        state: State,
        action: Optional[Action],
        pathCost: float,
        heuristicDist: float,
    ):
        """
        **parent**: *Optional[ProblemNode]*       - il nodo padre (None se è la radice)
        **children**: *list[Node]*                - i nodi figli associati
        **state**: *State*                        - lo stato associato al nodo
        **action**: *Optional[Action]*            - l'azione che ha portato a generare il nodo
        **pathCost**: *float*                     - costo per raggiungere il nodo a partire dalla radice
        **heuristicDist**: *float*                - distanza heuristica dalla/e destinazione/i
        """
        super().__init__(parent, state, action)
        self.pathCost = pathCost
        self.heuristicDist = heuristicDist

    def createChild(self, newState: State, action: Action, problem: Problem) -> ProblemNode:
        return ProblemNode(
            parent=self,
            action=action,
            state=newState,
            pathCost=self.pathCost + problem.pathCostFunction(self.state, action),
            heuristicDist=problem.heuristicDistFunction(newState),
        )

    # solo per type checking
    def childNode(self, problem: Problem, action: Action) -> ProblemNode:
        return cast(ProblemNode, super().childNode(problem, action))

    def addChild(self, child: ProblemNode) -> None:
        return super().addChild(child)

    # operators (by pathCost)
    def comparisonValue(self):
        return self.pathCost
