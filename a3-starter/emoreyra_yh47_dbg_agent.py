"""

"""

from backgState import *
from gameMaster import *

W = 0
R = 1

OUR_COLOR = W

def move(state, die1, die2):
    global OUR_COLOR
    OUR_COLOR = state.whose_move
    mov1, mov2, r = search()
    res = str(mov1) + "," + str(mov2)
    if r: res.append(",R")
    return res


def search():
    mov1, mov2 = 0
    R = False
    # Search Algorithm

    return mov1, mov2, R
    
def nextState(oldState, mov, di, endturn):
    # Assumes move is valid
    if (mov in ["P", "p"]): return bgstate(old=oldState)  # passing gives same state
    bar = oldState.bar.copy()
    points = oldState.pointLists.copy()
    roff = oldState.red_off.copy()
    woff = oldState.white_off.copy()
    newState = bgstate(old=oldState)
    if (mov != 0):
        # moving from point
        points[mov - 1].remove(oldState.whose_move)
        if (color == W):
            # white's move
            if (R in points[mov - 1 - di]):
                # hitting
                points[mov - 1 - di].remove(R)
                bar.append(R)
            if mov - 1 - di >= 0:
                points[mov - 1 - di].append(oldState.whose_move)
            else:  # bearing off
                woff.append(W)
            newState.whose_move = R
        else:
            # red's move
            if (W in points[mov - 1 + di]):
                # hitting
                points[mov - 1 + di].remove(W)
                bar.append(W)
            if mov - 1 + di <= 23:
                points[mov - 1 + di].append(R)
            else:  # bearing off
                roff.append(R)
            newState.whose_move = W
    else:
        # Remove from bar
        bar.remove(oldState.whose_move)
        
    if (endturn):
        if (oldState.whose_move == W): points[di-1].append(W)
        else: points[24-di].append(R)

    newState.white_off = woff
    newState.red_off = roff
    newState.bar = bar
    newState.pointLists = points

    return newState


def canMove(state, index, die):
    if any_on_bar(state, state.whose_move):
        return False
    if canBearOff(state):
        return True
    current_list = state.pointLists
    destination = index + die
    return isOpen(current_list, destination)


def availableMoveSet(state):
    moveset_available = {}
    color = state.whose_move
    checkers_list = state.pointLists
    for index, checkers in enumerate(checkers_list):
        if checkers and checkers[0] == color:
            if canMove(state, index, 1):
                moveset_available[1] += [index]
            if canMove(state, index, 6):
                moveset_available[6] += [index]
    return moveset_available


def isOpen(state, location):
    destination = state.pointLists[location]
    if state.whose_move == W:
        return destination[0] != R or len(destination) < 2
    else:
        return destination[0] != W or len(destination) < 2


def canBearOff(state):
    checker_position = state.pointLists
    home_range = homeRange(state)
    for index in home_range:
        return checker_position[index][0] != state.whose_move

def homeRange(state):
    if state.whose_move == W:
        home_range = range(7, 25)
    else:
        home_range = range(1, 19)
    return home_range



def staticEval(state):
    bar = state.bar
    points = state.pointLists
    # score for each color based on position
    rscore = 0
    wscore = 0
    # number of each color in board
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

    if OUR_COLOR == W:
        rscore *= -1
    else:
        wscore *= -1

    return rscore + wscore

    pass


class StateTree:

    def __init__(self, state):
        self.state = state
        self.children = []

    def get_children(self):
        return self.children

    def __add__(self, child):
        self.children += child

    def del_child(self, index):
        self.children.pop(index)

    def del_multiple_child(self, start, end):
        del self.children[start:end]
