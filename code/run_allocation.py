import numpy as np
from itertools import permutations, combinations, combinations_with_replacement
import copy

from player import Player
from goods import Goods
from calculate_local_nash import calculate_local_nash


def check_pareto_dominate(player_i, player_j, A_i, A_j):
    value_delta = np.zeros_like(A_i)
    for k in range(len(A_i)):
        value_delta[k] = player_i.value_array[k] * \
            A_i[k] - player_j.value_array[k] * A_j[k]
    i_dominate_j = np.all(value_delta >= 0)
    j_dominate_i = np.all(value_delta <= 0)
    return i_dominate_j, j_dominate_i, value_delta


def main():
    '''
    Set number of players n and goods m
    '''
    debug = False
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    # Players
    n = 10
    # Goods
    m = 5*n
    # Types of goods. Select (m or n)
    items = n
    # Sum of valuations
    K = 500

    quantities = np.ones(items)*m/items
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
    and Nash wellfare values
    '''
    max_nash = 1.
    num_iter = 0
    iter_flag = True

    while iter_flag:
        iter_flag = False

        # For every kinds of items
        for i in range(len(A_all[0])):
            g = np.zeros_like(A_all[0])
            g[i] = 1  # g \in A_j st [0,1]

            if debug:
                print("=========== m="+str(i))
                print("g = "+str(g))
            permute = permutations(players, 2)

            # For every permuation of players
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

                nash_wellfare = 1.
                for k in range(n):
                    nash_wellfare *= players[k].valuation(A_all[k])
                max_nash = max(max_nash, nash_wellfare)

    max_nash_brute = 1.
    # '''
    # Brute force combination
    # '''
    # player_list = [x for x in range(n)]
    # comb_list = []
    # for i in range(item):
    #     comb_list.append([])
    #     # num of player of each item
    #     for cwr in combinations_with_replacement(player_list, quantities[i]):
    #         comb_list[i].append(cwr)

    # c_x = 1
    # for i in range(n):
    #     c_x *= len(comb_list[i])
    # comb_index_list = np.zeros((c_x, item))

    # done = False
    # A_iter = np.zeros_like(A_all)
    # for i in range(c_x):
    #     for j in range(items):
    #         for l in comb_list[j][comb_index_list[i][j]]:
    #             for m in l:
    #                 A_iter[m][j] += 1
    # for i in range(items):
    #     for j in range(comb_list[i][comb_index_list[i]]):
    #         A_iter[j][i] += 1
    # nash_wellfare_brute = 1.
    # for i in range(n):
    #     nash_wellfare_brute *= players[i].valuation(A_iter[i])
    # max_nash_brute = max(max_nash_brute, nash_wellfare_brute)

    # permute_index = []
    # for x in range(items):
    #     permute_index.append([])
    #     for y in range(len(comb_list[x])):
    #         permute_index[x].append(y)
    # permute_brute = permutaions(permute_index, items)
    #   for comb_list_index in permute_brute:
    #        for i in range(len(comb_list_index)):
    #             comb_list[i][comb_list_index[i]]

    #         for cwr in combinations_with_replacement(player_list, quantities[i]):

    #             for player_cwr in cwr:
    #                 A_iter[pl][i] += 1

    #         for j in range(quantities[i]):
    #             pl = random.randrange(0, n)

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
        print(" - v_"+str(i)+"(A) = "+str(players[i].valuation(A_all[i])))
    print("Num of itereations = "+str(num_iter))
    print("Max valuation v(M) = "+str(max_valuation))

    pareto_optimal = True
    print("Check Pareto Optimality:")
    combination = combinations(players, 2)
    for player_i_j in combination:
        if player_i_j[0].id == player_i_j[1].id:
            continue
        else:
            i_dominate_j, j_dominate_i, value_delta = check_pareto_dominate(
                player_i_j[0], player_i_j[1], A_i, A_j)
            if i_dominate_j and not j_dominate_i:
                print(" - Player "+str(player_i_j[0].id)+" > " +
                      str(player_i_j[1].id)+" by "+str(value_delta))
                pareto_optimal = False
            elif j_dominate_i and not i_dominate_j:
                print(" - Player "+str(player_i_j[0].id)+" < " +
                      str(player_i_j[1].id)+" by "+str(value_delta))
                pareto_optimal = False
            else:
                print(" - Player "+str(player_i_j[0].id)+" ~ " +
                      str(player_i_j[1].id)+" by "+str(value_delta))

    print("Check Maximum Nash Wellfare:")
    print(" - Current NW = "+str(nash_wellfare))
    print(" - MNW        = "+str(max_nash_brute))
    MNW = (max_nash_brute == nash_wellfare)

    if pareto_optimal:
        print("It is Pareto_optimal")
    else:
        print("NOT Pareto_optimal")
    if MNW:
        print("It is MNW")
    else:
        print("NOT MNW")

    return pareto_optimal, MNW


if __name__ == "__main__":
    num_iter = 1000
    num_pareto = 0
    num_mnw = 0
    for i in range(num_iter):
        pareto_optimal, MNW = main()
        num_pareto += int(pareto_optimal)
        num_mnw += int(MNW)
    print("Pareto: "+str(num_pareto)+" Nash: " +
          str(num_mnw)+" / "+str(num_iter))
