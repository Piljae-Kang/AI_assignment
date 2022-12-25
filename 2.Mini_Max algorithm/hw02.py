from shutil import move
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

## Example Agent
class ReflexAgent(Agent):

  def Action(self, gameState):

    move_candidate = gameState.getLegalActions()

    scores = [self.reflex_agent_evaluationFunc(gameState, action) for action in move_candidate]
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)

    return move_candidate[get_index]

  def reflex_agent_evaluationFunc(self, currentGameState, action):

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()



def scoreEvalFunc(currentGameState):

  return currentGameState.getScore()

class AdversialSearchAgent(Agent):

  def __init__(self, getFunc ='scoreEvalFunc', depth ='2'):
    self.index = 0
    self.evaluationFunction = util.lookup(getFunc, globals())

    self.depth = int(depth)

  def isTerminal(self, gameState, depth): #하위 클래스에 터미널 체크하는 함수 만들어서 사용
    if depth == self.depth:
      return True
    if gameState.isWin():
      return True
    if gameState.isLose():
      return True

    return False



class MinimaxAgent(AdversialSearchAgent):
  """    [문제 01] MiniMaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  
  def Action(self, gameState):
    ####################### Write Your Code Here ################################

    v, move = self.MaxValue(gameState, 0)

    return move


  def MaxValue(self, gameState, depth):            
      if self.isTerminal(gameState, depth):                
        return self.evaluationFunction(gameState), None

      move = None        
      v = float("-inf")            
           
      for a in gameState.getLegalActions():                
        v2, a2 = self.MinValue(gameState.generateSuccessor(0, a), depth, 1)

        if v2 > v:
          v = v2
          move = a       
      return v, move
    
  
  def MinValue(self, gameState, depth, num_ghost):            
      if self.isTerminal(gameState, depth):               
        return self.evaluationFunction(gameState), None           
      v = float("inf")
      move = None         
  
      if num_ghost == gameState.getNumAgents()-1:                
        for a in gameState.getLegalActions(num_ghost):                    
          v2, a2 = self.MaxValue(gameState.generateSuccessor(num_ghost, a), depth+1)

          if v2 < v:
            v = v2
            move = a
      else:                
        for a in gameState.getLegalActions(num_ghost):                    
          v2, a2 = self.MinValue(gameState.generateSuccessor(num_ghost, a), depth, num_ghost+1)

          if v2 < v:
            v = v2
            move = a

      return v, move

    ############################################################################

class AlphaBetaAgent(AdversialSearchAgent):
  """
    [문제 02] AlphaBetaAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################

    inf = float("inf") 

    v, move = self.MaxValue(gameState, 0, -inf, inf)

    return move


  def MaxValue(self, gameState, depth, alpha, beta):            
      if self.isTerminal(gameState, depth):                 
        return self.evaluationFunction(gameState), None

      move = None        
      v = float("-inf")            
           
      for a in gameState.getLegalActions():                
        v2, a2 = self.MinValue(gameState.generateSuccessor(0, a), depth, 1, alpha, beta)

        if v2 > v:
          v = v2
          move = a
          alpha = max(alpha, v)

        if v >= beta:
          return v, move

      return v, move
    
  
  def MinValue(self, gameState, depth, num_ghost, alpha, beta):
      if self.isTerminal(gameState, depth):                
        return self.evaluationFunction(gameState), None

             
      v = float("inf")
      move = None         
  
      if num_ghost == gameState.getNumAgents()-1:                
        for a in gameState.getLegalActions(num_ghost):                    
          v2, a2 = self.MaxValue(gameState.generateSuccessor(num_ghost, a), depth+1, alpha, beta)

          if v2 < v:
            v = v2
            move = a
      else:                
        for a in gameState.getLegalActions(num_ghost):                    
          v2, a2 = self.MinValue(gameState.generateSuccessor(num_ghost, a), depth, num_ghost+1, alpha, beta)

          if v2 < v:
            v = v2
            move = a
            beta = min(beta, v)
          
          if v <= alpha:
            return v, move

      return v, move

    ############################################################################



class ExpectimaxAgent(AdversialSearchAgent):
  """
    [문제 03] ExpectimaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################

    v, move = self.MaxValue(gameState, 0)

    return move


  def MaxValue(self, gameState, depth):            
      if self.isTerminal(gameState, depth):                
        return self.evaluationFunction(gameState), None

      move = None        
      v = float("-inf")            
           
      for a in gameState.getLegalActions():                
        v2, a2 = self.MinValue(gameState.generateSuccessor(0, a), depth, 1)

        if v2 > v:
          v = v2
          move = a

      return v, move
    
  
  def MinValue(self, gameState, depth, num_ghost):            
      if self.isTerminal(gameState, depth):                
        return self.evaluationFunction(gameState), None

      move = None
      total_v = 0
      total_node = len(gameState.getLegalActions(num_ghost))
  
      if num_ghost == gameState.getNumAgents()-1:                
        for a in gameState.getLegalActions(num_ghost):                    
          v2, a2 = self.MaxValue(gameState.generateSuccessor(num_ghost, a), depth+1)
          total_v += v2

      else:                
        for a in gameState.getLegalActions(num_ghost):                    
          v2, a2 = self.MinValue(gameState.generateSuccessor(num_ghost, a), depth, num_ghost+1)
          total_v += v2

      return total_v/total_node, move # min에서는 각 노드 들의 min값의 value가 아니라 기댓값을 전해준다.

    ############################################################################
