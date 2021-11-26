# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 15:46:26 2021

@author: alimb
"""

import unittest
from custom_list import CustomList
from custom_meta import CustomMeta


class TestCustomList(unittest.TestCase):

    def test_instance(self):

        A = CustomList(5, 1, 3, 7)
        B = CustomList(1, 2, 7)
        self.assertIsInstance(A + B, CustomList)
        self.assertIsNot(A + B, A)
        self.assertIsNot(A + B, B)

    def test_arithmetics(self):

        A = CustomList(5, 1, 3, 7)
        B = CustomList(1, 2, 7)

        self.assertSequenceEqual(A - B,
                                 CustomList(4, -1, -4, 7))

        self.assertSequenceEqual(A + B,
                                 CustomList(6, 3, 10, 7))

    def test_arithmetics_with_lists(self):

        A = [1, 2]
        B = CustomList(3, 4)

        self.assertIsInstance(A + B, CustomList)
        self.assertSequenceEqual(A + B, CustomList(4, 6))

        self.assertIsInstance(A - B, CustomList)
        self.assertSequenceEqual(A - B, CustomList(-2, -2))

        self.assertIsInstance(B + A, CustomList)
        self.assertSequenceEqual(B + A, CustomList(4, 6))

        self.assertIsInstance(B - A, CustomList)
        self.assertSequenceEqual(B - A, CustomList(2, 2))

    def test_no_mutating_list_operand(self):

        A = [1, 2]
        B = CustomList(3, 4, 5)

        a = A.copy()
        _ = a + B
        self.assertFalse(isinstance(a, CustomList))
        self.assertEqual(len(a), len(A))
        self.assertSequenceEqual(a, A)

        a = A.copy()
        _ = B + a
        self.assertFalse(isinstance(a, CustomList))
        self.assertEqual(len(a), len(A))
        self.assertSequenceEqual(a, A)

        a = A.copy()
        _ = a - B
        self.assertFalse(isinstance(a, CustomList))
        self.assertEqual(len(a), len(A))
        self.assertSequenceEqual(a, A)

        a = A.copy()
        _ = B - a
        self.assertFalse(isinstance(a, CustomList))
        self.assertEqual(len(a), len(A))
        self.assertSequenceEqual(a, A)

    def test_no_mutating_CustomList_operand(self):

        A = CustomList(1, 2)
        B = CustomList(3, 4, 5)

        a = A.copy()
        _ = a + B
        self.assertEqual(len(a), len(A))
        self.assertSequenceEqual(a, A)

        a = A.copy()
        _ = B + a
        self.assertEqual(len(a), len(A))
        self.assertSequenceEqual(a, A)

        a = A.copy()
        _ = a - B
        self.assertEqual(len(a), len(A))
        self.assertSequenceEqual(a, A)

        a = A.copy()
        _ = B - a
        self.assertEqual(len(a), len(A))
        self.assertSequenceEqual(a, A)

    def test_equals(self):

        a = CustomList(1, 2, 3)
        b = CustomList(2, 1, 3)
        c = [1, 1, 4]
        d = CustomList(5, -2, 3)
        e = CustomList(3, 3)
        f = CustomList(1, 2, 4)
        g = CustomList(0, 2, 3)
        h = [5, 1, 4]
        i = CustomList(5)
        j = 6

        self.assertEqual(a, b)
        self.assertEqual(a, c)
        self.assertEqual(a, d)
        self.assertEqual(a, e)

        self.assertNotEqual(a, f)
        self.assertNotEqual(a, g)
        self.assertNotEqual(a, h)
        self.assertNotEqual(a, i)
        self.assertNotEqual(a, j)


class TestCustomMeta(unittest.TestCase):

    def test_custom_meta(self):

        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

        inst = CustomClass()

        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)

        self.assertRaises(AttributeError, lambda: inst.x)
        self.assertRaises(AttributeError, lambda: inst.val)
        self.assertRaises(AttributeError, lambda: inst.line())

        inst = CustomClass(13)
        self.assertEqual(inst.custom_val, 13)

        class Foo(metaclass=CustomMeta):
            val = -14

        foo = Foo()
        self.assertEqual(foo.custom_val, -14)


if __name__ == '__main__':
    unittest.main()
