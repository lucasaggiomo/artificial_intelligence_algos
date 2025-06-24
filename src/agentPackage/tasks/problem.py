from abc import ABC, abstractmethod
from typing import Generic

from agentPackage.action import TAction
from agentPackage.agent import Agent
from agentPackage.environment import Environment
from agentPackage.goal import Goal
from agentPackage.state import TState
from agentPackage.tasks.task import Task


class Problem(Generic[TState, TAction], Task[TState, TAction, Agent[TState, TAction]], ABC):
    @abstractmethod
    def __init__(
        self,
        initialState: TState,
        environment: Environment[TState, TAction],
        agents: list[Agent[TState, TAction]],
        goal: Goal[TState],
    ):
        """
        **initialState**: *State*                                     - stato di partenza\\
        **environment**: *Environment*                                - ambiente del sistema\\
        **agents**: *list[Agent]*                                     - agenti presenti nel sistema\\
        **goal**: *Goal*                                              - obiettivo
        """
        super().__init__(initialState, environment, agents)
        self.goal = goal

    @abstractmethod
    def pathCostFunction(self, state: TState, action: TAction) -> float:
        """Funzione del costo di un percorso, dato stato e azione"""
        pass

    @abstractmethod
    def heuristicDistFunction(self, state: TState) -> float:
        """Funzione heuristica della distanza di uno stato dalla/e destinazione/i"""
        # prima era così:
        # self.heuristicDistFunction = lambda state: heuristicDistFunction(state, self.goal)
        pass

    def isGoalAchieved(self, state: TState) -> bool:
        return self.goal.isGoalAchieved(state)

    def __str__(self) -> str:
        return f"Parto da:\n{self.initialState}\nDevo raggiungere l'obiettivo:\n{self.goal}\n"
