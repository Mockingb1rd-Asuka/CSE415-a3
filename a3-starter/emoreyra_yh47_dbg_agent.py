"""

"""

from backgState import *

W = 0; R = 1

def move(state, die1, die2):
    
    
    
def nextState(oldState, mov1, di1, mov2, di2):
    points = oldState.pointLists.copy()
    newState = bgstate(old = oldState)
    points[mov1-1].remove(oldState.whose_move)
    points[mov2-1].remove(oldState.whose_move)
    
    if (oldState.whose_move == W):
        points[mov1-1-di1].append(oldState.whose_move)
        points[mov2-1-di2].append(oldState.whose_move)
        newState.whose_move = R
    else:
        points[mov1-1+di1].append(oldState.whose_move)
        points[mov2-1+di2].append(oldState.whose_move)
        newState.whose_move = W
    
    newState.pointLists = points
    
    return newState
    
    
def canMove(state, mov, di):
    
    

def staticEval(state):
    