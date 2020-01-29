"""

"""

from backgState import *

W = 0; R = 1
OUR_COLOR = W

def move(state, die1, die2):
    OUR_COLOR = state.whose_move
    
def nextState(oldState, mov, di):
    # Assumes move is valid
    if (mov in ["P", "p"]): return bgstate(old = oldState)
    bar = oldState.bar.copy()
    points = oldState.pointLists.copy()
    newState = bgstate(old = oldState)
    points[mov-1].remove(oldState.whose_move)
    if (mov != 0):
        if (oldState.whose_move == W):
            if (R in points[mov-1-di]):
                # hitting
                points[mov-1-di].remove(R)
                bar.append(R)
            if mov-1-di >= 0:
                points[mov-1-di].append(oldState.whose_move)
            newState.whose_move = R
        else:
            if (W in points[mov-1+di]):
                # hitting
                points[mov-1+di].remove(W)
                bar.append(W)
            if mov-1+di <= 23:
                points[mov-1+di].append(oldState.whose_move)
            newState.whose_move = W
    else:
        bar.remove(oldState.whose_move)
        if (oldState.whose_move == W): points[di-1].append(W)
        else: points[24-di].append(R)
    
    newState.bar = bar
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
    rcount = 0
    wcount = 0
    for i, val in enumerate(points, 1):
        wscore += val.count(W) * (24 - i)
        rscore += val.count(R) * (i)
        wcount += val.count(W)
        rcount += val.count(R)
    
    rcount += bar.count(R)
    wcount += bar.count(W)
    
    rscore -= bar.count(R) * 20
    wscore -= bar.count(W) * 20
    
    rscore += (15 - rcount) * 30
    wscore += (15 - wcount) * 30
    
    if OUR_COLOR == W: rscore *= -1
    else: wscore *= -1
    
    return rscore + wscore
            