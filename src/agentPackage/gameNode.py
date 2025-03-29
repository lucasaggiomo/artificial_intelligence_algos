from __future__ import annotations

from .node import Node

from .state import State
from .action import Action
from .game import Game


class GameNode(Node):

    def __init__(
        self,
        parent: GameNode,
        state: State,
        action: Action,
        utility: float,
    ):
        """
        parent: Node                        # il nodo padre (None se è la radice)
        children: list[Node]                # i nodi figli associati
        state: State                        # lo stato associato al nodo
        action: Action                      # l'azione che ha portato a generare il nodo
        utility: float                      # valore di utilità del nodo (stato)
        """
        self.parent = parent
        self.children = []
        self.state = state
        self.action = action
        self.utility = utility

    def createChild(self, newState: State, action: Action, game: Game) -> GameNode:
        return GameNode(
            parent=self,
            action=action,
            state=newState,
            utility=game.utilityFunction(newState),
        )

    # operators (by utility)
    def comparison_value(self):
        return self
