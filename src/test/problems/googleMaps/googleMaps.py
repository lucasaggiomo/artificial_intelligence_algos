from __future__ import annotations

from typing import Callable

from ai.action import Action
from ai.agent import Agent
from ai.environment import Environment
from ai.goal import Goal
from ai.sensor import StateSensor
from ai.state import State
from ai.tasks.problem import Problem


class CityState(State):
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    # def __repr__(self) -> str:
    #     return f"State({self.bitmap} - {self.__str__()})"

    def __eq__(self, other):
        return isinstance(other, CityState) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class MoveAction(Action):
    def __init__(self, from_city: CityState, to_city: CityState):
        self.from_city = from_city
        self.to_city = to_city

    def __str__(self) -> str:
        return f"Move from {self.from_city} to {self.to_city}"

    def __eq__(self, other):
        return (
            isinstance(other, MoveAction)
            and self.from_city == other.from_city
            and self.to_city == other.to_city
        )

    def __hash__(self):
        return hash((self.from_city, self.to_city))


class GoogleMapsGoal(Goal):
    def __init__(self, goalState: CityState):
        self.goalState = goalState

    def isGoalAchieved(self, state: State) -> bool:
        return state == self.goalState


class GoogleMapsEnvironment(Environment):
    def transitionModel(self, state: CityState, action: MoveAction) -> CityState:
        return _transitionModel(state, action)


class GoogleMapsAgent(Agent):
    def __init__(self):
        super().__init__(StateSensor())


class GoogleMapsProblem(Problem):
    def __init__(
        self,
        initialState: CityState,
        environment: GoogleMapsEnvironment,
        agents: list[GoogleMapsAgent],
        goal: GoogleMapsGoal,
    ):
        super().__init__(initialState, environment, agents, goal)
        self.goal = goal

    def pathCostFunction(self, state: CityState, action: MoveAction):
        return _pathCostFunction(state, action)

    def heuristicDistFunction(self, state: CityState):
        return _heuristicDistFunction(state, self.goal)

    def getActionsFromState(self, state: CityState) -> list[MoveAction]:
        return _getActionsPerState(state)

    def transitionModel(self, state: CityState, action: MoveAction) -> CityState:
        return _transitionModel(state, action)


# città
city_names = [
    "Arad",
    "Zerind",
    "Oradea",
    "Sibiu",
    "Timisoara",
    "Lugoj",
    "Mehadia",
    "Drobeta",
    "Craiova",
    "Riminicu Vilcea",
    "Fagaras",
    "Pitesti",
    "Bucharest",
    "Giurgiu",
    "Urziceni",
    "Vaslui",
    "Iasi",
    "Neamt",
    "Hirsova",
    "Eforie",
]
states = [CityState(name) for name in city_names]

INF = float("inf")
# Matrice dei costi
costMatrix = {
    "Arad": {
        "Arad": 0,
        "Zerind": 75,
        "Sibiu": 140,
        "Timisoara": 118,
    },
    "Zerind": {
        "Arad": 75,
        "Zerind": 0,
        "Oradea": 71,
    },
    "Oradea": {
        "Zerind": 71,
        "Oradea": 0,
        "Sibiu": 151,
    },
    "Sibiu": {
        "Arad": 140,
        "Oradea": 151,
        "Sibiu": 0,
        "Riminicu Vilcea": 80,
        "Fagaras": 99,
    },
    "Timisoara": {
        "Arad": 118,
        "Timisoara": 0,
        "Lugoj": 111,
    },
    "Lugoj": {
        "Timisoara": 111,
        "Lugoj": 0,
        "Mehadia": 70,
    },
    "Mehadia": {
        "Lugoj": 70,
        "Mehadia": 0,
        "Drobeta": 75,
    },
    "Drobeta": {
        "Mehadia": 75,
        "Drobeta": 0,
        "Craiova": 120,
    },
    "Craiova": {
        "Drobeta": 120,
        "Craiova": 0,
        "Riminicu Vilcea": 146,
        "Pitesti": 138,
    },
    "Riminicu Vilcea": {
        "Sibiu": 80,
        "Craiova": 146,
        "Riminicu Vilcea": 0,
        "Pitesti": 97,
    },
    "Fagaras": {
        "Sibiu": 99,
        "Fagaras": 0,
        "Bucharest": 211,
    },
    "Pitesti": {
        "Craiova": 138,
        "Riminicu Vilcea": 97,
        "Pitesti": 0,
        "Bucharest": 101,
    },
    "Bucharest": {
        "Fagaras": 211,
        "Pitesti": 101,
        "Bucharest": 0,
        "Giurgiu": 90,
        "Urziceni": 85,
    },
    "Giurgiu": {
        "Bucharest": 90,
        "Giurgiu": 0,
    },
    "Urziceni": {
        "Bucharest": 85,
        "Urziceni": 0,
        "Vaslui": 142,
        "Hirsova": 98,
    },
    "Vaslui": {
        "Urziceni": 142,
        "Vaslui": 0,
        "Iasi": 92,
    },
    "Iasi": {
        "Vaslui": 92,
        "Iasi": 0,
        "Neamt": 87,
    },
    "Neamt": {
        "Iasi": 87,
        "Neamt": 0,
    },
    "Hirsova": {
        "Urziceni": 98,
        "Hirsova": 0,
        "Eforie": 86,
    },
    "Eforie": {
        "Hirsova": 86,
        "Eforie": 0,
    },
}

# heuristica (distanza in linea d'aria) [per semplicità, solo rispetto a Bucharest]
sld = {
    "Arad": 366,
    "Zerind": 374,
    "Oradea": 380,
    "Sibiu": 253,
    "Timisoara": 329,
    "Lugoj": 244,
    "Mehadia": 241,
    "Drobeta": 242,
    "Craiova": 160,
    "Riminicu Vilcea": 193,
    "Fagaras": 176,
    "Pitesti": 100,
    "Bucharest": 0,
    "Giurgiu": 77,
    "Urziceni": 80,
    "Vaslui": 199,
    "Iasi": 226,
    "Neamt": 234,
    "Hirsova": 151,
    "Eforie": 161,
}

# Creazione delle azioni possibili
actions = []
actionsPerStateTable = {}

for state in states:
    city_name = state.name
    actions_from_city = []

    if city_name in costMatrix:
        for destination, cost in costMatrix[city_name].items():
            destination_state = next(s for s in states if s.name == destination)
            action = MoveAction(state, destination_state)
            actions.append(action)
            actions_from_city.append(action)

    actionsPerStateTable[state] = actions_from_city


def _getActionsPerState(state: CityState) -> list[MoveAction]:
    return actionsPerStateTable[state]


def _transitionModel(state: CityState, action: MoveAction) -> CityState:
    if state != action.from_city:
        raise ValueError("Inconsistent arguments")
    return action.to_city


# Funzione di costo del percorso
def _pathCostFunction(state: CityState, action: MoveAction) -> int | float:
    return costMatrix[state.name].get(action.to_city.name, INF)


def heuristicDistance(start: CityState, stop: CityState) -> int:
    if stop.name != "Bucharest":
        raise NotImplementedError(
            "I can't calculate yet an heuristic distance on a destination different from Bucharest."
        )
    return sld[start.name]


def _heuristicDistFunction(state: CityState, goal: GoogleMapsGoal) -> int:
    return heuristicDistance(state, goal.goalState)
