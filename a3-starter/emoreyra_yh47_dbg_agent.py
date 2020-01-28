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
    
    
def canMove(state, move, die):
    currentState = state.pointLists
    destination = move + die
    return isOpen(currentState, destination)

def isOpen(state, location):
    destination = state.pointLists[location]
    if state.whose_move == W:
        return destination[0] != R or len(destination) < 2
    else:
        return destination[0] != W or len(destination) < 2


def staticEval(state):
    