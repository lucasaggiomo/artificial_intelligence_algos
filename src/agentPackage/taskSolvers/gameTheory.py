from src.agentPackage.taskSolvers.taskSolver import TaskSolver
from src.agentPackage.tasks.game import Game
from src.agentPackage.tasks.problem import Problem
from src.agentPackage.nodes.gameNode import GameNode
from src.agentPackage.state import State
from src.agentPackage.agent import Agent
from src.agentPackage.player import Player
from src.agentPackage.action import Action


class GameTheory(TaskSolver[Game]):
    # solo un agente for now bro
    def __init__(self, agent: Agent, player: Player, game: Game):
        super().__init__([agent, player], game)
        self.agent = agent
        self.player = player
        self.game = game
        self.currentState = game.initialState

    def startGame(self):
        print(f"Volevo essere un duro")

        while True:
            # let agent choose
            agentAction = GameTheory.minimaxDecision(self.game)
            if agentAction is None:
                raise ValueError("agentAction was None")

            # let agent execute action
            self.currentState = self.agent.executeAction(agentAction)

            if self.game.terminalTest(self.currentState):
                print("Game over")
                self.agent.environment.render()
                return

            # let player choose
            # playerAction = self.

    @staticmethod
    def minimaxDecision(game: Game) -> Action:
        maxUtilityAction = None
        maxUtility = float("-inf")
        for action in game.getActionsFromState(game.initialState):
            state = game.getNextState(game.initialState, action)
            currUtility = GameTheory.minValue(game, state)
            if currUtility > maxUtility:
                maxUtility = currUtility
                maxUtilityAction = action

        return maxUtilityAction

    @staticmethod
    def maxValue(game: Game, state: State) -> float:
        if game.terminalTest(state):
            return game.utilityFunction(state)

        maxUtility = float("-inf")
        # per ogni stato possibile raggiungibile, restituisce l'utilità maggiore
        for action in game.getActionsFromState(state):
            nextState = game.getNextState(state, action)
            currUtility = GameTheory.minValue(game, nextState)
            maxUtility = max(maxUtility, currUtility)

        return maxUtility

    @staticmethod
    def minUtility(game: Game, state: State) -> float:
        if game.terminalTest(state):
            return game.utilityFunction(state)

        minUtility = float("-inf")
        # per ogni stato possibile raggiungibile, restituisce l'utilità maggiore
        for action in game.getActionsFromState(state):
            nextState = game.getNextState(state, action)
            currUtility = GameTheory.maxValue(game, nextState)
            minUtility = min(minUtility, currUtility)

        return minUtility
