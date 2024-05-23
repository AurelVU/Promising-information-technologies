import time
from copy import deepcopy
import random
from multiprocessing import Pool
from typing import List, Tuple, Union

import numpy as np

NUM_PROCESS = 10


class GameTable:
    def __init__(self, width, height, len_win):
        self.array_points = [[] for _ in range(width)]
        self.width = width
        self.height = height
        self.len_win = len_win

    def is_move_possibility(self, line_index):
        if len(self.array_points[line_index]) < self.height:
            return True
        else:
            return False

    def get_possibility_move(self) -> List:
        return [i for i in range(self.width) if self.is_move_possibility(i)]

    def make_move(self, line_index, player):
        self.array_points[line_index].append(player)

    def check_horizontal(self, player):
        for i in range(self.width):
            count = 0
            for j in range(len(self.array_points[i])):
                if self.array_points[i][j] == player:
                    count += 1
                else:
                    count = 0
                if count == self.len_win:
                    return True
        return False

    def check_vertical(self, player):
        for i in range(self.height):
            count = 0
            for j in range(self.width):
                if len(self.array_points[j]) > i:
                    if self.array_points[j][i] == player:
                        count += 1
                    else:
                        count = 0
                else:
                    count = 0
                if count == self.len_win:
                    return True
        return False

    def check_diagonal(self, player):
        for i in range(self.width):
            for j in range(self.height):
                count = 0
                for k in range(self.len_win):
                    if (i + k >= self.width) or (j + k >= self.height):
                        break
                    if len(self.array_points[i + k]) > j + k:
                        if self.array_points[i + k][j + k] == player:
                            count += 1
                        else:
                            count = 0
                    else:
                        count = 0
                    if count == self.len_win:
                        return True
        for i in range(self.width):
            for j in range(self.height):
                count = 0
                for k in range(self.len_win):
                    if (i + k >= self.width) or (j - k < 0):
                        break
                    if len(self.array_points[i + k]) > j - k:
                        if self.array_points[i + k][j - k] == player:
                            count += 1
                        else:
                            count = 0
                    else:
                        count = 0
                    if count == self.len_win:
                        return True

    def check_win(self, player):
        if self.check_horizontal(player) or self.check_vertical(player) or self.check_diagonal(player):
            return True
        else:
            return False

    def check_finish(self):
        for i in range(self.width):
            if self.is_move_possibility(i):
                return False
        return True

    def print_table(self):
        for h in range(self.height - 1, -1, -1):
            for w in range(self.width):
                if len(self.array_points[w]) > h:
                    print(self.array_points[w][h], end=' ')
                else:
                    print('_', end=' ')
            print('\n')
        for i in range(self.width):
            print(i, end=' ')
        print('\n')

    def is_game_over(self):
        for player in range(1, 3):
            if self.check_win(player):
                print('Player', player, 'win')
                return True
        if self.check_finish():
            print('Draw')
            return True
        else:
            return False

    def game_table_to_tuples(self):
        return tuple([tuple(i) for i in self.array_points])

    def is_win_guaranteed(self, player, num_our_player, deep_force):
        if self.check_win(num_our_player):
            return True,
        if self.check_win(3 - num_our_player) or self.check_finish():
            return False
        if deep_force == 0:
            return False
        if player == num_our_player:
            for i in self.get_possibility_move():
                self.make_move(i, player)
                flag = True
                for j in self.get_possibility_move():
                    self.make_move(j, 3 - player)
                    if not self.is_win_guaranteed(player, num_our_player, deep_force - 1):
                        flag = False
                        self.array_points[j].pop()
                        break
                    self.array_points[j].pop()
                if flag:
                    self.array_points[i].pop()
                    return True
                self.array_points[i].pop()
            return False
        else:
            flag = True
            for i in self.get_possibility_move():
                self.make_move(i, player)
                if self.is_win_guaranteed(3 - player, num_our_player, deep_force):
                    self.array_points[i].pop()
                else:
                    self.array_points[i].pop()
                    flag = False
                    break
            return flag


class Node:
    def __init__(self, game_table, player):
        self.game_table = game_table
        self.player = player
        self.children: List[Union[None, Node]] = [None] * game_table.width
        self.number_win = 0
        self.number_draw = 0
        self.number_loss = 0


class GameTree:
    def __init__(self,
                 width,
                 height,
                 len_win,
                 num_our_player,
                 deep_force=1,
                 num_playout=50,
                 seed=42,
                 play_only_necessary_playout=True):
        self.current_node = Node(GameTable(width, height, len_win), 1)
        self.num_our_player = num_our_player
        self.num_enemy_player = 3 - num_our_player
        self.width = width
        self.height = height
        self.len_win = len_win
        self.dict_pos = {}
        self.deep_force = deep_force  # глубина перебора для семплирования
        self.num_playout = num_playout  # количество семплирований
        self.play_only_necessary_playout = play_only_necessary_playout
        random.seed(seed)

    def init_children_node(self, node):
        for it in node.game_table.get_possibility_move():
            if not node.children[it]:
                temp_table = deepcopy(node.game_table)
                temp_table.make_move(it, node.player)
                temp_tuple = temp_table.game_table_to_tuples()
                temp_node = self.dict_pos.get(temp_tuple)
                if not temp_node:
                    node.children[it] = Node(temp_table, 3 - node.player)
                    self.dict_pos[temp_tuple] = node.children[it]
                else:
                    node.children[it] = temp_node

    def make_move(self, line_index):
        self.init_children_node(self.current_node)
        self.current_node = self.current_node.children[line_index]

    def emulate_game(self, node):
        # 1 - win our player
        # 0 - draw
        # -1 - win enemy player

        # База рекурсии
        if node.game_table.check_win(self.num_our_player):
            return 1
        if node.game_table.check_win(self.num_enemy_player):
            return -1
        if node.game_table.check_finish():
            return 0

        self.init_children_node(node)

        pos_move = node.game_table.get_possibility_move()

        if node.player != self.num_our_player:
            if node.game_table.is_win_guaranteed(node.player, self.num_enemy_player, 1):
                return -1
        else:
            if node.game_table.is_win_guaranteed(node.player, self.num_our_player, self.deep_force):
                return 1

        rand_move = random.choice(pos_move)
        ans = self.emulate_game(node.children[rand_move])
        if ans == -1:
            node.number_loss += 1
        if ans == 0:
            node.number_draw += 1
        if ans == 1:
            node.number_win += 1
        return ans,

    @staticmethod
    def _get_index(node, all_samples):
        all_sum = node.number_draw + node.number_loss + node.number_win
        if all_sum == 0:
            return 0
        result = (node.number_win + node.number_draw / 2) / all_sum
        result += np.sqrt(2 * np.log(all_samples) / all_sum)
        return result

    def _emulate_game_multiproc(self, c: Tuple[Union[Node, int]]) -> List[int]:
        return [self.emulate_game(c[0]) for _ in range(c[1])]

    def get_best_move(self):
        t = time.time()
        self.init_children_node(self.current_node)
        with Pool(NUM_PROCESS) as p:
            p.map(
                self._emulate_game_multiproc,
                [
                    tuple([self.current_node, int((self.num_playout + NUM_PROCESS - 1) / NUM_PROCESS)])
                ] * NUM_PROCESS
            )

        pos_move = self.current_node.game_table.get_possibility_move()
        all_samples = 0
        for it in pos_move:
            all_samples += self.current_node.children[it].number_draw + \
                           self.current_node.children[it].number_loss + \
                           self.current_node.children[it].number_win

        first_node = self.current_node.children[pos_move[0]]
        max_index = self._get_index(first_node, all_samples)
        best_move = pos_move[0]
        for it in pos_move:
            if self.current_node.children[it].game_table.is_win_guaranteed(self.current_node.children[it].player,
                                                                           self.num_our_player, 1):
                return it
            if self._get_index(self.current_node.children[it], all_samples) > max_index:
                max_index = self._get_index(self.current_node.children[it], all_samples)
                best_move = it
        print(f'GET BEST MOVE {time.time() - t}')
        return best_move


if __name__ == '__main__':
    width_point = 7
    height_point = 6
    line_length_to_win = 4

    num_bot_player = 1
    cur_player = 1

    game_tree = GameTree(width_point, height_point, line_length_to_win, num_bot_player, num_playout=200)

    while True:

        game_tree.current_node.game_table.print_table()

        temp = game_tree.current_node.game_table.is_game_over()
        if temp:
            break

        if cur_player != num_bot_player:
            inp_line_index = int(input())
            if inp_line_index in game_tree.current_node.game_table.get_possibility_move():
                game_tree.make_move(inp_line_index)
                cur_player = 3 - cur_player
            else:
                print("Error")
                break

        else:
            print("Bot move")
            final_best_move = game_tree.get_best_move()
            game_tree.make_move(final_best_move)
            cur_player = 3 - cur_player
