from abc import ABC, abstractmethod
from typing import Generic

from src.agentPackage.agent import Agent
from src.agentPackage.tasks.task import T
from src.agentPackage.typeVars import A, S


# useless for now
class TaskSolver(Generic[S, A, T], ABC):
    @abstractmethod
    def __init__(self, agents: list[Agent[S, A]], task: T):
        self.agents = agents
        self.task = task

    # @abstractmethod
    # def solve(self):
    #     pass
