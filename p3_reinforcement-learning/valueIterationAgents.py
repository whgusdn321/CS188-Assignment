# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()
        #print()
        #print()
        
        #print('mdp.getStates() : ' ,mdp.getStates())
        #print('mdp.getPossibleActions(state) : ',mdp.getPossibleActions(mdp.getStates()[1]))
        #print('mdp.getTransitionStatesAndProbs :', mdp.getTransitionStatesAndProbs( (0,1), 'west') )
        #print('mdp.getTransitionStatesAndProbs :', mdp.getTransitionStatesAndProbs( (0,0), 'exit') )
        #print('mdp.getReward :', mdp.getReward( (0,1), 'west', (0,0) ))
        #print('mdp.getReward :', mdp.getReward( (0,0), 'exit', 'TERMINAL_STATE' ))
        #print('mdp.isTerminal :',mdp.isTerminal( (0,1) ))
        #print('values are :',self.values)
        #print('getValue( (0,1) ):',getValue((0,1)))
        
    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        mdp = self.mdp
        discount = self.discount
        iterations = self.iterations
        values = self.values
        new_values = util.Counter()
        states = mdp.getStates()
        
        k = 0
        #print('iterations is :',iterations)
        '''
        if iteration == 0 :
            for state in states:
                values[state] = 0
            return
        '''
    
        while k <= iterations:
            #print('new iteration!')
            if k  == 0:
                for state in states:
                    values[state] = 0
            else :
                for state in states: #when 0<k<=iterations
                    qValues = []
                    #print('state is!! :',state)
                    #print('values is !!:',values)
                    for action in mdp.getPossibleActions(state):
                        sum = 0
                        for item in mdp.getTransitionStatesAndProbs( state, action): #'mdp.getTransitionStatesAndProbs :', [((0, 1), 1.0), ((0, 0), 0.0), ((0, 2), 0.0)]
                            resultState = item[0]
                            prob = item[1]
                            sum += prob * ( mdp.getReward( state, action, resultState) + discount*self.values[resultState] )
                        qValues.append(sum)

                    if not mdp.isTerminal(state):
                        new_values[state] = max(qValues)
                    else :
                        new_values[state] = 0
                #print('new_values are :',new_values)
                self.values = new_values.copy()
            k += 1
        return

                    
        
        
    


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        mdp = self.mdp
        discount = self.discount
        iterations = self.iterations
        values = self.values
        
        #states = mdp.getStates()
        #print('state is :', state)
        
        qValues = []
        
                
        sum = 0
                
        for item in mdp.getTransitionStatesAndProbs(state, action): #'mdp.getTransitionStatesAndProbs :', [((0, 1), 1.0), ((0, 0), 0.0), ((0, 2), 0.0)]
                resultState = item[0]
                prob = item[1]
                sum += prob * ( mdp.getReward( state, action, resultState) + discount*values[resultState] )

        return sum
        

    
    

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        mdp = self.mdp
        discount = self.discount
        iterations = self.iterations
        values = self.values
        
        states = mdp.getStates()
        
        #print('iterations is :',iterations)
        
        if mdp.isTerminal(state):
            return None
        
        qValues = []
        for action in mdp.getPossibleActions(state):
            sum = 0
                
            for item in mdp.getTransitionStatesAndProbs(state, action): #'mdp.getTransitionStatesAndProbs :', [((0, 1), 1.0), ((0, 0), 0.0), ((0, 2), 0.0)]
                resultState = item[0]
                prob = item[1]
                sum += prob * ( mdp.getReward( state, action, resultState) + discount * self.values[resultState] )
            qValues.append( [sum,action] )
        
        sums = [item[0] for item in qValues ]
        actions = [item[1] for item in qValues]
        max_index = 0
        for i in range(len(sums)):
            if sums[i]>sums[max_index]:
                max_index = i

        return actions[max_index]
        
        

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        statesList = self.mdp.getStates()
        #print('stateList is :',statesList)
        j = len(statesList)
        cnt = 0
        while cnt != self.iterations:
            if cnt == 0 :
                self.values[statesList[cnt%j]] = 0
            else:
                qValues = []
                if len(self.mdp.getPossibleActions(statesList[cnt%j])) == 0:
                    cnt += 1
                    continue
                for action in self.mdp.getPossibleActions(statesList[cnt%j]):
                    sum = 0
                    for item in self.mdp.getTransitionStatesAndProbs(statesList[cnt%j], action): #'mdp.getTransitionStatesAndProbs :', [((0, 1), 1.0), ((0, 0), 0.0), ((0, 2), 0.0)]
                        resultState = item[0]
                        prob = item[1]
                        sum += prob * ( self.mdp.getReward( statesList[cnt%j], action, resultState) + self.discount * self.values[resultState] )
                    qValues.append(sum)

                max_index = 0
                for i in range(len(qValues)):
                    if qValues[i]>qValues[max_index]:
                        max_index = i

                self.values[statesList[cnt%j]] = qValues[max_index]
            cnt += 1




class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

