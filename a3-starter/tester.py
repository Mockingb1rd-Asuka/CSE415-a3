from emoreyra_yh47_dbg_agent import *
from backgState import *

state = bgstate()
moveset = availableMoveSet(state, [1, 6])
#print(state)
#print(moveset[1])

succ_list = successors(state)
#print(succ_list)
for succ in succ_list:
    print(succ[0].prettyPrint())
#print(canMove(state, 6, 1), 6, 1)