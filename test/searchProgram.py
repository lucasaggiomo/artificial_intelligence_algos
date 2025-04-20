import test.problemFormulations.nPuzzle as puzzle
from collections.abc import Callable
from test.problemFormulations.nPuzzle import (MoveAction, NPuzzleState,
                                              actionsPerState,
                                              generateRandomState,
                                              generateSortedState,
                                              heuristicDistFunction,
                                              manhattanDistance,
                                              pathCostFunction,
                                              transitionModel)
from threading import Event, Thread

from src.agentPackage.agent import Agent
from src.agentPackage.customTypes import (ActionsPerStateType,
                                          PathFunctionType,
                                          TransitionModelType)
from src.agentPackage.environment import Environment
from src.agentPackage.goal import Goal
from src.agentPackage.sensor import Sensor
from src.agentPackage.state import State
from src.agentPackage.tasks.problem import Problem
from src.agentPackage.taskSolvers.problemSolving import (ProblemSolving,
                                                         SearchAlgorithmType)

# import test.problemFormulations.googleMaps as maps
# from test.problemFormulations.googleMaps import (
#     CityState,
#     MoveAction,
#     transitionModel,
#     actionsPerState,
#     pathCostFunction,
#     heuristicDistFunction,
#     # manhattanDistance,
#     # generateRandomState,
#     # generateSortedState,
# )


def capitalize_first_letter(string: str) -> str:
    if string is None or len(string) == 0:
        return string
    if len(string) == 1:
        return string.upper()

    return string[0].upper() + string[1::]


# Funzione per eseguire l'algoritmo di ricerca con un limite di tempo
def runWithTimeout(
    searchAlgorithm: SearchAlgorithmType,
    problem,
    timeout: float,
    log: Callable[[str], None],
):
    global name

    solution = None
    stopEvent = Event()

    def search():
        nonlocal solution
        try:
            solution = searchAlgorithm(problem, stopEvent)
        except Exception as e:
            log(f"Algorithm {name} did not succeed: {e}")

    searchThread = Thread(target=search)
    searchThread.start()

    searchThread.join(timeout)

    if searchThread.is_alive():
        log(f"Tempo scaduto dopo {timeout} secondi!")
        stopEvent.set()
        return ProblemSolving.CUTOFF

    searchThread.join()

    return solution


def main():
    def reset():
        global environment, sensor, agent, solver

        environment = Environment(initialState, transitionModel)
        sensor = Sensor()
        agent = Agent(sensor)
        solver = ProblemSolving(agent, problem)

    # Definizione del problema
    # initialState = s((s.DIRTY << s.LEFT) | (s.CLEAN << s.RIGHT) | (s.RIGHT << s.VACUUM))
    # goalState = s((s.CLEAN << s.LEFT) | (s.CLEAN << s.RIGHT) | (s.RIGHT << s.VACUUM))

    DIMENSION = 3
    initialState = NPuzzleState((3, 4, 1, 5, 7, 8, 0, 6, 2), 3)
    goalState = generateSortedState(DIMENSION)
    goalMap = goalState.createGoalMap()

    # initialState = CityState('Arad')
    # goalState = CityState('Bucharest')
    goal = Goal(
        lambda state: state == goalState, lambda: f"{goalState}", context=goalState
    )

    environment = Environment(initialState, transitionModel)

    problem = Problem(
        initialState,
        environment,
        actionsPerState,
        transitionModel,
        goal,
        pathCostFunction,
        heuristicDistFunction=lambda state, goal: heuristicDistFunction(
            state, goal, goalMap, manhattanDistance
        ),
    )

    sensor = Sensor()
    agent = Agent(sensor)
    solver = ProblemSolving(agent, problem)

    # risolvi il problema
    # reset()

    print(f"-------------------------- PROBLEMA --------------------------")
    print(problem)

    algorithmsToTry = [
        # "breadthFirstSearch",
        # "depthFirstSearch",
        # "depthFirstSearchRecursive",
        # "iterativeDeepeningSearch",
        "uniformSearch",
        "greedySearch",
        "aStarSearch",
    ]

    with open("./test/output.txt", mode="w") as logger:

        def log(message: str, logToStdout: bool = True):
            if logToStdout:
                print(message)
            logger.write(f"{message}\n")

        for algorithm in algorithmsToTry:
            name = capitalize_first_letter(algorithm)
            log(f"{name}:")
            searchAlgorithm: SearchAlgorithmType = getattr(ProblemSolving, algorithm)
            try:
                from timeit import default_timer as timer

                start = timer()
                solution = runWithTimeout(searchAlgorithm, problem, timeout=10, log=log)
                end = timer()

                log(f"Search algorithm time: {end - start}")

                if solution is ProblemSolving.CUTOFF:
                    log(
                        "Nessuna soluzione trovata (non e' stato visitato tutto l'albero degli stati a causa di timeout o errori interni)"
                    )
                elif solution is ProblemSolving.NO_SOLUTIONS:
                    log("Non ci sono soluzioni")
                else:
                    actions, cost = solution
                    log(f"Soluzione trovata (Costo {cost})")
                    for i in range(len(actions)):
                        log(f"{f'{i+1}.':<5}\t{actions[i]}", logToStdout=False)

                log("-----------------------------------")
            except Exception as e:
                log(f"Algorithm {name} did not succeed: {e}")
            reset()
            log("")


if __name__ == "__main__":
    main()
