from __future__ import annotations

from typing import Generic, Self

from agentPackage.action import TAction
from agentPackage.nodes.node import Node
from agentPackage.player import Player
from agentPackage.state import TState
from agentPackage.tasks.game import Game


class GameNode(Generic[TState, TAction], Node[TState, TAction, Game[TState, TAction]]):
    def __init__(
        self,
        parent: Self,
        state: TState,
        action: TAction,
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

    def createChild(self, newState: TState, action: TAction, game: Game[TState, TAction]) -> Self:
        return GameNode[TState, TAction](
            parent=self,
            action=action,
            state=newState,
            utilities=[player.getUtility(newState) for player in game.agents],
        )

    # operators (by utility)
    def comparisonValue(self):
        return self
