from abc import ABC, abstractmethod
from typing import Generic

from src.agentPackage.action import A
from src.agentPackage.agent import Agent
from src.agentPackage.state import S
from src.agentPackage.tasks.task import T


# useless for now
class TaskSolver(Generic[S, A, T], ABC):
    @abstractmethod
    def __init__(self, task: T):
        self.task = task

    # @abstractmethod
    # def solve(self):
    #     pass
