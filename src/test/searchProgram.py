from collections.abc import Callable
from test.problemFormulations.nPuzzle import (
    NPuzzleAgent,
    NPuzzleEnvironment,
    NPuzzleGoal,
    NPuzzleProblem,
    NPuzzleProblemSolving,
    generateRandomState,
    generateSortedState,
    manhattanDistance,
)
from threading import Event, Thread
from typing import Optional

from agentPackage.taskSolvers.problemSolving import (
    ProblemSolving,
    SearchAlgorithmType,
    SolutionType,
)

# import test.problemFormulations.googleMaps as maps
# from test.problemFormulations.googleMaps import (
#     CityState,
#     MoveAction,
#     transitionModel,
#     actionsPerState,
#     pathCostFunction,
#     heuristicDistFunction,
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
) -> SolutionType:
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
    global name

    def reset():
        environment.currenState = initialState

    # Definizione del problema
    # initialState = s((s.DIRTY << s.LEFT) | (s.CLEAN << s.RIGHT) | (s.RIGHT << s.VACUUM))
    # goalState = s((s.CLEAN << s.LEFT) | (s.CLEAN << s.RIGHT) | (s.RIGHT << s.VACUUM))

    DIMENSION = 3
    # initialState = NPuzzleState((3, 4, 1, 5, 7, 8, 0, 6, 2), 3)
    initialState = generateRandomState(DIMENSION)
    goalState = generateSortedState(DIMENSION)

    # initialState = CityState('Arad')
    # goalState = CityState('Bucharest')
    goal = NPuzzleGoal(goalState)
    environment = NPuzzleEnvironment(initialState)
    agent = NPuzzleAgent()
    problem = NPuzzleProblem(initialState, environment, [agent], goal, manhattanDistance)
    solver = NPuzzleProblemSolving(agent, problem)

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
            searchAlgorithm: SearchAlgorithmType = getattr(solver, algorithm)
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
                elif solution is None:
                    print("Solution era None")
                    return
                else:
                    actions, cost = solution
                    if actions == None:
                        print("Actiosn era None")
                        return

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
