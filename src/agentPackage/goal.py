from src.agentPackage.state import State

from collections.abc import Callable

type GoalFunctionType = Callable[[State], bool]


class Goal:
    """Obiettivo da perseguire"""
    def __init__(
        self,
        achievedGoalFunction: GoalFunctionType,
        toStr: Callable[[], str] = None,
        context=None,
    ):
        self.achievedGoalFunction = achievedGoalFunction
        self.toStr = toStr
        self.context = context

    def isGoalAchieved(self, state: State) -> bool:
        return self.achievedGoalFunction(state)

    def __str__(self) -> str:
        if self.toStr is None:
            return super().__str__()
        return self.toStr()
