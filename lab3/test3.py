# import time
# from copy import deepcopy
# import random
# import numpy as np
#
#
# class GameTable:
#     def __init__(self, width_point, height_point, line_length_to_win):
#         self.array_points = [[] for i in range(width_point)]
#         self.width = width_point
#         self.height = height_point
#         self.len_win = line_length_to_win
#
#     def check_posibility_move(self, num_line):
#
#         if len(self.array_points[num_line]) < self.height:
#             return True
#         else:
#             return False
#
#     def get_array_posibility_move(self):
#         """
#         array_posibility_move = []
#         for i in range(self.width):
#             if self.check_posibility_move(i):
#                 array_posibility_move.append(i)
#         return array_posibility_move
#         """
#         return [i for i in range(self.width) if self.check_posibility_move(i)]
#
#     def make_move(self, num_line, player):
#         self.array_points[num_line].append(player)
#
#     def check_horizontal(self, player):
#         for i in range(self.width):
#             count = 0
#             for j in range(len(self.array_points[i])):
#                 if self.array_points[i][j] == player:
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
#                 if len(self.array_points[j]) > i:
#                     if self.array_points[j][i] == player:
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
#                     if len(self.array_points[i + k]) > j + k:
#                         if self.array_points[i + k][j + k] == player:
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
#                     if len(self.array_points[i + k]) > j - k:
#                         if self.array_points[i + k][j - k] == player:
#                             count += 1
#                         else:
#                             count = 0
#                     else:
#                         count = 0
#                     if count == self.len_win:
#                         return True
#
#     def check_win(self, player):
#         if self.check_horizontal(player) or self.check_vertical(player) or self.check_diagonal(player):
#             return True
#         else:
#             return False
#
#     def check_finish(self):
#         for i in range(self.width):
#             if self.check_posibility_move(i):
#                 return False
#         return True
#
#     def print_table(self):
#         for h in range(self.height - 1, -1, -1):
#             for w in range(self.width):
#                 if len(self.array_points[w]) > h:
#                     print(self.array_points[w][h], end=' ')
#                 else:
#                     print('_', end=' ')
#             print('\n')
#         for i in range(self.width):
#             print(i, end=' ')
#         print('\n')
#
#     def check_game_over(self):
#         for player in range(1, 3):
#             if self.check_win(player):
#                 print('Player', player, 'win')
#                 return True
#         if self.check_finish():
#             print('Draw')
#             return True
#         else:
#             return False
#
#     def get_GameTable_to_tuples(self):
#         return tuple([tuple(i) for i in self.array_points])
#
#     def check_garented_win(self, player, num_our_player, deep_force):
#         if self.check_win(num_our_player):
#             return True,
#         if self.check_win(3 - num_our_player) or self.check_finish():
#             return False
#         if deep_force == 0:
#             return False
#         if player == num_our_player:
#             for i in self.get_array_posibility_move():
#                 self.make_move(i, player)
#                 flag = True
#                 for j in self.get_array_posibility_move():
#                     self.make_move(j, 3 - player)
#                     if not self.check_garented_win(player, num_our_player, deep_force - 1):
#                         flag = False
#                         self.array_points[j].pop()
#                         break
#                     self.array_points[j].pop()
#                 if flag:
#                     self.array_points[i].pop()
#                     return True
#                 self.array_points[i].pop()
#             return False
#         else:
#             flag = True
#             for i in self.get_array_posibility_move():
#                 self.make_move(i, player)
#                 if self.check_garented_win(3 - player, num_our_player, deep_force):
#                     self.array_points[i].pop()
#                 else:
#                     self.array_points[i].pop()
#                     flag = False
#                     break
#             return flag
#
#
# class Node:
#     def __init__(self, game_table, player):
#         self.game_table = game_table
#         self.player = player
#         self.childrens = [None for i in range(game_table.width)]
#         self.number_win = 0
#         self.number_draw = 0
#         self.number_loss = 0
#
#
# class GameTree:
#     def __init__(self, width_point, height_point, line_length_to_win, num_our_player, deep_force=1,
#                  num_playout=50, seed=42, play_only_nesasery_playout=True):
#         self.curr_Node = Node(GameTable(width_point, height_point, line_length_to_win), 1)
#         self.num_our_player = num_our_player
#         self.num_enemy_player = 3 - num_our_player
#         self.width = width_point
#         self.height = height_point
#         self.len_win = line_length_to_win
#         self.dict_pos = {}
#         self.deep_force = deep_force  # глубина перебора для семплирования
#         self.num_playout = num_playout  # количество семплирований
#         self.play_only_nesasery_playout = play_only_nesasery_playout
#         random.seed(seed)
#
#     def init_childs_Node(self, Nodee):
#         for it in Nodee.game_table.get_array_posibility_move():
#             if not Nodee.childrens[it]:
#                 temp_table = deepcopy(Nodee.game_table)
#                 temp_table.make_move(it, Nodee.player)
#                 temp_tuple = temp_table.get_GameTable_to_tuples()
#                 temp_Node = self.dict_pos.get(temp_tuple)
#                 if not temp_Node:
#                     Nodee.childrens[it] = Node(temp_table, 3 - Nodee.player)
#                     self.dict_pos[temp_tuple] = Nodee.childrens[it]
#                 else:
#                     Nodee.childrens[it] = temp_Node
#
#     def make_move(self, num_line):
#         self.init_childs_Node(self.curr_Node)
#         self.curr_Node = self.curr_Node.childrens[num_line]
#
#     def emulate_game(self, cur_Node):
#         # 1 - win our player
#         # 0 - draw
#         # -1 - win enemy player
#
#         # База рекурсии
#         if cur_Node.game_table.check_win(self.num_our_player):
#             return 1
#         if cur_Node.game_table.check_win(self.num_enemy_player):
#             return -1
#         if cur_Node.game_table.check_finish():
#             return 0
#
#         self.init_childs_Node(cur_Node)
#
#         pos_move = cur_Node.game_table.get_array_posibility_move()
#
#         if cur_Node.player != self.num_our_player:
#             if cur_Node.game_table.check_garented_win(cur_Node.player, self.num_enemy_player, 1):
#                 return -1
#             rand_move = random.choice(pos_move)
#             ans = self.emulate_game(cur_Node.childrens[rand_move])
#             if ans == -1:
#                 cur_Node.number_loss += 1
#             if ans == 0:
#                 cur_Node.number_draw += 1
#             if ans == 1:
#                 cur_Node.number_win += 1
#             return ans
#
#         else:
#             if cur_Node.game_table.check_garented_win(cur_Node.player, self.num_our_player, self.deep_force):
#                 return 1
#             rand_move = random.choice(pos_move)
#             ans = self.emulate_game(cur_Node.childrens[rand_move])
#             if ans == -1:
#                 cur_Node.number_loss += 1
#             if ans == 0:
#                 cur_Node.number_draw += 1
#             if ans == 1:
#                 cur_Node.number_win += 1
#             return ans
#
#     def get_best_move(self):
#         t = time.time()
#         def get_index(Node, all_semplay):
#             all_sum = Node.number_draw + Node.number_loss + Node.number_win
#             if all_sum == 0:
#                 return 0
#             sum = (Node.number_win + Node.number_draw / 2) / all_sum
#             sum += np.sqrt(2 * np.log(all_semplay) / all_sum)
#             return sum
#
#         for it in range(self.num_playout):
#             self.emulate_game(self.curr_Node)
#         pos_move = self.curr_Node.game_table.get_array_posibility_move()
#         all_semplay = 0
#         for it in pos_move:
#             all_semplay += self.curr_Node.childrens[it].number_draw + self.curr_Node.childrens[it].number_loss + \
#                            self.curr_Node.childrens[it].number_win
#         first_Node = self.curr_Node.childrens[pos_move[0]]
#         max_index = get_index(first_Node, all_semplay)
#         best_move = pos_move[0]
#         for it in pos_move:
#             if self.curr_Node.childrens[it].game_table.check_garented_win(self.curr_Node.childrens[it].player,
#                                                                           self.num_our_player, 1):
#                 return it
#             if get_index(self.curr_Node.childrens[it], all_semplay) > max_index:
#                 max_index = get_index(self.curr_Node.childrens[it], all_semplay)
#                 best_move = it
#         print(f'GET BEST MOVE {time.time() - t}')
#         return best_move
#
#
# width_point = 7
# height_point = 6
# line_length_to_win = 4
#
# num_bot_player = 1
# cur_player = 1
#
# mainT = GameTree(width_point, height_point, line_length_to_win, num_bot_player, num_playout=200)
#
# while True:
#
#     mainT.curr_Node.game_table.print_table()
#
#     temp = mainT.curr_Node.game_table.check_game_over()
#     if temp:
#         break
#
#     if cur_player != num_bot_player:
#         num_line = int(input())
#         if num_line in mainT.curr_Node.game_table.get_array_posibility_move():
#             mainT.make_move(num_line)
#             cur_player = 3 - cur_player
#         else:
#             print("Error")
#             break
#
#     else:
#         print("Bot move")
#         best_move = mainT.get_best_move()
#         mainT.make_move(best_move)
#         cur_player = 3 - cur_player
#
