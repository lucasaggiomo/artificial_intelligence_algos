from abc import ABC, abstractmethod
from typing import Generic

from src.agentPackage.action import A
from src.agentPackage.agent import Agent
from src.agentPackage.environment import Environment
from src.agentPackage.goal import Goal
from src.agentPackage.state import S
from src.agentPackage.tasks.task import Task


class Problem(Generic[S, A], Task[S, A, Agent[S, A]], ABC):
    @abstractmethod
    def __init__(
        self,
        initialState: S,
        environment: Environment[S, A],
        agents: list[Agent[S, A]],
        goal: Goal[S],
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
    def pathCostFunction(self, state: S, action: A) -> float:
        """Funzione del costo di un percorso, dato stato e azione"""
        pass

    @abstractmethod
    def heuristicDistFunction(self, state: S) -> float:
        """Funzione heuristica della distanza di uno stato dalla/e destinazione/i"""
        # prima era così:
        # self.heuristicDistFunction = lambda state: heuristicDistFunction(state, self.goal)
        pass

    def isGoalAchieved(self, state: S) -> bool:
        return self.goal.isGoalAchieved(state)

    def __str__(self) -> str:
        return f"Parto da:\n{self.initialState}\nDevo raggiungere l'obiettivo:\n{self.goal}\n"
