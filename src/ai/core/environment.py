import textwrap
from abc import ABC, abstractmethod

from ai.core.action import Action
from ai.core.state import State


class Environment(ABC):
    def __init__(self, initialState: State):
        self.currentState = initialState

    def evolveState(self, action: Action, task: "Task") -> State:  # type: ignore
        """Evolve lo stato corrente, eseguendo l'azione richiesta"""
        self.currentState = task.transitionModel(self.currentState, action)
        return self.currentState

    def __str__(self) -> str:
        return f"Ambiente attuale:\n{textwrap.indent(str(self.currentState), "\t")}\n"
