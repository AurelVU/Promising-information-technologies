# from copy import deepcopy
# from typing import List, Tuple
#
# import numpy as np
#
# import random
#
#
# class GameTable:
#     def __init__(self, width, height, len_win):
#         self.points = [[]] * width
#         self.width = width
#         self.height = height
#         self.len_win = len_win
#
#     def is_move_available(self, line_index: int) -> bool:
#
#         if len(self.points[line_index]) < self.height:
#             return True
#         else:
#             return False
#
#     def get_available_move(self) -> List[int]:
#         """
#         array_posibility_move = []
#         for i in range(self.width):
#             if self.check_posibility_move(i):
#                 array_posibility_move.append(i)
#         return array_posibility_move
#         """
#         return [i for i in range(self.width) if self.is_move_available(i)]
#
#     def make_move(self, line_index, player):
#         self.points[line_index].append(player)
#
#     def check_horizontal(self, player):
#         for i in range(self.width):
#             count = 0
#             for j in range(len(self.points[i])):
#                 if self.points[i][j] == player:
#                     count += 1
#                 else:
#                     count = 0
#                 if count == self.len_win:
#                     return True
#         return False
#
#     def check_vertical(self, player):
#         for i in range(self.height):
#             count = 0
#             for j in range(self.width):
#                 if len(self.points[j]) > i:
#                     if self.points[j][i] == player:
#                         count += 1
#                     else:
#                         count = 0
#                 else:
#                     count = 0
#                 if count == self.len_win:
#                     return True
#         return False
#
#     def check_diagonal(self, player):
#         for i in range(self.width):
#             for j in range(self.height):
#                 count = 0
#                 for k in range(self.len_win):
#                     if (i + k >= self.width) or (j + k >= self.height):
#                         break
#                     if len(self.points[i + k]) > j + k:
#                         if self.points[i + k][j + k] == player:
#                             count += 1
#                         else:
#                             count = 0
#                     else:
#                         count = 0
#                     if count == self.len_win:
#                         return True
#         for i in range(self.width):
#             for j in range(self.height):
#                 count = 0
#                 for k in range(self.len_win):
#                     if (i + k >= self.width) or (j - k < 0):
#                         break
#                     if len(self.points[i + k]) > j - k:
#                         if self.points[i + k][j - k] == player:
#                             count += 1
#                         else:
#                             count = 0
#                     else:
#                         count = 0
#                     if count == self.len_win:
#                         return True
#         return False
#
#     def check_win(self, player):
#         if self.check_horizontal(player) or self.check_vertical(player) or self.check_diagonal(player):
#             return True
#         else:
#             return False
#
#     def check_finish(self):
#         for i in range(self.width):
#             if self.is_move_available(i):
#                 return False
#         return True
#
#     def print_table(self):
#         for h in range(self.height - 1, -1, -1):
#             for w in range(self.width):
#                 if len(self.points[w]) > h:
#                     print(self.points[w][h], end=' ')
#                 else:
#                     print('_', end=' ')
#             print('\n')
#         for i in range(self.width):
#             print(i, end=' ')
#         print('\n')
#
#     def check_game_over(self):
#         for player_index in range(1, 3):
#             if self.check_win(player_index):
#                 print(f'Player {player_index} win')
#                 return True
#         if self.check_finish():
#             print('Draw')
#             return True
#         else:
#             return False
#
#     def game_table_to_tuples(self) -> Tuple[tuple, ...]:
#         return tuple([tuple(i) for i in self.points])
#
#     def is_win_guaranteed(self, player, num_our_player, deep_force):
#         if self.check_win(num_our_player):
#             return True,
#         if self.check_win(3 - num_our_player) or self.check_finish():
#             return False
#         if deep_force == 0:
#             return False
#         if player == num_our_player:
#             for i in self.get_available_move():
#                 self.make_move(i, player)
#                 flag = True
#                 for j in self.get_available_move():
#                     self.make_move(j, 3 - player)
#                     if not self.is_win_guaranteed(player, num_our_player, deep_force - 1):
#                         flag = False
#                         self.points[j].pop()
#                         break
#                     self.points[j].pop()
#                 if flag:
#                     self.points[i].pop()
#                     return True
#                 self.points[i].pop()
#             return False
#         else:
#             flag = True
#             for i in self.get_available_move():
#                 self.make_move(i, player)
#                 if self.is_win_guaranteed(3 - player, num_our_player, deep_force):
#                     self.points[i].pop()
#                 else:
#                     self.points[i].pop()
#                     flag = False
#                     break
#             return flag
#
#
# class Node:
#     def __init__(self, game_table, player):
#         self.game_table = game_table
#         self.player = player
#         self.children = []
#         self.number_win = 0
#         self.number_draw = 0
#         self.number_loss = 0
#
#
# class GameTree:
#     def __init__(self,
#                  width,
#                  height,
#                  len_win,
#                  num_our_player,
#                  deep_force=1,
#                  num_samples=50,
#                  seed=42,
#                  play_only_necessary_playout=True
#                  ):
#         self.curr_node = Node(GameTable(width, height, len_win), 1)
#         self.num_our_player = num_our_player
#         self.num_enemy_player = 3 - num_our_player
#         self.width = width
#         self.height = height
#         self.len_win = len_win
#         self.dict_pos = {}
#         self.deep_force = deep_force  # глубина перебора для семплирования
#         self.num_samples = num_samples  # количество семплирований
#         self.play_only_necessary_playout = play_only_necessary_playout
#         random.seed(seed)
#
#     def init_children_node(self, node):
#         for it in node.game_table.get_available_move():
#             if not it < len(node.children) or not node.children[it]:
#                 temp_table = deepcopy(node.game_table)
#                 temp_table.make_move(it, node.player)
#                 temp_tuple = temp_table.game_table_to_tuples()
#                 temp_node = self.dict_pos.get(temp_tuple)
#                 if not temp_node:
#                     node.children.insert(it, Node(temp_table, 3 - node.player))
#                     self.dict_pos[temp_tuple] = node.children[it]
#                 else:
#                     node.children.insert(it, temp_node)
#
#     def make_move(self, line_index):
#         self.init_children_node(self.curr_node)
#         self.curr_node = self.curr_node.children[line_index]
#
#     def emulate_game(self, node: Node):
#         # 1 - win our player
#         # 0 - draw
#         # -1 - win enemy player
#
#         # База рекурсии
#         if node.game_table.check_win(self.num_our_player):
#             return 1
#         if node.game_table.check_win(self.num_enemy_player):
#             return -1
#         if node.game_table.check_finish():
#             return 0
#
#         self.init_children_node(node)
#
#         pos_move = node.game_table.get_available_move()
#
#         if node.player != self.num_our_player:
#             if node.game_table.is_win_guaranteed(node.player, self.num_enemy_player, 1):
#                 return -1
#             elif node.game_table.is_win_guaranteed(node.player, self.num_our_player, self.deep_force):
#                 return 1
#
#             rand_move = random.choice(pos_move)
#             ans = self.emulate_game(node.children[rand_move])
#             if ans == -1:
#                 node.number_loss += 1
#             if ans == 0:
#                 node.number_draw += 1
#             if ans == 1:
#                 node.number_win += 1
#             return ans
#
#     @staticmethod
#     def _get_index(node, samples):
#         all_sum = node.number_draw + node.number_loss + node.number_win
#         if all_sum == 0:
#             return 0
#         result_sum = (node.number_win + node.number_draw / 2) / all_sum
#         result_sum += np.sqrt(2 * np.log(samples) / all_sum)
#         return result_sum
#
#     def get_best_move(self):
#         for it in range(self.num_samples):
#             self.emulate_game(self.curr_node)
#
#         pos_move = self.curr_node.game_table.get_available_move()
#         all_samples = 0
#
#         for it in pos_move:
#             all_samples += self.curr_node.children[it].number_draw + \
#                            self.curr_node.children[it].number_loss + \
#                            self.curr_node.children[it].number_win
#
#         first_node = self.curr_node.children[pos_move[0]]
#         max_index = self._get_index(first_node, all_samples)
#         best_move = pos_move[0]
#         for it in pos_move:
#             if self.curr_node.children[it].game_table.is_win_guaranteed(self.curr_node.children[it].player,
#                                                                         self.num_our_player, 1):
#                 return it
#             if self._get_index(self.curr_node.children[it], all_samples) > max_index:
#                 max_index = self._get_index(self.curr_node.children[it], all_samples)
#                 best_move = it
#         return best_move
#
#
# if __name__ == '__main__':
#     width_point = 7
#     height_point = 6
#     line_length_to_win = 4
#
#     num_bot_player = 1
#     cur_player = 1
#
#     game_tree = GameTree(width_point, height_point, line_length_to_win, num_bot_player, num_samples=200)
#
#     while True:
#         game_tree.curr_node.game_table.print_table()
#
#         temp = game_tree.curr_node.game_table.check_game_over()
#         if temp:
#             break
#
#         if cur_player != num_bot_player:
#             num_line = int(input())
#             if num_line in game_tree.curr_node.game_table.get_available_move():
#                 game_tree.make_move(num_line)
#                 cur_player = 3 - cur_player
#             else:
#                 print("Error")
#                 break
#
#         else:
#             print("Bot move")
#             final_best_move = game_tree.get_best_move()
#             game_tree.make_move(final_best_move)
#             cur_player = 3 - cur_player
