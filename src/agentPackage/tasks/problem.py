from src.agentPackage.tasks.task import Task
from src.agentPackage.goal import Goal
from src.agentPackage.state import State
from src.agentPackage.environment import Environment
from src.agentPackage.customTypes import (
    ActionsPerStateType,
    TransitionModelType,
    PathFunctionType,
    HeuristicFunctionType,
    HeuristicStateOnlyFunctionType,
)


class Problem(Task):
    def __init__(
        self,
        initialState: State,
        environment: Environment,
        actionsPerState: ActionsPerStateType,
        transitionModel: TransitionModelType,
        goal: Goal,
        pathCostFunction: PathFunctionType,
        heuristicDistFunction: HeuristicFunctionType = None,
    ):
        """
        **initialState**: *State*                                     - stato di partenza\\
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
        self.heuristicDistFunction = lambda state: heuristicDistFunction(
            state, self.goal
        )

    def isGoalAchieved(self, state: State) -> bool:
        return self.goal.isGoalAchieved(state)

    def __str__(self) -> str:
        return f"Parto da:\n{self.initialState}\nDevo raggiungere l'obiettivo:\n{self.goal}\n"
