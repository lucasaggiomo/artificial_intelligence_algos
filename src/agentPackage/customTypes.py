from collections.abc import Callable

from .action import Action
from .state import State
from .goal import Goal

type PathFunctionType = Callable[[State, Action], float]
type HeuristicFunctionType = Callable[[State, Goal], float]
type HeuristicStateOnlyFunctionType = Callable[[State], float]
type ActionsPerStateType = Callable[[State], list[Action]]
type TransitionModelType = Callable[[State, Action], State]
type SolutionType = tuple[list[Action] | None, float] | None  # None = no solution, (None, float) = cutoff, ([...], float) = solution

type UtilityFunctionType = Callable[[State], float]
type TerminalTestFunctionType = Callable[[State], bool]