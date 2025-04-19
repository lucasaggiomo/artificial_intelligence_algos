from __future__ import annotations

from src.agentPackage.nodes.node import Node
from src.agentPackage.tasks.game import Game
from src.agentPackage.state import State
from src.agentPackage.action import Action


class GameNode(Node[Game]):

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
        super().__init__(parent, state, action)
        self.utility = utility

    def createChild(self, newState: State, action: Action, game: Game) -> GameNode:
        return GameNode(
            parent=self,
            action=action,
            state=newState,
            utility=game.utilityFunction(newState),
        )

    # operators (by utility)
    def comparisonValue(self):
        return self
