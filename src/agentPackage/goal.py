from collections.abc import Callable
from typing import Generic

from src.agentPackage.state import State
from src.agentPackage.typeVars import S

type GoalFunctionType[S: State] = Callable[[S], bool]
type HeuristicFunctionType[S: State] = Callable[[S, Goal], float]


class Goal(Generic[S]):
    """Obiettivo da perseguire"""

    def __init__(
        self,
        achievedGoalFunction: GoalFunctionType[S],
        toStr: Callable[[], str] = None,
        context=None,
    ):
        self.achievedGoalFunction = achievedGoalFunction
        self.toStr = toStr
        self.context = context

    def isGoalAchieved(self, state: S) -> bool:
        return self.achievedGoalFunction(state)

    def __str__(self) -> str:
        if self.toStr is None:
            return super().__str__()
        return self.toStr()
