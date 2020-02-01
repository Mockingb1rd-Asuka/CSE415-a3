"""

"""

from backgState import *
#import numpy as np
from gameMaster import *
import sys

W = 0
R = 1

OUR_COLOR = W

def move(state, die1, die2):
    global OUR_COLOR
    OUR_COLOR = state.whose_move
    mov1, mov2, r = search(state, [die1, die2])
    res = str(mov1) + "," + str(mov2)
    if r: res += ",R"
    return res


def search(state, dice):
    mov1, mov2 = 0
    r = False
    # Search Algorithm
    succs = successors(state)
    val = -10000000
    movesDice = (1, 6)
    bestmove = ("p")
    for i in range(5, 1):
        for s in succs:
            tempval = minimax(s[0],i)
            if (tempval > val):
                val = tempval
                r = movesDice[0] == dice [0]
                movesDice = s[1]
                bestmove = s[2]
    mov1 = bestmove[0]
    mov2 = bestmove[1]
    return mov1, mov2, r


def minimax(state, depth, alpha_beta_pair):
    if depth == 0: return staticEval(state)
    if state.whose_move == OUR_COLOR: prov = -sys.maxsize -1
    else: prov = sys.maxsize
    succ = successors(state)
    for s in succ:
        newVal = minimax(s[0], depth - 1)
        if ((state.whose_move == OUR_COLOR and newVal > prov) or
            (state.whose_move != OUR_COLOR and newVal < prov)):
            prov = newVal
    return prov

def successors(state):
    re = []
    intList = []
    moves = availableMoveSet(state, [1, 6])
    
    for di in moves.keys():
        for move in moves.get(di):
            intList.append([nextState(state, move, di, False), di, move])
    
    for intState in intList:
        otherRoll = moves.keys().remove(intState[1])
        moves = availableMoveSet(intState, [otherRoll])
        for di in moves.keys():
            for mov in moves.get(di):
                re.append([nextState(intState[0], moves.get(di), di, True),
                       (intState[1], otherRoll), (intState[2], mov)])
    
    return re

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
        points[mov].remove(oldState.whose_move)
        if (color == W):
            # white's move
            if (R in points[mov - di]):
                # hitting
                points[mov - di].remove(R)
                bar.append(R)
            if mov - 1 - di >= 0:
                points[mov - di].append(oldState.whose_move)
            else:  # bearing off
                woff.append(W)
            newState.whose_move = R
        else:
            # red's move
            if (W in points[mov + di]):
                # hitting
                points[mov + di].remove(W)
                bar.append(W)
            if mov + di <= 23:
                points[mov + di].append(R)
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
    checker_list = state.pointLists
    if not checker_list[index - 1]:
        return False
    if any_on_bar(state, state.whose_move) and index != 0:
        return False
    if canBearOff(state):
        return True
    current_list = state.pointLists
    destination = index + die
    return isOpen(current_list, destination)


def availableMoveSet(state, dice):
    moveset_available = {}
    checkers_list = state.pointLists
    for number in dice:
        moveset_available[number] = []
        for index, checkers in enumerate(checkers_list, 1):
            if canMove(state, index, number):
                moveset_available[number] += [index]
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
