from typing import Generic

from src.agentPackage.customTypes import (
    ActionsPerStateType,
    HeuristicStateOnlyFunctionType,
    PathFunctionType,
    TransitionModelType,
)
from src.agentPackage.environment import Environment
from src.agentPackage.goal import Goal, HeuristicFunctionType
from src.agentPackage.tasks.task import Task
from src.agentPackage.typeVars import A, S


class Problem(Generic[S, A], Task[S, A]):
    def __init__(
        self,
        initialState: S,
        environment: Environment[S, A],
        actionsPerState: ActionsPerStateType[S, A],
        transitionModel: TransitionModelType[S, A],
        goal: Goal,
        pathCostFunction: PathFunctionType,
        heuristicDistFunction: HeuristicFunctionType = None,
    ):
        """
        **initialState**: *S*                                     - stato di partenza\\
        **environment**: *Environment*                                - ambiente del sistema\\
        **actionsPerState**: *ActionsPerStateType*                    - associa ad ogni stato l'insieme delle possibili azioni\\
        **transitionModel**: *TransitionModelType*                    - associa ad ogni azione, a partire da uno stato, lo stato successivo\\
        **goal**: *Goal*                                              - obiettivo
        **pathCostFunction**: *PathFunctionType*                      . funzione del costo di un percorso, dato stato e azione
        **heuristicDistFunction**: *HeuristicStateOnlyFunctionType*   - funzione heuristica della distanza di uno stato dalla/e destinazione/i
        """
        super().__init__(initialState, environment, actionsPerState, transitionModel)
        self.goal = goal
        self.pathCostFunction = pathCostFunction
        self.heuristicDistFunction = lambda state: heuristicDistFunction(state, self.goal)

    def isGoalAchieved(self, state: S) -> bool:
        return self.goal.isGoalAchieved(state)

    def __str__(self) -> str:
        return f"Parto da:\n{self.initialState}\nDevo raggiungere l'obiettivo:\n{self.goal}\n"
