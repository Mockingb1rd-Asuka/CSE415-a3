"""

"""

from backgState import *

W = 0; R = 1
OUR_COLOR = W

def move(state, die1, die2):
    OUR_COLOR = state.whose_move
    
# Assumes move is valid
def nextState(oldState, mov, di):
    bar = oldState.bar.copy()
    points = oldState.pointLists.copy()
    newState = bgstate(old = oldState)
    points[mov-1].remove(oldState.whose_move)
    if (mov != 0):
        if (oldState.whose_move == W):
            points[mov-1-di].append(oldState.whose_move)
            newState.whose_move = R
        else:
            points[mov-1+di].append(oldState.whose_move)
            newState.whose_move = W
    else:
        bar.remove(oldState.whose_move)
    
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
    bar = state.bar
    points = state.pointLists
    rscore = 0
    wscore = 0
    for i, val in enumerate(points, 1):
        wscore += val.count(W) * (24 - i)
        rscore += val.count(r) * (i)
        
    rscore -= bar.count(R) * 20
    wscore -= bar.count(W) * 20
        
    if OUR_COLOR == W: rscore *= -1
    else: wscore *= -1
    
    return rscore + wscore
            