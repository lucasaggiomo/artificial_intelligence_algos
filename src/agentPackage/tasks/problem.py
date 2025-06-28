from abc import ABC, abstractmethod
from typing import Sequence

from agentPackage.action import Action
from agentPackage.agent import Agent
from agentPackage.environment import Environment
from agentPackage.goal import Goal
from agentPackage.state import State
from agentPackage.tasks.task import Task


class Problem(Task, ABC):
    @abstractmethod
    def __init__(
        self,
        initialState: State,
        environment: Environment,
        agents: Sequence[Agent],
        goal: Goal,
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
    def pathCostFunction(self, state: State, action: Action) -> float:
        """Funzione del costo di un percorso, dato stato e azione"""
        pass

    @abstractmethod
    def heuristicDistFunction(self, state: State) -> float:
        """Funzione heuristica della distanza di uno stato dalla/e destinazione/i"""
        # prima era così:
        # self.heuristicDistFunction = lambda state: heuristicDistFunction(state, self.goal)
        pass

    def isGoalAchieved(self, state: State) -> bool:
        return self.goal.isGoalAchieved(state)

    def __str__(self) -> str:
        return f"Parto da:\n{self.initialState}\nDevo raggiungere l'obiettivo:\n{self.goal}\n"
