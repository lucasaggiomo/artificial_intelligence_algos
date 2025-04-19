from abc import ABC, abstractmethod

from src.agentPackage.agent import Agent
from src.agentPackage.action import Action
from src.agentPackage.environment import Environment


class Player(Agent, ABC):
    @abstractmethod
    def executeAction(self, action: Action, environment: Environment):
        pass
