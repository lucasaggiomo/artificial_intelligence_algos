from .action import Action
from .perception import Perception
from .state import State
from .agent import Agent
from .goal import Goal
from .problem import Problem

from .node import Node

from .customTypes import SolutionType

type SearchAlgorithmType = Callable[[Problem, Event], SolutionType]

from collections import deque
from collections.abc import Callable

from heapq import *

from threading import Event


class ProblemSolving:
    CUTOFF = None
    NO_SOLUTIONS = [None, -1]

    def __init__(self, agent: Agent, problem: Problem):
        self.agent = agent
        self.problem = problem
        self.currentState = problem.initialState

    def simpleProblemSolvingAgent(
        self,
        search: SearchAlgorithmType,
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
            print(
                "Nessuna soluzione trovata, ma non è stato visitato tutto l'albero degli stati"
            )
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
            self.agent.environment.render()
            for action in actions:
                self.agent.executeAction(action)

    @staticmethod
    def backtrackSolution(node: Node) -> SolutionType:
        actions = deque()
        cost = node.pathCost
        curr = node
        while curr.parent is not None:
            actions.appendleft(curr.action)
            curr = curr.parent
        return (list(actions), cost)

    @staticmethod
    def breadthFirstSearch(problem: Problem, stopEvent: Event) -> SolutionType:
        node = Node(
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        if problem.isGoalAchieved(node.state):
            return ProblemSolving.backtrackSolution(node)

        fringe: deque[Node] = deque()
        fringe.appendleft(node)

        explored: set[State] = set()

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
                        return ProblemSolving.backtrackSolution(child)
                    fringe.appendleft(child)

    @staticmethod
    def depthFirstSearch(problem: Problem, stopEvent: Event) -> SolutionType:
        node = Node(
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        if problem.isGoalAchieved(node.state):
            return ProblemSolving.backtrackSolution(node)

        fringe: deque[Node] = deque()
        fringe.append(node)

        explored: set[State] = set()

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
                        return ProblemSolving.backtrackSolution(child)
                    fringe.append(child)

    @staticmethod
    def depthFirstSearchRecursive(problem: Problem, stopEvent: Event) -> SolutionType:
        initialNode = Node(
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        explored: set[State] = set()
        return ProblemSolving.depthFirstSearchRecursiveHelper(
            problem, stopEvent, initialNode, explored
        )

    @staticmethod
    def depthFirstSearchRecursiveHelper(
        problem: Problem, stopEvent: Event, node: Node, explored: set
    ) -> SolutionType:
        if stopEvent.is_set():
            return ProblemSolving.CUTOFF

        if problem.isGoalAchieved(node.state):
            return ProblemSolving.backtrackSolution(node)

        explored.add(node.state)

        for action in problem.getActionsFromState(node.state):
            child = node.childNode(problem, action)

            if child.state not in explored:
                solution = ProblemSolving.depthFirstSearchRecursiveHelper(
                    problem, stopEvent, child, explored
                )
                if solution is not ProblemSolving.NO_SOLUTIONS:
                    return solution

        return ProblemSolving.NO_SOLUTIONS

    @staticmethod
    def depthFirstSearchRecursiveLimited(
        problem: Problem, stopEvent: Event, limit: int
    ) -> SolutionType:
        initialNode = Node(
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        explored: set[State] = set()
        return ProblemSolving.depthFirstSearchRecursiveLimitedHelper(
            problem, stopEvent, initialNode, explored, limit
        )

    @staticmethod
    def depthFirstSearchRecursiveLimitedHelper(
        problem: Problem, stopEvent: Event, node: Node, explored: set, limit: int
    ) -> SolutionType:
        if stopEvent.is_set():
            return ProblemSolving.CUTOFF

        if problem.isGoalAchieved(node.state):
            return ProblemSolving.backtrackSolution(
                node
            )  # Abbiamo trovato la soluzione

        if limit == 0:
            return ProblemSolving.CUTOFF

        explored.add(node.state)  # Segniamo lo stato come visitato

        cutoff_occurred = False

        for action in problem.getActionsFromState(node.state):
            child = node.childNode(problem, action)

            if child.state not in explored:
                solution = ProblemSolving.depthFirstSearchRecursiveLimitedHelper(
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
    def iterativeDeepeningSearch(problem: Problem, stopEvent: Event) -> SolutionType:
        limit = 1
        while True:
            if stopEvent.is_set():
                return ProblemSolving.CUTOFF

            solution = ProblemSolving.depthFirstSearchRecursiveLimited(
                problem, stopEvent, limit
            )
            if solution is not ProblemSolving.CUTOFF:
                return solution
            limit += 1

    # Algoritmi di ricerca basati su un costo (best-first)

    @staticmethod
    def bestFirstSearch(
        problem: Problem, stopEvent: Event, costFunction: Callable[[Node], int]
    ) -> SolutionType:
        node = Node(
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        if problem.isGoalAchieved(node.state):
            return ProblemSolving.backtrackSolution(node)

        fringe: list[Node] = []
        heappush(fringe, (costFunction(node), node))

        fringeNodeMap: dict[State, Node] = {
            node.state: node
        }  # bruttissimo ma non ho altre idee

        explored: set[State] = set()

        while True:
            if stopEvent.is_set():
                return ProblemSolving.CUTOFF

            if len(fringe) == 0:
                return ProblemSolving.NO_SOLUTIONS

            node: Node = heappop(fringe)[1]
            # ignora se già esplorato (controllo anche qui perché non rimuovo dalla fringe)
            if node.state in explored:
                continue

            if problem.isGoalAchieved(node.state):
                return ProblemSolving.backtrackSolution(node)

            explored.add(node.state)

            # per ogni azione possibile dallo stato corrente, la espande (cioè aggiunge alla frontiera)
            # se non già presente (oppure se il percorso trovato è meno costoso)
            for action in problem.getActionsFromState(node.state):
                child = node.childNode(problem, action)

                # ignora se già esplorato
                if child.state in explored:
                    continue

                oldNode = fringeNodeMap.get(child.state)
                if oldNode is None or child.pathCost < oldNode.pathCost:
                    # aggiunge (o sostituisce) lo stato child.state con il nodo child nella frontiera
                    heappush(fringe, (costFunction(child), child))
                    fringeNodeMap[child.state] = child

    @staticmethod
    def uniformSearch(problem: Problem, stopEvent: Event) -> SolutionType:
        return ProblemSolving.bestFirstSearch(
            problem, stopEvent, lambda node: node.pathCost
        )

    @staticmethod
    def greedySearch(problem: Problem, stopEvent: Event) -> SolutionType:
        return ProblemSolving.bestFirstSearch(
            problem, stopEvent, lambda node: node.heuristicDist
        )

    @staticmethod
    def aStarSearch(problem: Problem, stopEvent: Event) -> SolutionType:
        return ProblemSolving.bestFirstSearch(
            problem, stopEvent, lambda node: node.pathCost + node.heuristicDist
        )
