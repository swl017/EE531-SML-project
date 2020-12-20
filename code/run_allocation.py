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
    n = 3

    m = 2*n
    items = m
    quantities = np.ones(items)
    goods = Goods(items, quantities)
    players = []
    preference = np.ones(items)
    K = 500
    for i in range(n):
        players.append(Player(i, goods.total_set, K))
        # players.append(Player(i, goods.total_set, K, preference))
        print("player "+str(i)+"'s preference: "+str(players[i].value_array))
    # players.append(Player(0, goods.total_set, [1., 0.]))
    # players.append(Player(1, goods.total_set, [0., 1.]))

    '''
    Setup initial allocation
    '''
    A_all = np.ones(m)
    for i in range(n-1):
        A_all = np.vstack([A_all, np.zeros(m)])
    A_init = copy.deepcopy(A_all)
    print("A_all:"+str(A_all))
    # A_all = np.ones(n)*m/n
    # for i in range(int(n/3.)):
    #     A_all[i] += 1
    #     A_all[len(A_all)-1-i] -= 1
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
        for i in range(m):
            g = np.zeros(m)
            g[i] = 1  # g \in A_j st [0,1]
            if debug:
                print("===========")
                print("g   = "+str(g))
            permute = permutations(players, 2)
            for player_i_j in permute:
                if player_i_j[0].id == player_i_j[1].id:
                    continue
                num_iter += 1
                A_i = A_all[player_i_j[0].id]
                A_j = A_all[player_i_j[1].id]
                if debug:
                    print("---")
                    print("Player [i,j] = " +
                          str([player_i_j[0].id, player_i_j[1].id]))
                    print("iter: "+str(num_iter))
                    print("A   = "+str(A_all))
                    print("A_i = "+str(A_i))
                    print("A_i+g = "+str(A_i+g))
                    print("A_j = "+str(A_j))
                    print("A_j-g = "+str(A_j-g))

                if calculate_local_nash(player_i_j[0], player_i_j[1], A_i, A_j, g):
                    A_all[player_i_j[0].id] += g
                    A_all[player_i_j[1].id] -= g
                    if debug:
                        print("Allocation = "+str(A_all))
                    iter_flag = True

    # num_iter *= 0.5
    print("===========")
    print("Number of players: "+str(n))
    print("Number of goods  : "+str(m))
    print("Initial allocation: ")
    print(str(A_init))
    print("Resulting allocation: ")
    print(str(A_all))
    print("Values: ")
    for i in range(n):
        print("v("+str(i)+") = "+str(players[i].valuation(A_all[i])))
    print("Num of itereations = "+str(num_iter))
    print("Max valuation v(M) = "+str(max_valuation))


if __name__ == "__main__":
    main()
