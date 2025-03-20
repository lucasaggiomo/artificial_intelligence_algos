from .state import State
from collections.abc import Callable

from .customTypes import GoalFunctionType

class Goal:
    """Obiettivo da perseguire"""
    
    achievedGoalFunction: GoalFunctionType
    toStr: Callable[[], str]
    
    def __init__(self, achievedGoalFunction: GoalFunctionType, toStr: Callable[[], str] = None):
        self.achievedGoalFunction = achievedGoalFunction
        self.toStr = toStr
        
    def isGoalAchieved(self, state: State) -> bool:
        return self.achievedGoalFunction(state)
    
    def __str__(self) -> str:
        if self.toStr is None:
            return super().__str__()
        return self.toStr()