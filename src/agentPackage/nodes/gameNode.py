from __future__ import annotations

from typing import Generic, Self

from src.agentPackage.nodes.node import Node
from src.agentPackage.tasks.game import Game
from src.agentPackage.typeVars import A, S


class GameNode(Generic[S, A], Node[S, A, Game[S, A]]):
    def __init__(
        self,
        parent: Self,
        state: S,
        action: A,
        utility: float,
    ):
        """
        **parent**: *Node*                        - il nodo padre (None se è la radice)
        **children**: *list[Node]*                - i nodi figli associati
        **state**: *State*                        - lo stato associato al nodo
        **action**: *Action*                      - l'azione che ha portato a generare il nodo
        **utility**: *float*                      - valore di utilità del nodo (stato)
        """
        super().__init__(parent, state, action)
        self.utility = utility

    def createChild(self, newState: S, action: A, game: Game[S, A]) -> Self:
        return GameNode[S, A](
            parent=self,
            action=action,
            state=newState,
            utility=game.utilityFunction(newState),
        )

    # operators (by utility)
    def comparisonValue(self):
        return self
