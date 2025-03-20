from agentPackage.goal import Goal
from agentPackage.problem import Problem
from agentPackage.agent import Agent
from agentPackage.environment import Environment
from agentPackage.sensor import Sensor
from agentPackage.agent import Agent
from agentPackage.problemSolving import ProblemSolving

from agentPackage.customTypes import (
    ActionTableType,
    TransitionModelType,
    PathFunctionType,
)

import problemFormulations.googleMaps as maps
from problemFormulations.googleMaps import (
    CityState,
    MoveAction,
    transitionModel,
    actions,
    states,
    actionsPerState,
    pathCostFunction,
)

# Definizione del problema
# initialState = s((s.DIRTY << s.LEFT) | (s.CLEAN << s.RIGHT) | (s.RIGHT << s.VACUUM))
# goalState = s((s.CLEAN << s.LEFT) | (s.CLEAN << s.RIGHT) | (s.RIGHT << s.VACUUM))
initialState = CityState("Arad")
# goalState = CityState("Urziceni")
goal = Goal(lambda state: len(state.name) > 7, lambda: 'Una qualunque città con nome più lungo di 7 lettere')

problem = Problem(
    states,
    initialState,
    actions,
    actionsPerState,
    transitionModel,
    goal,
    pathCostFunction,
)


def reset():
    global environment, sensor, agent, solver

    environment = Environment(initialState, transitionModel)
    sensor = Sensor()
    agent = Agent(environment, sensor)
    solver = ProblemSolving(agent, problem)


# risolvi il problema
reset()

print(f"-------------------------- PROBLEMA --------------------------")
print(problem)

print("BreadthFirstSearch:")
solver.simpleProblemSolvingAgent(ProblemSolving.breadthFirstSearch)

reset()
print("\nUniformSearch:")
solver.simpleProblemSolvingAgent(ProblemSolving.uniformSearch)

reset()
print("\nDepthFirstSearch:")
solver.simpleProblemSolvingAgent(ProblemSolving.depthFirstSearch)

reset()
print("\nDepthFirstSearchRecursive:")
solver.simpleProblemSolvingAgent(ProblemSolving.depthFirstSearchRecursive)

reset()
print("\nIterativeDeepeningSearch:")
solver.simpleProblemSolvingAgent(ProblemSolving.iterativeDeepeningSearch)
