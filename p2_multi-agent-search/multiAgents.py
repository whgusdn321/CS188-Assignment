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
from math import *
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
        print('legalMoves :', legalMoves)
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore] #Best can be many values, not only one.
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        
        "Add more of your code here if you want to"
        
        return legalMoves[chosenIndex]
    def manhattanDistance(a,b):
    
        ax,ay = a[0],a[1]
        bx,by = b[0],b[1]
    
        xDistance = abs(a[0]-b[0])
        yDistance = abs(a[1]-b[1])
    
        return xDistance + yDistance
    
    
    
    
    
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
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        
        action = action
        actionPoints = 0
        if action == 'Stop':
            actionPoints = -1
        
        '''
        print('action : ',action)
        print('successorGameState.getscore() :', successorGameState.getScore())
        print('newPos = ',newPos)
        
        print('newGhostposition :',newGhostStates[0].getPosition())
        print('newScaredTimes :',newScaredTimes)
        '''
        "*** YOUR CODE HERE ***"
        ghostDistance = []
        for item in newGhostStates:
            print('%d items in states',len(newGhostStates))
            ghostDistance.append( manhattanDistance(newPos, item.getPosition()) ) #Calclate ghostDistance and add them. If there is only one ghost, only one item in ghostDistance array .
        leftedFoodNum = len(newFood)
        closestFoodDis = 0
        if len(newFood) != 0:
            closestFoodDis = manhattanDistance(newPos,newFood[0])
            for item in newFood :
                if manhattanDistance(newPos, item) < closestFoodDis:
                    closestFoodDis = manhattanDistance(newPos, item)
        print('ghostDistance', ghostDistance[0])
        print('closestFoodDis = %d'%closestFoodDis)
        print()
        scaredTime = newScaredTimes
        return successorGameState.getScore() + ghostDistance[0] - closestFoodDis +scaredTime[0] + actionPoints
        #return successorGameState.getScore() + 10/(0.98-ghostDistance[0]) - closestFoodDis +scaredTime[0] + actionPoints

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





class MinimaxAgent(MultiAgentSearchAgent):
    
    def getAction(self, gameState):
        
        def max_value(state,nowDepth,nowAgent, totalAgents ):
            
            v = -99999
            for action in state.getLegalActions(nowAgent):
                successorState = state.generateSuccessor(nowAgent,action)
                v = max(v, value(successorState,nowDepth,nowAgent, totalAgents))
            return v
    
        def min_value(state,nowDepth,nowAgent, totalAgents):
            v = 99999
            for action in state.getLegalActions(nowAgent):
                successorState = state.generateSuccessor(nowAgent,action)
                v = min(v, value(successorState,nowDepth,nowAgent, totalAgents))
            return v
        
        
        def value( state, nowDepth,nowAgent,totalAgents):
            #print('state is', state)
            
            #print('Evaluation0 is :', self.evaluationFunction(state) )
            nowAgent += 1 #increase to determine Max or min
            print('!!nowAgent is!!',nowAgent)
            print('!!TotalAgent is!!',totalAgents)
            if nowAgent < totalAgents:
                if len(state.getLegalActions(nowAgent)) == 0:
                    #print('Evaluation1 is :', self.evaluationFunction(state) )
                    return self.evaluationFunction(state)
            if nowAgent >= totalAgents: #New depth!
                nowDepth += 1
                nowAgent = 0
                if len(state.getLegalActions(nowAgent)) == 0: #If the max node is terminal node.
                    #print('Evaluation2 is :', self.evaluationFunction(state) )
                    return self.evaluationFunction(state)
                print('nowDepth is', nowDepth)
                if nowDepth == self.depth:
                    print('Sibal')
                    print('state is', state)
                    #print('Evaluation3 is :', self.evaluationFunction(state) )
                    return self.evaluationFunction(state)
                else:
                    return max_value(state,nowDepth,nowAgent,totalAgents)
            else: #Same depth, so min_value() should be called.
                return min_value(state,nowDepth,nowAgent,totalAgents)
            
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
        """
        "*** YOUR CODE HERE ***"
        
        print('gameState.getNumAgents(): ',gameState.getNumAgents()) #the number of Agents are 3!
        #print('self.evaluationFunction!!!! :',self.evaluationFunction(gameState))
        print('gameState.getLegalActions :', gameState.getLegalActions(0))
        print('depth :',self.depth)
        agents = gameState.getNumAgents()
        
        kk = ''
        v = -99999
        for item in gameState.getLegalActions(0):
            successorState = gameState.generateSuccessor(0,item)
            print('successorState is :', successorState)
            print('action is ', item)
            #print('self.evaluationFunction :',self.evaluationFunction(successorState))
            k = value(successorState,0,0,agents)
            if k > v:
                v = k
                kk = item
            

#v = max(v, value(successorState,0,0,agents) )
        print('Its over!')
        print('selected movement :',kk)


        return kk


                                            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(state,nowDepth,nowAgent, totalAgents,alpha,betha ):
            v = -999999
            for action in state.getLegalActions(nowAgent):
                successorState = state.generateSuccessor(nowAgent,action)
                t = value(successorState,nowDepth,nowAgent,totalAgents,alpha,betha)
                v = max(v, t)
                if v> betha:
                    return v
                alpha = max(alpha,v)
            return v
        
        def min_value(state,nowDepth,nowAgent, totalAgents,alpha,betha):
            v = 999999
            for action in state.getLegalActions(nowAgent):
                successorState = state.generateSuccessor(nowAgent,action)
                t = value(successorState,nowDepth,nowAgent,totalAgents,alpha,betha)
                print('t is :',t)
                v = min(v, t)
                if v< alpha:
                    return v
                betha = min(betha,v)
            return v
        
        
        def value( state, nowDepth,nowAgent,totalAgents,alpha,betha):
            
            
            
            nowAgent += 1 #increase to determine Max or min
            print('!!nowAgent is!!',nowAgent)
            if nowAgent < totalAgents: # if there is no child anymore, in case of min node,
                if len(state.getLegalActions(nowAgent)) == 0:
                    return self.evaluationFunction(state)
            if nowAgent >= totalAgents: #New depth! this means max node!
                nowDepth += 1
                nowAgent = 0
                if len(state.getLegalActions(nowAgent)) == 0: #If the max node dosen't have a child node.
                    return self.evaluationFunction(state)
                if nowDepth == self.depth: #If the max node exceed the search level
                    return self.evaluationFunction(state)
                else:
                    return max_value(state,nowDepth,nowAgent,totalAgents,alpha,betha) # If the max node within search level
            else: #Same depth, so min_value() should be called.
                return min_value(state,nowDepth,nowAgent,totalAgents,alpha,betha)


        
        print('gameState.getNumAgents(): ',gameState.getNumAgents()) #the number of Agents are 3!
        print('gameState.getLegalActions :', gameState.getLegalActions(0))
        print('depth :',self.depth)
        agents = gameState.getNumAgents()
            
        kk = ''
        v = -999999
        alpha, betha= -999999,999999
        for item in gameState.getLegalActions(0):
            successorState = gameState.generateSuccessor(0,item)
            print('successorState is :', successorState)
            print('action is ', item)
            #print('self.evaluationFunction :',self.evaluationFunction(successorState))
            t = value(successorState,0,0,agents,alpha,betha)
            if t > v:
                v = t
                kk = item
            if v> betha:
                return v
            alpha = max(alpha,v)
        
        
        print('Its over!')
        print('selected movement :',kk)


        return kk


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
        def max_value(state,nowDepth,nowAgent, totalAgents ):
            
            v = -99999
            for action in state.getLegalActions(nowAgent):
                successorState = state.generateSuccessor(nowAgent,action)
                v = max(v, value(successorState,nowDepth,nowAgent, totalAgents))
            return v
        
        def min_value(state,nowDepth,nowAgent, totalAgents):
            v = 0
            count = 0
            for action in state.getLegalActions(nowAgent):
                successorState = state.generateSuccessor(nowAgent,action)
                v += value(successorState,nowDepth,nowAgent, totalAgents)
                count += 1
            return float(v)/count
        
        
        def value( state, nowDepth,nowAgent,totalAgents):
            nowAgent += 1 #increase to determine Max or min
            print('!!nowAgent is!!',nowAgent)
            print('!!TotalAgent is!!',totalAgents)
            if nowAgent < totalAgents:
                if len(state.getLegalActions(nowAgent)) == 0:
                    #print('Evaluation1 is :', self.evaluationFunction(state) )
                    return self.evaluationFunction(state)
            if nowAgent >= totalAgents: #New depth!
                nowDepth += 1
                nowAgent = 0
                if len(state.getLegalActions(nowAgent)) == 0: #If the max node is terminal node.
                    #print('Evaluation2 is :', self.evaluationFunction(state) )
                    return self.evaluationFunction(state)
                print('nowDepth is', nowDepth)
                if nowDepth == self.depth:
                    print('Sibal')
                    print('state is', state)
                    #print('Evaluation3 is :', self.evaluationFunction(state) )
                    return self.evaluationFunction(state)
                else:
                    return max_value(state,nowDepth,nowAgent,totalAgents)
            else: #Same depth, so min_value() should be called.
                return min_value(state,nowDepth,nowAgent,totalAgents)


        
        print('gameState.getNumAgents(): ',gameState.getNumAgents()) #the number of Agents are 3!
        #print('self.evaluationFunction!!!! :',self.evaluationFunction(gameState))
        print('gameState.getLegalActions :', gameState.getLegalActions(0))
        print('depth :',self.depth)
        agents = gameState.getNumAgents()
        
        kk = ''
        v = -99999
        for item in gameState.getLegalActions(0):
            successorState = gameState.generateSuccessor(0,item)
            print('successorState is :', successorState)
            print('action is ', item)
            #print('self.evaluationFunction :',self.evaluationFunction(successorState))
            k = value(successorState,0,0,agents)
            print('k is :',k)
            if k > v:
                v = k
                kk = item
        return kk

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

