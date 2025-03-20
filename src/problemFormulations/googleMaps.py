from __future__ import annotations

from agentPackage.state import State
from agentPackage.action import Action


class CityState(State):
    name: str

    def __init__(self, name: int):
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
    from_city: CityState
    to_city: CityState

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

# Creazione delle azioni possibili
actions = []
actionsPerState = {}

for state in states:
    city_name = state.name
    actions_from_city = []

    if city_name in costMatrix:
        for destination, cost in costMatrix[city_name].items():
            destination_state = next(s for s in states if s.name == destination)
            action = MoveAction(state, destination_state)
            actions.append(action)
            actions_from_city.append(action)

    actionsPerState[state] = actions_from_city

# Modello di transizione: associa (stato, azione) al nuovo stato
transitionModel = {(action.from_city, action): action.to_city for action in actions}

# Funzione di costo del percorso
def pathCostFunction(state: CityState, action: MoveAction) -> int:
    return costMatrix[state.name].get(
        action.to_city.name, INF
    )