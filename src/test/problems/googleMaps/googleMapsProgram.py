from collections.abc import Callable
from test.problems.googleMaps.googleMaps import (
    CityState,
    GoogleMapsAgent,
    GoogleMapsEnvironment,
    GoogleMapsGoal,
    GoogleMapsProblem,
)
from threading import Event, Thread

from agentPackage.taskSolvers.problemSolving import (
    ProblemSolving,
    SearchAlgorithmType,
    SolutionType,
)


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
        environment.currentState = initialState

    initialState = CityState("Arad")
    goalState = CityState("Bucharest")
    goal = GoogleMapsGoal(goalState)
    environment = GoogleMapsEnvironment(initialState)
    agent = GoogleMapsAgent()
    problem = GoogleMapsProblem(initialState, environment, [agent], goal)
    solver = ProblemSolving(agent, problem)

    print(f"-------------------------- PROBLEMA --------------------------")
    print(problem)

    algorithmsToTry = [
        "breadthFirstSearch",
        "depthFirstSearch",
        "depthFirstSearchRecursive",
        "iterativeDeepeningSearch",
        "uniformSearch",
        "greedySearch",
        "aStarSearch",
    ]

    with open("./test/nPuzzleOutput.txt", mode="w") as logger:

        def log(message: str, logToStdout: bool = True):
            if logToStdout:
                print(message)
            logger.write(f"{message}\n")

        algorithmsTimeMap: dict[str, float] = {}
        algorithmsCostMap: dict[str, float] = {}

        for algorithm in algorithmsToTry:
            name = capitalize_first_letter(algorithm)
            log(f"{name}:")
            searchAlgorithm: SearchAlgorithmType = getattr(solver, algorithm)
            try:
                from timeit import default_timer as timer

                start = timer()
                solution = runWithTimeout(searchAlgorithm, problem, timeout=10, log=log)
                end = timer()

                time = end - start
                log(f"Search algorithm time: {time}s")

                if solution is None:
                    raise ValueError("Solution era None")

                if solution is ProblemSolving.CUTOFF:
                    log(
                        "Nessuna soluzione trovata (non e' stato visitato tutto l'albero degli stati a causa di timeout o errori interni)"
                    )
                    time = float("+inf")
                    cost = float("+inf")
                elif solution is ProblemSolving.NO_SOLUTIONS:
                    log("Non ci sono soluzioni")
                    time = float("+inf")
                    cost = float("+inf")
                else:
                    actions, cost = solution
                    if actions == None:
                        print("Actions era None")
                        return

                    log(f"Soluzione trovata (Costo {cost})")
                    for i in range(len(actions)):
                        log(f"{f'{i+1}.':<5}\t{actions[i]}", logToStdout=False)

                algorithmsTimeMap[name] = time
                algorithmsCostMap[name] = cost

                log("-----------------------------------")
            except Exception as e:
                log(f"Algorithm {name} did not succeed: {e}")
            reset()
            log("")

        # ordina per costo crescente e tempo decrescente
        sorted_by_cost = sorted(algorithmsCostMap.items(), key=lambda item: item[1])
        sorted_by_time = sorted(algorithmsTimeMap.items(), key=lambda item: item[1])

        # trova il costo minimo e tempo massimo
        min_cost = sorted_by_cost[0][1]
        max_time = sorted_by_time[0][1]

        # trova tutti gli algoritmi con quel costo o tempo
        cheapest_algos = [name for name, cost in sorted_by_cost if cost == min_cost]
        fastest_algos = [name for name, time in sorted_by_time if time == max_time]

        # mostra i risultati
        log(f"Algoritmo(i) piu' veloce(i) con tempo {max_time}s: {', '.join(fastest_algos)}")
        log(
            f"Algoritmo(i) con soluzione meno costosa con costo {min_cost}: {', '.join(cheapest_algos)}"
        )


if __name__ == "__main__":
    main()
