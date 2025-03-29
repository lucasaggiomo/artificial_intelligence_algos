from collections.abc import Callable

from .action import Action
from .state import State
from .goal import Goal

type PathFunctionType = Callable[[State, Action], int]
type HeuristicFunctionType = Callable[[State, Goal], int]
type HeuristicStateOnlyFunctionType = Callable[[State], int]
type ActionsPerStateType = Callable[[State], list[Action]]
type TransitionModelType = Callable[[State, Action], State]
type SolutionType = tuple[list[Action] | None, int] | None  # None = no solution, (None, int) = cutoff, ([...], int) = solution
