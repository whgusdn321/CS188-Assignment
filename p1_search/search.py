# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
from util import*

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]




def depthFirstSearch(problem):
    """
        Search the deepest nodes in the search tree first.
        
        Your search algorithm needs to return a list of actions that reaches the
        goal. Make sure to implement a graph search algorithm.
        
        To get started, you might want to try some of these simple commands to
        understand the search problem that is being passed in:
        
        print "Start:", problem.getStartState()
        print "Is the start a goal?", problem.isGoalState(problem.getStartState())
        print "Start's successors:", problem.getSuccessors(problem.getStartState())
        """
    "*** YOUR CODE HERE ***"
    print "Start:", problem.getStartState()
    fringe = []
    closed_set = set()
    
    
    node = {
        'state': problem.getStartState(),
        'parent': None,
        'action': None
            }
    
    fringe.append(node)
    
    while len(fringe) != 0:
        node = fringe.pop()
        
        if node['state'] in closed_set:
            continue
        else:
            closed_set.add(node['state'])


        if not problem.isGoalState(node['state']) :
            for successor in problem.getSuccessors(node['state']):
                child_node = {
                    'state': successor[0],
                    'parent': node,
                    'action': successor[1]
                    }
                fringe.append(child_node)
        
        actions = []
        now_node = node
        while node['parent'] != None:
            print('asdfaaaa')
            actions.insert(0, node['action'])
            node = node['parent']


        if problem.isGoalState(now_node['state']):
            break
    return actions


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    fringe = []
    closed_set =set()
    answers = []
    
    node = {
        'state': problem.getStartState(),
        'parent': None,
        'action': None,
        'pathes': []
        }
    
    fringe.append(node)
    
    while len(fringe) != 0:
        node = fringe.pop(0)
        print(node['state'])
        
        
        if node['state'] in closed_set:
            '''
            print('[successor[1]] :',[successor[1]])
            node['pathes'] = node['pathes']+[successor[1]]
            '''
            continue
        else:
            closed_set.add(node['state'])
        
        """
        if problem.isGoalState(node['state']):
            actions = []
            now_node = node
            while node['parent'] != None:
                actions.insert(0, node['action'])
                node = node['parent']
            return actions
        """
        if problem.isGoalState(node['state']):
            print('goal!!!!!!!!!')
            print('pathes are :', node['pathes'])
            return node['pathes']
        if not problem.isGoalState(node['state']) :
            
            for successor in problem.getSuccessors(node['state']):
                child_node = {
                    'state': successor[0],
                    'parent': node,
                    'action': successor[1],
                    'pathes' : list(node['pathes']) + [successor[1]]
                }
                fringe.append(child_node)
                
    return node['pathes']
class PriorityQ:
    """
        Implements a priority queue data structure. Each inserted item
        has a priority associated with it and the client is usually interested
        in quick retrieval of the lowest-priority item in the queue. This
        data structure allows O(1) access to the lowest-priority item.
        """
    def  __init__(self):
        self.heap = []
        self.count = 0
    
    def push(self, item, priority, parent, action):
        entry = (priority, self.count, item, parent,  action)
        heapq.heappush(self.heap, entry)
        self.count += 1
    
    def pop(self):
        (priority,self.count,item, parent, action) = heapq.heappop(self.heap)
        return (priority,self.count,item, parent, action)
    
    def isEmpty(self):
        return len(self.heap) == 0
    
    def update(self, item, priority, parent,action):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (pr, co, it,pa,act) in enumerate(self.heap):
            if it == item:
                if pr<= priority:
                    break
                del self.heap[index]
                self.heap.append( (priority, co, item, pa, act))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority,parent,action)

def uniformCostSearch(problem):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = []
    closed_set = set()
    
    
    node = {
        'state': problem.getStartState(),
        'parent': None,
        'action': None,
        'cost_g' : 0
    }

    fringe.append(node)
    
    while len(fringe) != 0:
        index = 0
        temp_cost=fringe[0]['cost_g']
        for i in range(len(fringe)):
            if fringe[i]['cost_g'] < temp_cost:
                temp_cost = fringe[i]['cost_g']
                index = i
        node = fringe.pop(index)
        
        if node['state'] in closed_set:
            continue
        else:
            closed_set.add(node['state'])
        
        if problem.isGoalState(node['state']):
            actions = []
            now_node = node
            while node['parent'] != None:
                actions.insert(0, node['action'])
                node = node['parent']
            return actions
    
        if not problem.isGoalState(node['state']) :
            for successor in problem.getSuccessors(node['state']):
                child_node = {
                    'state': successor[0],
                    'parent': node,
                    'action': successor[1],
                    'cost_g': successor[2] +node['cost_g']
                }
                fringe.append(child_node)

    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = []
    closed_set = set()
    
    
    node = {
        'state': problem.getStartState(),
        'parent': None,
        'action': None,
        'cost_g' : 0,
        'cost_g+h' : 0
    }
    node['cost_g+h'] =heuristic(node['state'],problem)
    fringe.append(node)
    
    while len(fringe) != 0:
        index = 0
        temp_cost=fringe[0]['cost_g+h']
        for i in range(len(fringe)):
            if fringe[i]['cost_g+h'] < temp_cost:
                temp_cost = fringe[i]['cost_g+h']
                index = i
        node = fringe.pop(index)
        
        if node['state'] in closed_set:
            continue
        else:
            closed_set.add(node['state'])
        
        if problem.isGoalState(node['state']):
            actions = []
            now_node = node
            while node['parent'] != None:
                actions.insert(0, node['action'])
                node = node['parent']
            return actions
        
        if not problem.isGoalState(node['state']) :
            for successor in problem.getSuccessors(node['state']):
                child_node = {
                    'state': successor[0],
                    'parent': node,
                    'action': successor[1],
                    'cost_g': successor[2] +node['cost_g'] ,
                    'cost_g+h' : 0
                    }
                child_node['cost_g+h'] += child_node['cost_g']+heuristic(child_node['state'],problem)
                fringe.append(child_node)

    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
