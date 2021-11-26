# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 00:10:47 2021

@author: alimb
"""


import unittest
import numpy as np
from exceptions import InvalidInput
from main import TicTac, TicTacGame, TicTacCPU


class TestInputValidation(unittest.TestCase):
    def test_simple_valid_input(self):
        user_input = list('123456789')
        for x in user_input:
            self.assertEqual(x, TicTac._validate_input(x, user_input))

    def test_preprocessed_valid_input(self):
        valid_input = list('yn123')
        user_input = list('yYnN123')
        for x in user_input:
            self.assertEqual(x.lower(), 
                             TicTac._validate_input(x, 
                                                    valid_input, 
                                                    lambda x: x.lower()))

    def test_preprocess_exception(self):
        valid_input = list('y')
        with self.assertRaises(InvalidInput):
            TicTac._validate_input('y', valid_input, lambda x: int(x))

    def test_invalid_input(self):
        valid_input = list('123')
        user_input = list('ashjwu4567890')
        for x in user_input:
            with self.assertRaises(InvalidInput):
                TicTac._validate_input(x, valid_input)


class TestWinning(unittest.TestCase):

    def setUp(self):
        self.game = TicTacGame((TicTacCPU(2, 1), TicTacCPU(2, 2)))

    def test_no_winning(self):
        self.game.field = np.array(
            [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8]])
        self.assertFalse(self.game._check_winning(self.game.players[0]))

        self.game.field = np.array(
            [[-1, 1, 2],
             [-1, 4, 5],
             [6, 7, 8]])
        self.assertFalse(self.game._check_winning(self.game.players[0]))

        self.game.field = np.array(
            [[-2, 1, 2],
             [-2, 4, 5],
             [-2, 7, 8]])
        self.assertFalse(self.game._check_winning(self.game.players[0]))

    def test_horizontal_three_a_row(self):
        for player in self.game.players:
            player_value = player.value
            for i in range(3):
                self.game._reset_game()
                self.game.field[i, :] = [player_value] * 3
                self.assertTrue(self.game._check_winning(player))

    def test_vertical_three_a_row(self):
        for player in self.game.players:
            player_value = player.value
            for i in range(3):
                self.game._reset_game()
                self.game.field[:, i] = [player_value] * 3
                self.assertTrue(self.game._check_winning(player))

    def test_primary_diagonal_three_a_row(self):
        self.game.field = np.array(
            [[-1, 1, 2],
             [3, -1, 5],
             [6, 7, -1]])
        self.assertTrue(self.game._check_winning(self.game.players[0]))

        self.game.field = np.array(
            [[-2, 1, 2],
             [3, -2, 5],
             [6, 7, -2]])
        self.assertTrue(self.game._check_winning(self.game.players[1]))

    def test_secondary_diagonal_three_a_row(self):
        self.game.field = np.array(
            [[0, 1, -1],
             [3, -1, 5],
             [-1, 7, 8]])
        self.assertTrue(self.game._check_winning(self.game.players[0]))

        self.game.field = np.array(
            [[0, 1, -2],
             [3, -2, 5],
             [-2, 7, 8]])
        self.assertTrue(self.game._check_winning(self.game.players[1]))


class TestCPU(unittest.TestCase):
    def setUp(self):
        self.cpu = TicTacCPU(2, 1)

    def test_no_two_a_row(self):
        field = np.array(
            [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8]])
        self.assertIsNone(self.cpu._search_row(field, -1))

        field = np.array(
            [[0, -1, 2],
             [-1, 4, 5],
             [6, 7, -1]])
        self.assertIsNone(self.cpu._search_row(field, -1))

        for i in range(3):
            field = np.array(
                [[0, 1, 2],
                 [3, 4, 5],
                 [6, 7, 8]])
            field[:, i] = [-1] * 3
            self.assertIsNone(self.cpu._search_row(field, -1))

            field = np.array(
                [[0, 1, 2],
                 [3, 4, 5],
                 [6, 7, 8]])
            field[i, :] = [-1] * 3
            self.assertIsNone(self.cpu._search_row(field, -1))

        field = np.array(
            [[-1, 1, 2],
             [-2, 4, 5],
             [-1, 7, 8]])
        self.assertIsNone(self.cpu._search_row(field, -1))

        field = np.array(
            [[0, -1, 2],
             [3, -1, 5],
             [6, -2, 8]])
        self.assertIsNone(self.cpu._search_row(field, -1))

        field = np.array(
            [[0, 1, 2],
             [-2, -1, -1],
             [6, 7, 8]])
        self.assertIsNone(self.cpu._search_row(field, -1))

    def test_horizontal(self):
        field = np.array(
            [[-1, 1, -1],
             [3, 4, 5],
             [6, 7, 8]])
        self.assertEqual((0, 1), self.cpu._search_row(field, -1))

        field = np.array(
            [[0, 1, 2],
             [3, -1, -1],
             [6, 7, 8]])
        self.assertEqual((1, 0), self.cpu._search_row(field, -1))

        field = np.array(
            [[0, 1, 2],
             [3, 4, 5],
             [-1, -1, 8]])
        self.assertEqual((2, 2), self.cpu._search_row(field, -1))

    def test_vertical(self):
        field = np.array(
            [[0, 1, 2],
             [-1, 4, 5],
             [-1, 7, 8]])
        self.assertEqual((0, 0), self.cpu._search_row(field, -1))

        field = np.array(
            [[0, -1, 2],
             [3, 4, 5],
             [6, -1, 8]])
        self.assertEqual((1, 1), self.cpu._search_row(field, -1))

        field = np.array(
            [[0, 1, -1],
             [3, 4, -1],
             [6, 7, 8]])
        self.assertEqual((2, 2), self.cpu._search_row(field, -1))

    def test_primary_diagonal(self):
        field = np.array(
            [[-1, 1, 2],
             [3, -1, 5],
             [6, 7, 8]])
        self.assertEqual((2, 2), self.cpu._search_row(field, -1))

        field = np.array(
            [[-1, 1, 2],
             [3, 4, 5],
             [6, 7, -1]])
        self.assertEqual((1, 1), self.cpu._search_row(field, -1))

        field = np.array(
            [[0, 1, 2],
             [3, -1, 5],
             [6, 7, -1]])
        self.assertEqual((0, 0), self.cpu._search_row(field, -1))

    def test_secondary_diagonal(self):
        field = np.array(
            [[0, 1, -1],
             [3, 4, 5],
             [-1, 7, 8]])
        self.assertEqual((1, 1), self.cpu._search_row(field, -1))

        field = np.array(
            [[0, 1, -1],
             [3, -1, 5],
             [6, 7, 8]])
        self.assertEqual((2, 0), self.cpu._search_row(field, -1))

        field = np.array(
            [[0, 1, 2],
             [3, -1, 5],
             [-1, 7, 8]])
        self.assertEqual((0, 2), self.cpu._search_row(field, -1))


if __name__ == '__main__':
    unittest.main()
