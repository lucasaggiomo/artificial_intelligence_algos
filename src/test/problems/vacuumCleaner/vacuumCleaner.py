from __future__ import annotations

from agentPackage.action import Action
from agentPackage.agent import Agent
from agentPackage.environment import Environment
from agentPackage.goal import Goal
from agentPackage.sensor import StateSensor
from agentPackage.state import State
from agentPackage.tasks.problem import Problem


class VacuumState(State):
    VACUUM = 2
    LEFT = 1
    RIGHT = 0

    CLEAN = 0
    DIRTY = 1

    LEFT_MASK = 1 << LEFT
    RIGHT_MASK = 1 << RIGHT
    VACUUM_MASK = 1 << VACUUM

    POSITION_LABELS = {LEFT: "Left", RIGHT: "Right"}

    CLEANLINESS_LABELS = {CLEAN: "Clean", DIRTY: "Dirty"}

    def __init__(self, bitmap: int):
        if bitmap < 0 or bitmap > 8:
            raise ValueError(
                f"{bitmap} is not a valid VacuumState value (valid values are from 0 to 8)"
            )
        self.bitmap = bitmap

    def __str__(self) -> str:
        return f"Vacuum: {VacuumState.getVacuum(self.bitmap):>5}, Left: {VacuumState.getLeft(self.bitmap):>5}, Right: {VacuumState.getRight(self.bitmap):>5}"

    # def __repr__(self) -> str:
    #     return f"State({self.bitmap} - {self.__str__()})"

    def __eq__(self, other):
        return isinstance(other, VacuumState) and self.bitmap == other.bitmap

    def __hash__(self):
        return hash(self.bitmap)

    # metodi statici utili per conversioni in stringa
    @staticmethod
    def getVacuum(state: int) -> str:
        return VacuumState.POSITION_LABELS[(state & VacuumState.VACUUM_MASK) >> VacuumState.VACUUM]

    @staticmethod
    def getLeft(state: int) -> str:
        return VacuumState.CLEANLINESS_LABELS[(state & VacuumState.LEFT_MASK) >> VacuumState.LEFT]

    @staticmethod
    def getRight(state: int) -> str:
        return VacuumState.CLEANLINESS_LABELS[(state & VacuumState.RIGHT_MASK) >> VacuumState.RIGHT]


class VacuumAction(Action):
    LEFT = 0
    RIGHT = 1
    SUCK = 2
    NOOP = 3

    ACTION_LABELS = {LEFT: "Left", RIGHT: "Right", SUCK: "Suck", NOOP: "NoOp"}

    def __init__(self, value: int):
        if value not in VacuumAction.ACTION_LABELS.keys():
            raise ValueError(
                f"{value} is not a valid VacuumAction value (valid values are: {VacuumAction.ACTION_LABELS})"
            )
        self.value = value

    def __str__(self) -> str:
        return VacuumAction.ACTION_LABELS[self.value]

    # def __repr__(self) -> str:
    #     return f"Action({self.value} - {self.__str__()})"

    def __eq__(self, other):
        return isinstance(other, VacuumAction) and self.value == other.value

    def __hash__(self):
        return hash(self.value)


class VacuumGoal(Goal):
    def __init__(self, goalState: VacuumState):
        self.goalState = goalState

    def isGoalAchieved(self, state: State) -> bool:
        return state == self.goalState


class VacuumEnvironment(Environment):
    def transitionModel(self, state: VacuumState, action: VacuumAction) -> VacuumState:
        return _transitionModel(state, action)


class VacuumAgent(Agent):
    def __init__(self):
        super().__init__(StateSensor())


class VacuumProblem(Problem):
    def __init__(
        self,
        initialState: VacuumState,
        environment: VacuumEnvironment,
        agents: list[VacuumAgent],
        goal: VacuumGoal,
    ):
        super().__init__(initialState, environment, agents, goal)
        self.goal = goal

    def pathCostFunction(self, state: VacuumState, action: VacuumAction):
        return 0 if action == VacuumAction.NOOP else 1

    def heuristicDistFunction(self, state: VacuumState):
        return _heuristicDistFunction(state, self.goal)

    def getActionsFromState(self, state: VacuumState) -> list[VacuumAction]:
        return ALL_ACTIONS_PER_STATE[state]

    def transitionModel(self, state: VacuumState, action: VacuumAction) -> VacuumState:
        return _transitionModel(state, action)


def putBitInPosition(bitmap: int, bit: int, position: int) -> int:
    return (bitmap & ~(1 << position)) | (bit << position)


def _transitionModel(state: VacuumState, action: VacuumAction) -> VacuumState:
    return VacuumState(getNextBitmap(state.bitmap, action))


def getNextBitmap(bitmap: int, action: VacuumAction) -> int:
    if action.value == VacuumAction.LEFT:
        return putBitInPosition(bitmap, VacuumState.LEFT, VacuumState.VACUUM)

    if action.value == VacuumAction.RIGHT:
        return putBitInPosition(bitmap, VacuumState.RIGHT, VacuumState.VACUUM)

    if action.value == VacuumAction.SUCK:
        return putBitInPosition(
            bitmap,
            VacuumState.CLEAN,
            (bitmap & VacuumState.VACUUM_MASK) >> VacuumState.VACUUM,
        )

    if action.value == VacuumAction.NOOP:
        return bitmap

    raise ValueError(f"Azione non riconosciuta: {action}")


def _heuristicDistFunction(state: VacuumState, goal: VacuumGoal) -> int:
    current = state.bitmap
    goal_bitmap = goal.goalState.bitmap

    vacuum_pos = (current & VacuumState.VACUUM_MASK) >> VacuumState.VACUUM
    left_dirty = ((current & VacuumState.LEFT_MASK) >> VacuumState.LEFT) == VacuumState.DIRTY
    right_dirty = ((current & VacuumState.RIGHT_MASK) >> VacuumState.RIGHT) == VacuumState.DIRTY

    goal_left_clean = (
        (goal_bitmap & VacuumState.LEFT_MASK) >> VacuumState.LEFT
    ) == VacuumState.CLEAN
    goal_right_clean = (
        (goal_bitmap & VacuumState.RIGHT_MASK) >> VacuumState.RIGHT
    ) == VacuumState.CLEAN

    actions = 0

    # Se la sinistra deve essere pulita ma non lo è
    if goal_left_clean and left_dirty:
        if vacuum_pos != VacuumState.LEFT:
            actions += 1  # move to left
        actions += 1  # suck

    # Se la destra deve essere pulita ma non lo è
    if goal_right_clean and right_dirty:
        if vacuum_pos != VacuumState.RIGHT:
            actions += 1  # move to right
        actions += 1  # suck

    return actions


# variabili del problema
ALL_STATES = [VacuumState(i) for i in range(8)]
ALL_ACTIONS = [VacuumAction(a) for a in VacuumAction.ACTION_LABELS.keys()]

# tutte le azioni sono possibili in ogni stato
ALL_ACTIONS_PER_STATE = {state: ALL_ACTIONS for state in ALL_STATES}
