from abc import ABC, abstractmethod

from agentPackage.tasks.task import Task


# useless for now
class TaskSolver(ABC):
    @abstractmethod
    def __init__(self, task: Task):
        self.task = task

    # @abstractmethod
    # def solve(self):
    #     pass
