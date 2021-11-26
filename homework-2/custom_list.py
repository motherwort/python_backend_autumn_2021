# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 15:45:23 2021

@author: alimb
"""


class CustomList(list):

    def __init__(self, *args):
        if (len(args) == 1) and isinstance(args[0], list):
            super().__init__(args[0])
        else:
            super().__init__(list(args))

    def __eq__(self, o):
        if not (isinstance(o, list)):
            return False
        else:
            return sum(self) == sum(o)

    def __add__(self, x):
        min_len = min(len(x), len(self))
        a = [self[i] + x[i] for i in range(min_len)]

        if len(self) > len(x):
            b = self[min_len:]
        else:
            b = x[min_len:]

        return CustomList(a + b)

    def __sub__(self, x):
        min_len = min(len(x), len(self))
        a = [self[i] - x[i] for i in range(min_len)]

        if len(self) > len(x):
            b = self[min_len:]
        else:
            b = list(map(lambda x: -x, x[min_len:]))

        return CustomList(a + b)

    def __radd__(self, x):
        return CustomList.__add__(self, x)

    def __rsub__(self, x):
        return CustomList.__sub__(x, self)

    def __iadd__(self, x):
        return CustomList.__add__(self, x)

    def __isub__(self, x):
        return CustomList.__sub__(self, x)


if __name__ == '__main__':
    pass
