import numpy as np
from itertools import permutations
import copy

from player import Player
from goods import Goods
from calculate_local_nash import calculate_local_nash


def main():
    '''
    Set number of players n and goods m
    '''
    debug = False
    # Players
    n = 5
    # Goods
    m = 3*n
    # Types of goods. Select (m or n)
    items = n
    # Sum of valuations
    K = 500

    quantities = np.ones(items)*items/m
    goods = Goods(items, quantities)

    # Create player instances
    players = []
    preference = np.ones(items)

    for i in range(n):
        players.append(Player(i, goods.total_set, K))
        # players.append(Player(i, goods.total_set, K, preference))
        print("player "+str(i)+"'s preference: "+str(players[i].value_array))

    '''
    Setup initial allocation
    '''
    A_all = quantities

    for i in range(n-1):
        A_all = np.vstack([A_all, np.zeros(items)])
    A_init = copy.deepcopy(A_all)
    print("A_all:"+str(A_all))
    '''
    Search maximum valuation
    '''
    max_valuation = 0

    for i in range(n):
        max_valuation = max(max_valuation, players[i].valuation(A_all[i]))

    '''
    Loop for permutations of players
    '''
    num_iter = 0
    iter_flag = True

    while iter_flag:
        iter_flag = False

        for i in range(len(A_all[0])):
            g = np.zeros_like(A_all[0])
            g[i] = 1  # g \in A_j st [0,1]

            if debug:
                print("=========== m="+str(i))
                print("g = "+str(g))
            permute = permutations(players, 2)

            for player_i_j in permute:
                if player_i_j[0].id == player_i_j[1].id:
                    continue

                num_iter += 1

                # Allocations for player i and j
                A_i = A_all[player_i_j[0].id]
                A_j = A_all[player_i_j[1].id]
                if debug:
                    print("---")
                    print("Player [i,j] = " +
                          str([player_i_j[0].id, player_i_j[1].id]))
                    print("iter: " + str(num_iter))
                    print("A   = " + str(A_all))
                    print("A_i = " + str(A_i))
                    print("A_i+g = "+str(A_i+g))
                    print("A_j = " + str(A_j))
                    print("A_j-g = "+str(A_j-g))

                if np.any(A_j - g < 0):  # Avoid impossible cases
                    continue
                elif calculate_local_nash(player_i_j[0], player_i_j[1], A_i, A_j, g):
                    '''
                    Transfer a good g if 
                        vi(Ai+g)* vj (Aj -g) > vi(Ai)* vj (Aj ))
                    -> True if allocations can be imnproved    
                    '''
                    A_all[player_i_j[0].id] += g
                    A_all[player_i_j[1].id] -= g
                    if debug:
                        print("Allocation = "+str(A_all))
                    iter_flag = True

    '''
    Result summary
    '''
    print("===========")
    print("Number of players: "+str(n))
    print("Number of goods  : "+str(m))
    print("Initial allocation: ")
    print(str(A_init))
    print("Resulting allocation: ")
    print(str(A_all))
    print("Values: ")
    for i in range(n):
        print("v_"+str(i)+"(A) = "+str(players[i].valuation(A_all[i])))
    print("Num of itereations = "+str(num_iter))
    print("Max valuation v(M) = "+str(max_valuation))


if __name__ == "__main__":
    main()
