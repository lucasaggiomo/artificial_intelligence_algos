from __future__ import annotations

from typing import Optional

from ai.core.action import Action
from ai.core.state import State
from ai.problems.problem import Problem


class ProblemNode:
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
        self.parent = parent
        self.children: list[ProblemNode] = []
        self.state = state
        self.action = action
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

    def addChild(self, child: ProblemNode) -> None:
        self.children.append(child)
        child.parent = self
        
    def childNode(self,  problem: Problem, action: Action) -> ProblemNode:
        """
        Crea un nodo figlio usando il metodo astratto `createChild` che ogni sottoclasse deve implementare.
        """
        newState = problem.transitionModel(self.state, action)

        # metodo astratto per creare un nodo figlio
        newNode = self.createChild(newState, action, problem)

        self.addChild(newNode)
        return newNode
    
    # operators (by pathCost)
    def comparisonValue(self):
        return self.pathCost

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
