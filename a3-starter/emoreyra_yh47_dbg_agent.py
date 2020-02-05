'''
emoreyra_yh47_dbg_agent.py
CSE 415, Winter 2020, Assignment 3
Emela Moreyra - emoreyra
jerry Hong - yh47
'''

from backgState import *
import sys

W = 0
R = 1

OUR_COLOR = W

prune_count = 0


def move(state, die1, die2):
    global OUR_COLOR
    OUR_COLOR = state.whose_move
    mov1, mov2, r = search(state, [die1, die2])
    res = str(mov1)
    if (mov2 != -1): res += "," + str(mov2)
    if r: res += ",R"
    return res


def search(state, dice):
    mov1 = 0
    mov2 = 0
    R = False
    depth = 2
    # Search Algorithm
    succ = successors(state)
    vals = []
    for i in range(1, depth):
        vals = []
        for s in succ:
            vals.append(minimax(s, i, -sys.maxsize - 1, sys.maxsize))
    
    succ_sel = vals.index(max(vals))
    pick = succ[succ_sel]
    if (len(pick[1]) != 0):
        R = pick[1][0] != dice[0]
    mov1 = pick[2][0]
    if (len(pick[2]) < 2): mov2 = -1 #this move is not used in this case
    else: mov2 = pick[2][1]
        
    return mov1, mov2, R


def minimax(state, depth, alpha, beta):
    global prune_count
    if depth == 0: return staticEval(state[0])
    if state[0].whose_move == OUR_COLOR:
        prov = -sys.maxsize - 1
    else:
        prov = sys.maxsize
    succ = successors(state[0])
    for s in succ:
        newVal = minimax(s, depth - 1, alpha, beta)
        if state[0].whose_move == OUR_COLOR and newVal > prov:
            prov = newVal
            alpha = newVal
            print("new_alpha:" + str(alpha))
        elif state[0].whose_move != OUR_COLOR and newVal < prov:
            prov = newVal
            beta = newVal
            #print("new_beta:" + str(beta))
        if alpha >= beta:
            prune_count += 1
            print("prune_num" + str(prune_count))
            break
    return prov


def successors(state):
    re = []
    intList = []
    moves = availableMoveSet(state, [1, 6])

    for di in moves.keys():
        for m in moves.get(di):
            intList.append([nextState(state, m, di, False), di, m])

    for intState in intList:
        if (intState[2] not in ["P", "p"]):
            for roll in moves.keys():
                if roll != intState[1]:
                    otherRoll = roll
            int_moves = availableMoveSet(intState[0], [otherRoll])
            for di in int_moves.keys():
                for mov in int_moves.get(di):
                    if canMove(intState[0], mov, di):
                        the_successor = [nextState(intState[0], mov, di, True),
                                         (intState[1], otherRoll), (intState[2], mov)]
                        if the_successor not in re:
                            re.append(the_successor)
        else:
            re.append([intState[0], (), (intState[2])])
    return re


def nextState(oldState, mov, di, endturn):
    # Assumes move is valid
    newState = bgstate(old=oldState)
    if (mov in ["P", "p"]): 
        newState.whose_move = 1 - newState.whose_move
        return newState  # passing gives same state
    
    if (mov != 0):
        # moving from point
        mov = mov - 1
        newState.pointLists[mov].remove(oldState.whose_move)
        if (oldState.whose_move == W):
            # white's move
            if (R in newState.pointLists[mov + di]):
                # hitting
                newState.pointLists[mov + di].remove(R)
                newState.bar.append(R)
            if mov + di <= 23:
                newState.pointLists[mov + di].append(oldState.whose_move)
            else:  # bearing off
                newState.white_off.append(W)
        else:
            # red's move
            if (W in newState.pointLists[mov - di]):
                # hitting
                newState.pointLists[mov - di].remove(W)
                newState.bar.append(W)
            if mov - di >= 0:
                newState.pointLists[mov - di].append(R)
            else:  # bearing off
                newState.white_off.append(R)
    else:
        # Remove from bar
        bar.remove(oldState.whose_move)

    if (endturn):
        newState.whose_move = 1 - newState.whose_move

    return newState


def canMove(state, index, die):
    if (index in ["P", "p"]): return True
    checker_list = state.pointLists
    index -= 1
    if state.whose_move in state.bar and index != 0:
        return False
    if not checker_list[index]:
        return False
    if checker_list[index][0] != state.whose_move:
        return False
    if canBearOff(state):
        if state.whose_move == W: dest_pt = index + die
        else: dest_pt = index - die
        return bear_off(state, index, dest_pt, state.whose_move) != False
    if state.whose_move == W:
        destination = index + die
    else:
        destination = index - die
    return isOpen(state, destination)


def availableMoveSet(state, dice):
    moveset_available = {}
    checkers_list = state.pointLists
    for number in dice:
        moveset_available[number] = ["p"]
        for index, checkers in enumerate(checkers_list, 0):
            if canMove(state, index-1, number):
                moveset_available[number] += [index-1]
    return moveset_available


def isOpen(state, location):
    checker_lists = state.pointLists
    if location >= len(checker_lists) or location < 0:
        return False
    destination = checker_lists[location]
    if not destination:
        return True
    elif state.whose_move == W:
        return destination[0] != R or len(destination) < 2
    else:
        return destination[0] != W or len(destination) < 2


def canBearOff(state):
    checker_position = state.pointLists
    if state.whose_move == R:
        home_range = range(6, 24)
    else:
        home_range = range(0, 18)
    for index in home_range:
        if checker_position[index] and checker_position[index][0] == state.whose_move:
            return False
    return True


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
        wscore += val.count(W) * (i)
        rscore += val.count(R) * (24 - i)
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




def bear_off(state, src_pt, dest_pt, who):
  # Return False if 'who' is not allowed to bear off this way.
  # Otherwise, create the new state showing the result of bearing
  # this one checker off, and return the new state.

  # First of all, is bearing off allowed, regardless of the dice roll?
  if not bearing_off_allowed(state, who): return False
  # Direct bear-off, if possible:
  pl = state.pointLists[src_pt-1]
  if pl==[] or pl[0]!=who:
    print("Cannot bear off from point "+src(src_pt))
    return False
  # So there is a checker to possibly bear off.
  # If it does not go exactly off, then there must be
  # no pieces of the same color behind it, and dest
  # can only be one further away.
  good = False
  if who==W:
    if dest_pt==25:
       good = True
    elif dest_pt==26:
       for point in range(18,src_pt-1):
         if W in state.pointLists[point]: return False
       good = True
  elif who==R:
    if dest_pt==0:
       good = True
    elif dest_pt== -1:
       for point in range(src_pt, 6):
         if R in state.pointLists[point]: return False
       good = True
  if not good: return False
  born_off_state = bgstate(state)
  born_off_state.pointLists[src_pt-1].pop()
  if who==W: born_off_state.white_off.append(W)
  else:  born_off_state.red_off.append(R)
  return born_off_state
