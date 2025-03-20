from collections.abc import Callable

from .action import Action
from .state import State

type PathFunctionType = Callable[[State, Action], int]
type ActionTableType = dict[State, list[Action]]
type TransitionModelType = dict[tuple[State, Action], State]
type SolutionType = tuple[list[Action] | None, int] | None  # None = no solution, (None, int) = cutoff, ([...], int) = solution

type GoalFunctionType = Callable[[State], bool]