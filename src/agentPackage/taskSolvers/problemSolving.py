from collections import deque
from collections.abc import Callable
from heapq import *
from threading import Event
from typing import Generic

from agentPackage.action import Action, TAction
from agentPackage.agent import Agent
from agentPackage.nodes.problemNode import ProblemNode
from agentPackage.state import State, TState
from agentPackage.tasks.problem import Problem
from agentPackage.taskSolvers.taskSolver import TaskSolver

type SolutionType[A: Action] = tuple[list[A] | None, float] | None
type SearchAlgorithmType[S: State, A: Action] = Callable[[Problem[S, A], Event], SolutionType[A]]
type CostFunctionType[S: State, A: Action] = Callable[[ProblemNode[S, A]], float]


class ProblemSolving(Generic[TState, TAction], TaskSolver[TState, TAction, Problem[TState, TAction]]):
    CUTOFF = None
    NO_SOLUTIONS = [None, -1]

    def __init__(self, agent: Agent[TState, TAction], problem: Problem[TState, TAction]):
        super().__init__(problem)

        self.agent = agent
        self.problem = problem
        self.currentState = problem.initialState

    def simpleProblemSolvingAgent(
        self,
        search: SearchAlgorithmType[TState, TAction],
        stopEvent: Event,
        executeSolution: bool = False,
        print_problem: bool = False,
    ):
        # algoritmo generico di ricerca (BFS, DFS, ...), trova la soluzione, intesa come sequenza di azioni
        if print_problem:
            print(f"-------------------------- PROBLEMA --------------------------")
            print(self.problem)

        print("\nCerco una soluzione...")
        solution = search(self.problem, stopEvent)
        if solution is None:
            # cutoff
            print("Nessuna soluzione trovata, ma non è stato visitato tutto l'albero degli stati")
            return

        actions, cost = solution
        if actions is None:
            # no solutions
            print("Non ci sono soluzioni")
            return

        print(f"Soluzione trovata (Costo {cost})")
        for i in range(len(actions)):
            print(f"{f'{i+1}.':<5}\t{actions[i]}")

        if executeSolution:
            print("Inizio l'esecuzione...")
            self.problem.environment.render()
            for action in actions:
                self.agent.executeAction(action, self.problem.environment)
                self.currentState = self.problem.environment.getCurrentState()

    @staticmethod
    def backtrackSolution(node: ProblemNode[TState, TAction]) -> SolutionType[TAction]:
        actions = deque()
        cost = node.pathCost
        curr = node
        while curr.parent is not None:
            actions.appendleft(curr.action)
            curr = curr.parent
        return (list[TAction](actions), cost)

    @staticmethod
    def breadthFirstSearch(problem: Problem[TState, TAction], stopEvent: Event) -> SolutionType[TAction]:
        node = ProblemNode[TState, TAction](
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        if problem.isGoalAchieved(node.state):
            return ProblemSolving[TState, TAction].backtrackSolution(node)

        fringe: deque[ProblemNode[TState, TAction]] = deque()
        fringe.appendleft(node)

        explored: set[TState] = set()

        while True:
            if stopEvent.is_set():
                return ProblemSolving.CUTOFF

            if len(fringe) == 0:
                return ProblemSolving.NO_SOLUTIONS

            # prende il più vecchio nodo inserito e lo espande
            node = fringe.pop()
            explored.add(node.state)

            # per ogni azione trova il nodo destinazione corrispondente
            # quindi, se lo stato associato non è stato già esplorato,
            # verifica se ha raggiunto l'obiettivo e in tal caso restituisce la soluzione;
            # altrimenti aggiunge il nodo alla frontiera
            for action in problem.getActionsFromState(node.state):
                child = node.childNode(problem, action)
                if child.state not in explored:
                    if problem.isGoalAchieved(child.state):
                        return ProblemSolving[TState, TAction].backtrackSolution(child)
                    fringe.appendleft(child)

    @staticmethod
    def depthFirstSearch(problem: Problem[TState, TAction], stopEvent: Event) -> SolutionType[TAction]:
        node = ProblemNode[TState, TAction](
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        if problem.isGoalAchieved(node.state):
            return ProblemSolving[TState, TAction].backtrackSolution(node)

        fringe: deque[ProblemNode[TState, TAction]] = deque()
        fringe.append(node)

        explored: set[TState] = set()

        while True:
            if stopEvent.is_set():
                return ProblemSolving.CUTOFF

            if len(fringe) == 0:
                return ProblemSolving.NO_SOLUTIONS

            # prende l'ultimo nodo inserito e lo espande
            node = fringe.pop()
            explored.add(node.state)

            # per ogni azione trova il nodo destinazione corrispondente
            # quindi, se lo stato associato non è stato già esplorato,
            # verifica se ha raggiunto l'obiettivo e in tal caso restituisce la soluzione;
            # altrimenti aggiunge il nodo alla frontiera
            for action in problem.getActionsFromState(node.state):
                child = node.childNode(problem, action)
                if child.state not in explored:
                    if problem.isGoalAchieved(child.state):
                        return ProblemSolving[TState, TAction].backtrackSolution(child)
                    fringe.append(child)

    @staticmethod
    def depthFirstSearchRecursive(problem: Problem[TState, TAction], stopEvent: Event) -> SolutionType[TAction]:
        initialNode = ProblemNode[TState, TAction](
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        explored: set[TState] = set()
        return ProblemSolving[TState, TAction].depthFirstSearchRecursiveHelper(
            problem, stopEvent, initialNode, explored
        )

    @staticmethod
    def depthFirstSearchRecursiveHelper(
        problem: Problem[TState, TAction], stopEvent: Event, node: ProblemNode[TState, TAction], explored: set[TState]
    ) -> SolutionType[TAction]:
        if stopEvent.is_set():
            return ProblemSolving.CUTOFF

        if problem.isGoalAchieved(node.state):
            return ProblemSolving[TState, TAction].backtrackSolution(node)

        explored.add(node.state)

        for action in problem.getActionsFromState(node.state):
            child = node.childNode(problem, action)

            if child.state not in explored:
                solution = ProblemSolving[TState, TAction].depthFirstSearchRecursiveHelper(
                    problem, stopEvent, child, explored
                )
                if solution is not ProblemSolving.NO_SOLUTIONS:
                    return solution

        return ProblemSolving.NO_SOLUTIONS

    @staticmethod
    def depthFirstSearchRecursiveLimited(
        problem: Problem[TState, TAction], stopEvent: Event, limit: int
    ) -> SolutionType[TAction]:
        initialNode = ProblemNode[TState, TAction](
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        explored: set[TState] = set()
        return ProblemSolving[TState, TAction].depthFirstSearchRecursiveLimitedHelper(
            problem, stopEvent, initialNode, explored, limit
        )

    @staticmethod
    def depthFirstSearchRecursiveLimitedHelper(
        problem: Problem[TState, TAction],
        stopEvent: Event,
        node: ProblemNode[TState, TAction],
        explored: set[TState],
        limit: int,
    ) -> SolutionType[TAction]:
        if stopEvent.is_set():
            return ProblemSolving.CUTOFF

        if problem.isGoalAchieved(node.state):
            return ProblemSolving[TState, TAction].backtrackSolution(node)  # Abbiamo trovato la soluzione

        if limit == 0:
            return ProblemSolving.CUTOFF

        explored.add(node.state)  # Segniamo lo stato come visitato

        cutoff_occurred = False

        for action in problem.getActionsFromState(node.state):
            child = node.childNode(problem, action)

            if child.state not in explored:
                solution = ProblemSolving[TState, TAction].depthFirstSearchRecursiveLimitedHelper(
                    problem, stopEvent, child, explored, limit - 1
                )
                if solution is ProblemSolving.CUTOFF:
                    cutoff_occurred = True
                elif solution is not ProblemSolving.NO_SOLUTIONS:
                    return solution

        if cutoff_occurred:
            return ProblemSolving.CUTOFF

        # non ci sono soluzioni (nessun CUTOFF)
        return ProblemSolving.NO_SOLUTIONS

    @staticmethod
    def iterativeDeepeningSearch(problem: Problem[TState, TAction], stopEvent: Event) -> SolutionType[TAction]:
        limit = 1
        while True:
            if stopEvent.is_set():
                return ProblemSolving.CUTOFF

            solution = ProblemSolving[TState, TAction].depthFirstSearchRecursiveLimited(
                problem, stopEvent, limit
            )
            if solution is not ProblemSolving.CUTOFF:
                return solution
            limit += 1

    # Algoritmi di ricerca basati su un costo (best-first)

    @staticmethod
    def bestFirstSearch(
        problem: Problem[TState, TAction], stopEvent: Event, costFunction: CostFunctionType[TState, TAction]
    ) -> SolutionType[TAction]:
        node = ProblemNode[TState, TAction](
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        if problem.isGoalAchieved(node.state):
            return ProblemSolving[TState, TAction].backtrackSolution(node)

        fringe: list[ProblemNode[TState, TAction]] = []
        heappush(fringe, (costFunction(node), node))

        costMap: dict[TState, float] = {node.state: node}

        explored: set[TState] = set()

        while True:
            if stopEvent.is_set():
                return ProblemSolving.CUTOFF

            if len(fringe) == 0:
                return ProblemSolving.NO_SOLUTIONS

            node: ProblemNode[TState, TAction] = heappop(fringe)[1]
            # ignora se già esplorato (controllo anche qui perché non rimuovo dalla fringe)
            if node.state in explored:
                continue

            if problem.isGoalAchieved(node.state):
                return ProblemSolving[TState, TAction].backtrackSolution(node)

            explored.add(node.state)

            # per ogni azione possibile dallo stato corrente, la espande (cioè aggiunge alla frontiera)
            # se non già presente (oppure se il percorso trovato è meno costoso)
            for action in problem.getActionsFromState(node.state):
                child = node.childNode(problem, action)

                # ignora se già esplorato
                if child.state in explored:
                    continue

                currCost = costMap.get(child.state)
                nextCost = costFunction(child)
                if currCost is None or nextCost < currCost:
                    # aggiunge (o sostituisce) lo stato child.state con il nodo child nella frontiera
                    heappush(fringe, (nextCost, child))
                    costMap[child.state] = nextCost

    @staticmethod
    def uniformSearch(problem: Problem[TState, TAction], stopEvent: Event) -> SolutionType[TAction]:
        return ProblemSolving[TState, TAction].bestFirstSearch(problem, stopEvent, lambda node: node.pathCost)

    @staticmethod
    def greedySearch(problem: Problem[TState, TAction], stopEvent: Event) -> SolutionType[TAction]:
        return ProblemSolving[TState, TAction].bestFirstSearch(
            problem, stopEvent, lambda node: node.heuristicDist
        )

    @staticmethod
    def aStarSearch(problem: Problem[TState, TAction], stopEvent: Event) -> SolutionType[TAction]:
        return ProblemSolving[TState, TAction].bestFirstSearch(
            problem, stopEvent, lambda node: node.pathCost + node.heuristicDist
        )
