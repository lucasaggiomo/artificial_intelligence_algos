# --------------------------------- DEPRECATED ---------------------------------

# from collections.abc import Callable

# from src.agentPackage.action import Action
# from src.agentPackage.state import State

# from src.agentPackage.goal import Goal

# type PathFunctionType[S: State, A: Action] = Callable[[S, A], float]
# type HeuristicStateOnlyFunctionType[S: State, A: Action] = Callable[[S], float]
# type ActionsPerStateType[S: State, A: Action] = Callable[[S], list[A]]
# type TransitionModelType[S: State, A: Action] = Callable[[S, A], S]

# None = no solution, (None, float) = cutoff, ([...], float) = solution

# type UtilityFunctionType[S: State] = Callable[[S], float]
# type TerminalTestFunctionType[S: State] = Callable[[S], bool]
