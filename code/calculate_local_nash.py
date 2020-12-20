import numpy as np
from player import Player


def calculate_local_nash(player_i, player_j, A_i, A_j, g):
    '''
    Transfer a good g if 
        vi(Ai+g)* vj (Aj -g) > vi(Ai)* vj (Aj ))
    Terminate else.
    '''
    room_to_improve1 = (player_i.valuation(A_i + g) * player_j.valuation(A_j - g) -
                        player_i.valuation(A_i) * player_j.valuation(A_j) > 0) and np.all(A_j - g >= 0)

    room_to_improve2 = player_i.valuation(g) > 0 and player_j.valuation(g) == 0

    debug = False
    if debug:
        print("val cal "+str([player_i.valuation(A_i + g), player_j.valuation(
            A_j - g), player_i.valuation(A_i), player_j.valuation(A_j)]))
        print("bool "+str([room_to_improve1, room_to_improve2]))
    return room_to_improve1 or room_to_improve2
