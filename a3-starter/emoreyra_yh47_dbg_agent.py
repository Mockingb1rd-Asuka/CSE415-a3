"""

"""

from backgState import *

from gameMaster import *

OUR_COLOR = 0
STATE_TREE = []
WHITE = 0
RED = 1
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
    if gameMaster.any_on_bar(state, OUR_COLOR):
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
    pass

def buildStateTree(state, move):
    root = state
    STATE_TREE = StateTree(state)
    next_move = 1 - state.whose_move
    for checkerPair

class StateTree:

    def __init__(self, state):
        self.state = state
        self.state_list = self.build_dict
        self.children = []

    def __getstate__(self):
        return self.state

    def get_children(self):
        return self.children

    def __add__(self, child):
        self.children += child

    def del_child(self, index):
        self.children.pop(index)

    def del_multiple_child(self, start, end):
        del self.children[start:end]

    def build_dict(self):
        currentState = self.state.pointLists
        stateList = {}
        if self.state.bar:
            stateList[0] = [self.state.bar[0], len(self.state.bar)]
        for index, checkers in enumerate(currentState, 1):
            if checkers:
                stateList[index] = [checkers[index][0], len(checkers)]
        return stateList