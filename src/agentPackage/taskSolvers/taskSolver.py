from abc import ABC, abstractmethod
from typing import Generic

from agentPackage.action import TAction
from agentPackage.agent import Agent
from agentPackage.state import TState
from agentPackage.tasks.task import TTask


# useless for now
class TaskSolver(Generic[TState, TAction, TTask], ABC):
    @abstractmethod
    def __init__(self, task: TTask):
        self.task = task

    # @abstractmethod
    # def solve(self):
    #     pass
