from __future__ import annotations

from typing import Optional, cast

from ai.action import Action
from ai.nodes.node import Node
from ai.state import State
from ai.tasks.game import Game


class GameNode(Node):
    def __init__(
        self,
        parent: Optional[GameNode],
        state: State,
        action: Optional[Action],
        utilities: list[float],
    ):
        """
        **parent**: *Optional[GameNode]*          - il nodo padre (None se è la radice)
        **children**: *list[Node]*                - i nodi figli associati
        **state**: *State*                        - lo stato associato al nodo
        **action**: *Optional[Action]*            - l'azione che ha portato a generare il nodo
        **utilities**: *list[float]*              - valore di utilità del nodo (stato) per ogni player
        """
        super().__init__(parent, state, action)
        self.utilities = utilities

    def createChild(self, newState: State, action: Action, game: Game) -> GameNode:
        return GameNode(
            parent=self,
            action=action,
            state=newState,
            utilities=[player.getUtility(newState) for player in game.players],
        )

    # solo per type checking
    def childNode(self, game: Game, action: Action) -> GameNode:
        return cast(GameNode, super().childNode(game, action))

    def addChild(self, child: GameNode) -> None:
        return super().addChild(child)

    # operators (by utility)
    def comparisonValue(self):
        return self
