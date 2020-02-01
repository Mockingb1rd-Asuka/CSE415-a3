"""

"""

from backgState import *

W = 0
R = 1

OUR_COLOR = W
STATE_TREE = None


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


def canMove(state, move, die):
    if OUR_COLOR in state.bar:
        return False
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


def buildStateTree(state, color):
    global STATE_TREE
    STATE_TREE = StateTree(state)
    buildBranch(STATE_TREE, color, state, 1)


def buildBranch(root, color, state, step):
    checkers_available = build_dict(state)
    if step == 1:
        color = 1 - color  # changing color
    if checkers_available:
        for index, checkers in checkers_available.items():
            new_state = nextState(state, index, step, color)
            new_leaf = StateTree(new_state)
            root.__add__(new_leaf)
            buildBranch(new_leaf, color, new_state, 7 - step)  # waiving between 1 and 6


def build_dict(state):
    currentState = state.pointLists
    stateDict = {}
    if state.bar:
        stateDict[0] = [state.bar[0], len(state.bar)]
    for index, checkers in enumerate(currentState, 1):
        if checkers:
            stateDict[index] = [checkers[index][0], len(checkers)]
    return stateDict


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
