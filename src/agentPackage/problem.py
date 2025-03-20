from .goal import Goal
from .action import Action
from .state import State

from .customTypes import ActionTableType, TransitionModelType, PathFunctionType

class Problem:
    states: list[State]                                 # insieme dei possibili stati
    initialState: State                                 # stato di partenza
    actions: list[Action]                               # insieme delle azioni possibili
    actionsPerState: ActionTableType                    # associa ad ogni stato l'insieme delle possibili azioni
    transitionModel: TransitionModelType                # associa ad ogni azione, a partire da uno stato, lo stato successivo
    goal: Goal                                          # obiettivo
    pathCostFunction: PathFunctionType                  # funzione del costo di un percorso
    
    def __init__(self,
                 states: list[State],
                 initialState: State,
                 actions: list[Action],
                 actionsPerState: ActionTableType,
                 transitionModel: TransitionModelType,
                 goal: Goal,
                 pathCostFunction: PathFunctionType):
        self.states = states
        self.initialState = initialState
        self.actions = actions
        self.actionsPerState = actionsPerState
        self.transitionModel = transitionModel
        self.goal = goal
        self.pathCostFunction = pathCostFunction
        
    def getActionsFromState(self, state: State) -> list[Action]:
        """
            ACTIONS\n
            Restituisce l'insieme delle azioni possibili da un certo stato
        """
        return self.actionsPerState[state]

    def getNextState(self, state: State, action: Action) -> State:
        """
            RESULT\n
            Restituisce lo stato ottenuto eseguendo un'azione a partire da un certo stato
        """
        return self.transitionModel[(state, action)]
    
    def isGoalAchieved(self, state: State) -> bool:
        return self.goal.isGoalAchieved(state)
    
    def __str__(self) -> str:
        output = f"Parto da:\n\t{self.initialState}\nDevo raggiungere l'obiettivo:\n\t{self.goal}\nAzioni possibili: {self.actions}\nAzioni per stato:\n"
        for state, actions in self.actionsPerState.items():
            output += f"\t{state}\t===>\t{", ".join([action.__str__() for action in actions])}\n"
        output += "\nStato successivo per azione e stato:\n"
        for key, state in self.transitionModel.items():
            output += f"\tSTATE[\"{key[0]}\"] - ACTION[\"{key[1]}\"]\t===>\tSTATE[\"{state}\"]\n"
        return output