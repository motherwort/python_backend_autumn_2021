# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 16:54:39 2021

@author: alimb
"""


class CustomMeta(type):

    @staticmethod
    def __customize(dct):
        def make_custom(x):
            if x.startswith('__') and x.endswith('__'):
                return x
            else:
                return 'custom_' + x
                
        return {make_custom(x): dct[x] for x in dct}

    def __call__(self, *args, **kwargs):
        obj = self.__new__(self, *args, **kwargs)
        self.__init__(obj, *args, **kwargs)
        obj.__dict__ = CustomMeta.__customize(obj.__dict__)
        return obj

    def __new__(cls, name, bases, attrs):
        custom_attrs = CustomMeta.__customize(attrs)
        new_class = super().__new__(cls, name, bases, custom_attrs)
        return new_class


if __name__ == '__main__':
    pass
