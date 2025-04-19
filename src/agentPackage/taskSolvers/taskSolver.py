from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.agentPackage.tasks.task import Task
from src.agentPackage.agent import Agent

# Assuming that we have a pair of types Animal and Bear, and Bear is a subtype of Animal, these are defined as follows:
# A generic class MyCovGen[T] is called covariant in type parameter T if MyCovGen[Bear] is a subtype of MyCovGen[Animal]. This is the most intuitive form of variance.
T = TypeVar("T", bound=Task, covariant=True)


# useless for now
class TaskSolver(Generic[T], ABC):
    @abstractmethod
    def __init__(self, agents: list[Agent], task: T):
        self.agents = agents
        self.task = task

    # @abstractmethod
    # def solve(self):
    #     pass
