import numpy as np
import random

class Goods(object):
    def __init__(self, items, quantities, rand_quantities=False, total_item_num=0):
        self.items      = items
        self.quantities = quantities
        self.total_set  = np.zeros(items)
        self.total_item_num = total_item_num
        if not rand_quantities:
            for i in range(len(quantities)):
                self.total_set[i] = quantities[i]
        else:
            for i in range(len(quantities)):
                if self.total_item_num > 0:
                    self.total_set[i]    = random.randrange(0,int(total_item_num*.7)+1)
                    self.total_item_num -= self.total_set[i]
