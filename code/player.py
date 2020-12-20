import numpy as np
import random


class Player(object):
    def __init__(self, id, goods, K, value_array=None):
        self.id = id
        self.goods = goods
        self.K = K
        '''
        Assume [0,1] valuation for every goods.
        Else, assign values inidividually.
        '''
        if np.any(value_array) != None:
            # if np.any(value_array) != None or len(value_array) > 0:
            self.value_array = value_array
        else:
            self.value_array = np.zeros_like(goods)
            for i in range(len(goods)):
                if i == len(goods)-1:
                    self.value_array[i] = self.K
                else:
                    self.value_array[i] = random.randrange(0, self.K)
                self.K -= self.value_array[i]
                if self.K == 0:
                    break
        # print("K = "+str(self.K))

    def valuation(self, subset_of_goods):
        valuation = 0.
        for i in range(len(subset_of_goods)):
            valuation += self.value_array[i] * subset_of_goods[i]
        return valuation
