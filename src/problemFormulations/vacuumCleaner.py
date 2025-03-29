from __future__ import annotations

from agentPackage.state import State
from agentPackage.action import Action


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
        return VacuumState.POSITION_LABELS[
            (state & VacuumState.VACUUM_MASK) >> VacuumState.VACUUM
        ]

    @staticmethod
    def getLeft(state: int) -> str:
        return VacuumState.CLEANLINESS_LABELS[
            (state & VacuumState.LEFT_MASK) >> VacuumState.LEFT
        ]

    @staticmethod
    def getRight(state: int) -> str:
        return VacuumState.CLEANLINESS_LABELS[
            (state & VacuumState.RIGHT_MASK) >> VacuumState.RIGHT
        ]


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


def getAllStates(cls) -> list[VacuumState]:
    return [cls(i) for i in range(8)]


def getAllActions(cls) -> list[VacuumAction]:
    return [cls(a) for a in VacuumAction.ACTION_LABELS.keys()]


def putBitInPosition(bitmap: int, bit: int, position: int) -> int:
    return (bitmap & ~(1 << position)) | (bit << position)


def getNextState(state: VacuumState, action: VacuumAction) -> VacuumState:
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


def pathCostFunction(state: State, action: Action) -> int:
    return 0 if action == VacuumAction.NOOP else 1


# variabili del problema
states = getAllStates()
actions = getAllActions()

# tutte le azioni sono possibili in ogni stato
actionsPerState = {state: actions for state in states}

transitionModel = {
    (state, action): getNextState(state, action)
    for state in states
    for action in actions
}
