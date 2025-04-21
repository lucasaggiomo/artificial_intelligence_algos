from __future__ import annotations

from typing import Generic, Self

from src.agentPackage.action import A
from src.agentPackage.nodes.node import Node
from src.agentPackage.player import Player
from src.agentPackage.state import S
from src.agentPackage.tasks.game import Game


class GameNode(Generic[S, A], Node[S, A, Game[S, A]]):
    def __init__(
        self,
        parent: Self,
        state: S,
        action: A,
        utilities: list[float],
    ):
        """
        **parent**: *Node*                        - il nodo padre (None se è la radice)
        **children**: *list[Node]*                - i nodi figli associati
        **state**: *State*                        - lo stato associato al nodo
        **action**: *Action*                      - l'azione che ha portato a generare il nodo
        **utilities**: *list[float]*              - valore di utilità del nodo (stato) per ogni player
        """
        super().__init__(parent, state, action)
        self.utilityies = utilities

    def createChild(self, newState: S, action: A, game: Game[S, A]) -> Self:
        return GameNode[S, A](
            parent=self,
            action=action,
            state=newState,
            utilities=[player.getUtility(newState) for player in game.agents],
        )

    # operators (by utility)
    def comparisonValue(self):
        return self
