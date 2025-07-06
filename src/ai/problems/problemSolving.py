from collections import deque
from collections.abc import Callable
from heapq import heappop, heappush
from threading import Event
from typing import Optional

from ai.core.action import Action
from ai.core.agent import Agent
from ai.core.state import State
from ai.core.taskSolver import TaskSolver
from ai.problems.problem import Problem
from ai.problems.problemNode import ProblemNode

type SolutionType = Optional[tuple[Optional[list[Action]], float]]
type SearchAlgorithmType = Callable[[Problem], SolutionType]
type CostFunctionType = Callable[[ProblemNode], float]


class ProblemSolving(TaskSolver):
    CUTOFF = None
    NO_SOLUTIONS = (None, -1)

    stopEvent: Optional[Event] = None

    def __init__(self, agent: Agent, problem: Problem):
        super().__init__(problem)

        self.agent = agent
        self.problem = problem
        self.currenState = problem.initialState

    def simpleProblemSolvingAgent(
        self,
        search: SearchAlgorithmType,
        executeSolution: bool = False,
        print_problem: bool = False,
    ):
        # algoritmo generico di ricerca (BFS, DFS, ...), trova la soluzione, intesa come sequenza di azioni
        if print_problem:
            print(f"-------------------------- PROBLEMA --------------------------")
            print(self.problem)

        print("\nCerco una soluzione...")
        solution = search(self.problem)
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
            print(str(self.problem.environment))
            for action in actions:
                self.agent.executeAction(action, self.problem)
                self.currenState = self.problem.environment.currentState

    @staticmethod
    def backtrackSolution(node: ProblemNode) -> SolutionType:
        actions = deque()
        cost = node.pathCost
        curr = node
        while curr.parent is not None:
            actions.appendleft(curr.action)
            curr = curr.parent
        return (list[Action](actions), cost)

    @staticmethod
    def isEventSet():
        return ProblemSolving.stopEvent is not None and ProblemSolving.stopEvent.is_set()

    @staticmethod
    def breadthFirstSearch(problem: Problem) -> SolutionType:
        node = ProblemNode(
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        if problem.isGoalAchieved(node.state):
            return ProblemSolving.backtrackSolution(node)

        fringe: deque[ProblemNode] = deque()
        fringe.appendleft(node)

        explored: set = set()

        while True:
            if ProblemSolving.isEventSet():
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
    def depthFirstSearch(problem: Problem) -> SolutionType:
        node = ProblemNode(
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        if problem.isGoalAchieved(node.state):
            return ProblemSolving.backtrackSolution(node)

        fringe: deque[ProblemNode] = deque()
        fringe.append(node)

        explored: set[State] = set()

        while True:
            if ProblemSolving.isEventSet():
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
    def depthFirstSearchRecursive(problem: Problem) -> SolutionType:
        initialNode = ProblemNode(
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        explored: set[State] = set()
        return ProblemSolving.depthFirstSearchRecursiveHelper(problem, initialNode, explored)

    @staticmethod
    def depthFirstSearchRecursiveHelper(
        problem: Problem, node: ProblemNode, explored: set[State]
    ) -> SolutionType:
        if ProblemSolving.isEventSet():
            return ProblemSolving.CUTOFF

        if problem.isGoalAchieved(node.state):
            return ProblemSolving.backtrackSolution(node)

        explored.add(node.state)

        for action in problem.getActionsFromState(node.state):
            child = node.childNode(problem, action)

            if child.state not in explored:
                solution = ProblemSolving.depthFirstSearchRecursiveHelper(problem, child, explored)
                if solution is not ProblemSolving.NO_SOLUTIONS:
                    return solution

        return ProblemSolving.NO_SOLUTIONS

    @staticmethod
    def depthFirstSearchRecursiveLimited(problem: Problem, limit: int) -> SolutionType:
        initialNode = ProblemNode(
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        explored: set[State] = set()
        return ProblemSolving.depthFirstSearchRecursiveLimitedHelper(
            problem, initialNode, explored, limit
        )

    @staticmethod
    def depthFirstSearchRecursiveLimitedHelper(
        problem: Problem,
        node: ProblemNode,
        explored: set[State],
        limit: int,
    ) -> SolutionType:
        if ProblemSolving.isEventSet():
            return ProblemSolving.CUTOFF

        if problem.isGoalAchieved(node.state):
            return ProblemSolving.backtrackSolution(node)  # Abbiamo trovato la soluzione

        if limit == 0:
            return ProblemSolving.CUTOFF

        explored.add(node.state)  # Segniamo lo stato come visitato

        cutoff_occurred = False

        for action in problem.getActionsFromState(node.state):
            child = node.childNode(problem, action)

            if child.state not in explored:
                solution = ProblemSolving.depthFirstSearchRecursiveLimitedHelper(
                    problem, child, explored, limit - 1
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
    def iterativeDeepeningSearch(problem: Problem) -> SolutionType:
        limit = 1
        while True:
            if ProblemSolving.isEventSet():
                return ProblemSolving.CUTOFF

            solution = ProblemSolving.depthFirstSearchRecursiveLimited(problem, limit)
            if solution is not ProblemSolving.CUTOFF:
                return solution
            limit += 1

    # Algoritmi di ricerca basati su un costo (best-first)

    @staticmethod
    def bestFirstSearch(problem: Problem, costFunction: CostFunctionType) -> SolutionType:
        node = ProblemNode(
            parent=None,
            state=problem.initialState,
            action=None,
            pathCost=0,
            heuristicDist=problem.heuristicDistFunction(problem.initialState),
        )

        if problem.isGoalAchieved(node.state):
            return ProblemSolving.backtrackSolution(node)

        fringe: list[tuple[float, ProblemNode]] = []
        heappush(fringe, (costFunction(node), node))

        costMap: dict[State, float] = {node.state: node.pathCost}

        explored: set[State] = set()

        while True:
            if ProblemSolving.isEventSet():
                return ProblemSolving.CUTOFF

            if len(fringe) == 0:
                return ProblemSolving.NO_SOLUTIONS

            node: ProblemNode = heappop(fringe)[1]
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

                currCost = costMap.get(child.state)
                nextCost = costFunction(child)
                if currCost is None or nextCost < currCost:
                    # aggiunge (o sostituisce) lo stato child.state con il nodo child nella frontiera
                    heappush(fringe, (nextCost, child))
                    costMap[child.state] = nextCost

    @staticmethod
    def uniformSearch(problem: Problem) -> SolutionType:
        return ProblemSolving.bestFirstSearch(problem, lambda node: node.pathCost)

    @staticmethod
    def greedySearch(problem: Problem) -> SolutionType:
        return ProblemSolving.bestFirstSearch(problem, lambda node: node.heuristicDist)

    @staticmethod
    def aStarSearch(problem: Problem) -> SolutionType:
        return ProblemSolving.bestFirstSearch(
            problem, lambda node: node.pathCost + node.heuristicDist
        )
