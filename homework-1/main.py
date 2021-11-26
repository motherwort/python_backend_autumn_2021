# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 13:23:22 2021

@author: alimb
"""


import numpy as np
import time
from exceptions import InvalidInput


class TicTac:
    def __init__(self):
        pass

    def run(self):
        self.__show_menu()
        game_mode = self.__game_mode_dialogue()
        players = self.__init_players(game_mode)
        game = TicTacGame(players)

        while(True):
            game.start_game()
            if not self.__play_again_dialogue():
                break

    def __show_menu(self):
        print('===============================\n' +
              'xxx                         ooo\n' +
              'xxx       TIC-TAC-TOE       ooo\n' +
              'xxx                         ooo\n' +
              'xxx                         ooo\n' +
              'xxx    Select game mode:    ooo\n' +
              'xxx                         ooo\n' +
              'xxx  [1] Player vs. Player  ooo\n' +
              'xxx  [2] Player vs. CPU     ooo\n' +
              'xxx  [3] CPU vs. CPU        ooo\n' +
              'xxx                         ooo')

    @staticmethod
    def _validate_input(raw_input, valid_input, preprocess=None):
        if preprocess is None:
            user_input = raw_input
        else:
            try:
                user_input = preprocess(raw_input)
            except Exception:
                raise InvalidInput()

        if user_input in valid_input:
            return user_input
        else:
            raise InvalidInput()

    @staticmethod
    def _user_input_dialogue(valid_input, 
                             preprocess=None, 
                             postprocess=None, 
                             exception_message=''):
        while(True):
            try:
                raw_input = input()
                validated_input = TicTac._validate_input(raw_input, 
                                                         valid_input, 
                                                         preprocess)
                if postprocess is None:
                    return validated_input
                else:
                    return postprocess(validated_input)
            except InvalidInput:
                print('\n' + exception_message)

    def __game_mode_dialogue(self):
        exception_message = 'Input 1, 2 or 3 to select game mode. Try again.'
        return TicTac._user_input_dialogue(valid_input=list('123'), 
                                           postprocess=lambda x: int(x),
                                           exception_message=exception_message)

    def __play_again_dialogue(self):
        time.sleep(1.2)
        print('\nPlay again? [Y/n]')
        exception_message = "Input n or N to end game, input y or Y or press enter to play again."
        return TicTac._user_input_dialogue(valid_input=['', 'y', 'n'], 
                                           preprocess=lambda x: x.lower(),
                                           postprocess=lambda x: x in ['', 'y'],
                                           exception_message=exception_message)

    def __input_player_name(self, n):
        print(f'\nInput Player {n} name:')
        name = input()
        return name

    def __select_cpu_mode(self, n):
        print(f'\nSelect CPU{n} mode: 1 (weak) or 2 (good)')
        exception_message = 'Input 1 or 2 to select CPU mode. Try again.'
        return TicTac._user_input_dialogue(valid_input=list('12'), 
                                           postprocess=lambda x: int(x),
                                           exception_message=exception_message)

    def __init_players(self, game_mode):
        if game_mode < 3:
            player1 = TicTacPlayer(self.__input_player_name(1), 1)
        else:
            player1 = TicTacCPU(self.__select_cpu_mode(1), 1)

        if game_mode < 2:
            player2 = TicTacPlayer(self.__input_player_name(2), 2)
        else:
            player2 = TicTacCPU(self.__select_cpu_mode(2), 2)
        return player1, player2


class TicTacCPU:

    def __init__(self, mode, number):
        self.mode = mode
        self.name = f'CPU{number}'
        self.score = 0
        self.value = -number

    def make_turn(self, field):
        print('\nThinking...', end='')
        time.sleep(1.2)
        print()
        if self.mode == 1:
            index = self.__engine1(field)
        elif self.mode == 2:
            index = self.__engine2(field)

        field[index] = self.value

    def __engine1(self, field):
        while(True):
            index = tuple(np.random.randint(0, 3, 2))
            if field[index] >= 0:
                return index

    def _search_row(self, field, value):
        def two_a_row(x, y):
            return (np.sum(x == y) == 2 and np.sum(x < 0) == 2)

        for i in range(3):
            if two_a_row(field[i, :3], value):
                index = (i, np.where(field[i, :] >= 0)[0][0])
                break
            elif two_a_row(field[:, i], value):
                index = (np.where(field[:, i].flatten() >= 0)[0][0], i)
                break
        else:
            if two_a_row(field.diagonal(), value):
                i = np.where(field.diagonal() >= 0)[0][0]
                index = (i, i)
            elif two_a_row(np.fliplr(field).diagonal(), value):
                i = np.where(np.fliplr(field).diagonal() >= 0)[0][0]
                index = (i, 2 - i)
            else:
                index = None

        return index

    def __engine2(self, field):
        if np.sum(field < 0) == 0:
            index = tuple(np.random.randint(0, 3, 2))
        else:
            index = self._search_row(field, self.value)
            if index is None:
                enemy_value = -2 if self.value == -1 else -1
                index = self._search_row(field, enemy_value)
            if index is None:
                index = self.__engine1(field)

        return index


class TicTacPlayer:

    def __init__(self, name, number):
        self.name = name
        self.score = 0
        self.value = -number
        pass

    def __make_turn_dialogue(self):
        print('\nEnter a number:')
        exception_message = 'Input a number from 1 to 9 corresponding to a free cell. Try again.'
        return TicTac._user_input_dialogue(valid_input=list('123456789'),
                                           postprocess=lambda x: int(x) - 1,
                                           exception_message=exception_message)

    def make_turn(self, field):
        while(True):
            user_input = self.__make_turn_dialogue()
            index = (user_input // 3, user_input % 3)
            if field[index] >= 0:
                field[index] = self.value
                return
            else:
                print('\nThe cell is not free. Choose a free cell.', end='')


class TicTacGame:

    def __init__(self, players):
        self.players = players
        self.game_counter = 0
        self.__encoding = '123456789ox'

    def _reset_game(self):
        self.field = np.array(
            [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8]])
        self.turn_counter = 0

    def start_game(self):
        self._reset_game()
        for self.turn_counter in range(9):
            turn = (self.turn_counter + self.game_counter % 2) % 2
            self.__show_board(turn)
            self.players[turn].make_turn(self.field)
            if self._check_winning(self.players[turn]):
                self.players[turn].score += 1
                self.__show_board()
                self.__win_message(turn)
                break
        else:
            print("\nIT'S A MATCH!")
            self.__show_board()

        self.game_counter += 1

    def _check_winning(self, player):
        def three_a_row(x, y):
            return np.sum(x == y) == 3

        for i in range(3):
            if three_a_row(self.field[i, :], player.value):
                return True
            if three_a_row(self.field[:, i], player.value):
                return True
        if (three_a_row(self.field.diagonal(), player.value) or 
                three_a_row(np.fliplr(self.field).diagonal(), player.value)):
            return True
        else:
            return False

    def __win_message(self, turn):
        print(str(self.players[turn].name).upper() + ' WON!')
        print('\nXXX {player1} {score1}:{score2} {player2} OOO'
              .format(player1=self.players[0].name,
                      player2=self.players[1].name,
                      score1=self.players[0].score,
                      score2=self.players[1].score))

    def __show_board(self, turn=None):
        if turn is not None:
            char = 'X' if turn == 0 else 'O'
            print(f"\n{char*3} {self.players[turn].name}'s turn {char*3}")

        for r in range(3)[::-1]:
            row = self.field[r]
            encoded = list(map(lambda x: self.__encoding[x], row))
            print(f'[ {encoded[0]} | {encoded[1]} | {encoded[2]} ]')


if __name__ == '__main__':
    TicTac().run()
