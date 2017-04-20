# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        from search import bfs
        from searchAgents import PositionSearchProblem, mazeDistance
        "*** YOUR CODE HERE ***"

        nearestGhostDistance = 1000
        for ghostState in newGhostStates:
            if ghostState.scaredTimer == 0:
                nearestGhostDistance = min(nearestGhostDistance, mazeDistance(ghostState.configuration.pos, newPos, successorGameState))

        nearestFoodDistance = 1000
        for foodPos in newFood.asList():
            #nearestFoodDistance = min(nearestFoodDistance, mazeDistance(foodPos, newPos, successorGameState))
            nearestFoodDistance = min(nearestFoodDistance, manhattanDistance(foodPos, newPos))
        return successorGameState.getScore() - 5.0 / (nearestGhostDistance + 1.0) - nearestFoodDistance / 2.0

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class ScoreAction:
    def __init__(self, score, action):
        self.score = score
        self.action = action

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """

        return self.minimaxSearch(gameState, agentIndex = 0, depth = self.depth).action

    def minimaxSearch(self, gameState, agentIndex, depth):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return ScoreAction(self.evaluationFunction(gameState), Directions.STOP)
        else:
            if self.firstAgent(agentIndex):
                return self.findmax(gameState, agentIndex, depth)
            else:
                return self.findmin(gameState, agentIndex, depth)

    def findmax(self, gameState, agentIndex, depth):
            legalActions = gameState.getLegalActions(agentIndex)
            successorGameStates = [gameState.generateSuccessor(agentIndex, legalAction) for legalAction in legalActions]
            if self.lastAgent(gameState, agentIndex):
                nextAgent, nextdepth = 0, depth - 1
            else:
                nextAgent, nextdepth = agentIndex + 1, depth
            score, action = float('-inf'), Directions.STOP
            for legalAction in gameState.getLegalActions(agentIndex):
                successorGameState = gameState.generateSuccessor(agentIndex, legalAction)
                new_score = self.minimaxSearch(successorGameState, nextAgent, nextdepth).score
                if new_score > score:
                    score, action = new_score, legalAction
            return ScoreAction(score, action)

    def findmin(self, gameState, agentIndex, depth):
            legalActions = gameState.getLegalActions(agentIndex)
            successorGameStates = [gameState.generateSuccessor(agentIndex, legalAction) for legalAction in legalActions]
            if self.lastAgent(gameState, agentIndex):
                nextAgent, nextdepth = 0, depth - 1
            else:
                nextAgent, nextdepth = agentIndex + 1, depth
            score, action = float('inf'), Directions.STOP
            for legalAction in gameState.getLegalActions(agentIndex):
                successorGameState = gameState.generateSuccessor(agentIndex, legalAction)
                new_score = self.minimaxSearch(successorGameState, nextAgent, nextdepth).score
                if new_score < score:
                    score, action = new_score, legalAction
            return ScoreAction(score, action)

    def lastAgent(self, gameState, agentIndex):
        return agentIndex == gameState.getNumAgents() - 1

    def firstAgent(self, agentIndex):
        return agentIndex == 0

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minimaxSearchAlphaBeta(gameState, agentIndex = 0, depth = self.depth).action

    def minimaxSearchAlphaBeta(self, gameState, agentIndex, depth, alpha = float('-inf'), beta = float('inf')):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return ScoreAction(self.evaluationFunction(gameState), Directions.STOP)
        else:
            if self.firstAgent(agentIndex):
                return self.findmax(gameState, agentIndex, depth, alpha, beta)
            else:
                return self.findmin(gameState, agentIndex, depth, alpha, beta)

    def findmax(self, gameState, agentIndex, depth, alpha, beta):
            legalActions = gameState.getLegalActions(agentIndex)
            if self.lastAgent(gameState, agentIndex):
                nextAgent, nextdepth = 0, depth - 1
            else:
                nextAgent, nextdepth = agentIndex + 1, depth
            score, action = float('-inf'), Directions.STOP
            for legalAction in gameState.getLegalActions(agentIndex):
                successorGameState = gameState.generateSuccessor(agentIndex, legalAction)
                newScoreAction = self.minimaxSearchAlphaBeta(successorGameState, nextAgent, nextdepth, alpha, beta)
                if newScoreAction.score > score:
                    score, action = newScoreAction.score, legalAction
                if newScoreAction.score > beta:
                    return newScoreAction
                alpha = max(alpha, newScoreAction.score)
            return ScoreAction(score, action)

    def findmin(self, gameState, agentIndex, depth, alpha, beta):
            legalActions = gameState.getLegalActions(agentIndex)
            if self.lastAgent(gameState, agentIndex):
                nextAgent, nextdepth = 0, depth - 1
            else:
                nextAgent, nextdepth = agentIndex + 1, depth
            score, action = float('inf'), Directions.STOP
            for legalAction in gameState.getLegalActions(agentIndex):
                successorGameState = gameState.generateSuccessor(agentIndex, legalAction)
                newScoreAction = self.minimaxSearchAlphaBeta(successorGameState, nextAgent, nextdepth, alpha, beta)
                if newScoreAction.score < score:
                    score, action = newScoreAction.score, legalAction
                if newScoreAction.score < alpha:
                    return newScoreAction
                beta = min(beta, newScoreAction.score)
            return ScoreAction(score, action)

    def lastAgent(self, gameState, agentIndex):
        return agentIndex == gameState.getNumAgents() - 1

    def firstAgent(self, agentIndex):
        return agentIndex == 0



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimaxSearch(gameState, agentIndex = 0, depth = self.depth).action

    def expectimaxSearch(self, gameState, agentIndex, depth):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            score = self.evaluationFunction(gameState)
            return ScoreAction(self.evaluationFunction(gameState), Directions.STOP)
        else:
            if self.firstAgent(agentIndex):
                #print(self.findmax(gameState, agentIndex, depth).score, self.findmax(gameState, agentIndex, depth).action)
                return self.findmax(gameState, agentIndex, depth)
            else:
                #print(self.findexpect(gameState, agentIndex, depth).score, self.findexpect(gameState, agentIndex, depth).action)
                return self.findexpect(gameState, agentIndex, depth)

    def findmax(self, gameState, agentIndex, depth):
            legalActions = gameState.getLegalActions(agentIndex)
            successorGameStates = [gameState.generateSuccessor(agentIndex, legalAction) for legalAction in legalActions]
            if self.lastAgent(gameState, agentIndex):
                nextAgent, nextdepth = 0, depth - 1
            else:
                nextAgent, nextdepth = agentIndex + 1, depth
            scores = [self.expectimaxSearch(successorGameState, nextAgent, nextdepth).score for successorGameState in successorGameStates]
            #print(len(scores), 'max')
            bestScore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            chosenIndex = random.choice(bestIndices)
            return ScoreAction(bestScore, legalActions[chosenIndex])

    def findexpect(self, gameState, agentIndex, depth):
            legalActions = gameState.getLegalActions(agentIndex)
            successorGameStates = [gameState.generateSuccessor(agentIndex, legalAction) for legalAction in legalActions]
            if self.lastAgent(gameState, agentIndex):
                nextAgent, nextdepth = 0, depth - 1
            else:
                nextAgent, nextdepth = agentIndex + 1, depth
            scores = [self.expectimaxSearch(successorGameState, nextAgent, nextdepth).score for successorGameState in successorGameStates]
            #print(scores, 'expect')
            #print(len(scores), 'expect')
            averageScore = sum(scores) / float(len(scores))
            return ScoreAction(averageScore, Directions.STOP)

    def lastAgent(self, gameState, agentIndex):
        return agentIndex == gameState.getNumAgents() - 1

    def firstAgent(self, agentIndex):
        return agentIndex == 0

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: There are four components contributing to the evaulation result.
      current score, left food and position, ghost position, capsule postion

    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


    from search import bfs
    from searchAgents import PositionSearchProblem, mazeDistance
    "*** YOUR CODE HERE ***"


    nearestGhostDistance = 1000
    for ghostState in newGhostStates:
        if ghostState.scaredTimer == 0:
            nearestGhostDistance = min(nearestGhostDistance, mazeDistance(ghostState.configuration.pos, newPos, currentGameState))
    nearestFoodDistance = 1000
    averageDistance = 0.0

    for foodPos in newFood.asList():
        size = len(newFood.asList())
        if size < 3:
            distance = mazeDistance(foodPos, newPos, currentGameState)
        else:
            distance = manhattanDistance(foodPos, newPos)
        averageDistance += distance
        nearestFoodDistance = min(nearestFoodDistance, distance)
    averageDistance = averageDistance / float(len(newFood.asList()) + 0.1)
    score_factor = currentGameState.getScore()
    food_factor = -(0.9 * nearestFoodDistance + 0.1 * averageDistance) / 2.0 - len(newFood.asList())
    ghost_factor =  -5.0 / (nearestGhostDistance + 1.0)
    capsule_factor = - 50.0 * len(currentGameState.getCapsules()) + 0.1* sum(newScaredTimes)

    return score_factor + food_factor + ghost_factor + capsule_factor

# Abbreviation
better = betterEvaluationFunction
