#!/usr/bin/env python3

import math
from copy import copy, deepcopy
import colorama

PLACEHOLDER = 1
colorama.init()

class Board(object):
    def __init__(self, board):
        self.board = board
        self.height = len(self.board)
        self.width = len(self.board[0]) # assume the board is not empty
        self.history_boards = [ self.board ]
        self.history_moves = []
        self.build_neighbors()
        self.build_pieces()
        self.build_valid_moves()

    def is_valid(self):
        row_lengths = [len(row) for row in self.board]
        if min(row_lengths) != max(row_lengths):
            print('Board is not rectangular')
            return False

        product = 1
        for row in self.board:
            for element in row:
                product *= element

        x = product // 2
        seen = set([x])
        while x * x != product:
            x = (x + (product // x)) // 2
            if x in seen:
                print('Numbers cannot be all canceled out') 
                return False
            seen.add(x)
        return True

    def to_string(self):
        return str(self.board)

    def get_value(self, position):
        return self.board[position[0]][position[1]]


    def get_cached_neighbors(self, position):
        return self.neighbors[position[0]][position[1]]


    def get_neighbors(self, position):
        if self.get_value(position) == PLACEHOLDER:
            return []
        neighbors = [position]

        # up
        row_id = position[0] - 1
        column_id = position[1]
        while row_id >= 0 and row_id < self.height and self.get_value([row_id, column_id]) == PLACEHOLDER:
            neighbors.append([row_id, column_id])
            row_id -= 1

        # down
        row_id = position[0] + 1
        column_id = position[1]
        while row_id >= 0 and row_id < self.height and self.get_value([row_id, column_id]) == PLACEHOLDER:
            neighbors.append([row_id, column_id])
            row_id += 1

        # left
        row_id = position[0]
        column_id = position[1] - 1
        while column_id >= 0 and column_id < self.width and self.get_value([row_id, column_id]) == PLACEHOLDER:
            neighbors.append([row_id, column_id])
            column_id -= 1

        # right
        row_id = position[0]
        column_id = position[1] + 1
        while column_id >= 0 and column_id < self.width and self.get_value([row_id, column_id]) == PLACEHOLDER:
            neighbors.append([row_id, column_id])
            column_id += 1
        return neighbors

    def build_neighbors(self):
        self.neighbors = []
        for row_id in range(self.height):
            neighbors_row = []
            for column_id in range(self.width):
                neighbors_row.append(self.get_neighbors([row_id, column_id]))
            self.neighbors.append(neighbors_row)

    def connectible(self, position1, position2):
        neighbors1 = self.get_cached_neighbors(position1)
        neighbors2 = self.get_cached_neighbors(position2)
        for n1 in neighbors1:
            for n2 in neighbors2:
                if n1[0] == n2[0] and n1[1] == n2[1]:
                    return True

                if n1[0] == n2[0]: # n1[1] != n2[1]
                    (a, b) = (n1[1], n2[1])
                    if a > b:
                        (a, b) = (b, a)
                    empty_path = True
                    c = a + 1
                    while c < b:
                        if self.get_value([n1[0], c]) != PLACEHOLDER:
                            empty_path = False
                            break
                        c += 1
                    if empty_path:
                        return True

                if n1[1] == n2[1]: # n1[0] != n2[0]
                    (a, b) = (n1[0], n2[0])
                    if a > b:
                        (a, b) = (b, a)
                    empty_path = True
                    c = a + 1
                    while c < b:
                        if self.get_value([c, n1[1]]) != PLACEHOLDER:
                            empty_path = False
                            break
                        c += 1
                    if empty_path:
                        return True
        return False

    def cancellable(self, position1, position2):
        value1 = self.get_value(position1)
        value2 = self.get_value(position2)
        gcd = math.gcd(value1, value2)
        if gcd == 1:
            return False
        return self.connectible(position1, position2)

    def build_pieces(self):
        self.pieces = []
        for row_id in range(self.height):
            for column_id in range(self.width):
                position = [row_id, column_id]
                if self.get_value(position) != PLACEHOLDER:
                    self.pieces.append(position)

    def build_valid_moves(self):
        self.valid_moves = []
        for i in range(len(self.pieces)):
            for j in range(i + 1, len(self.pieces)):
                if self.cancellable(self.pieces[i], self.pieces[j]):
                    self.valid_moves.append([self.pieces[i], self.pieces[j]])

    def apply_move(self, move):
        if not self.cancellable(move[0], move[1]):
            raise Exception('moves are invalid')
        value1 = self.get_value(move[0])
        value2 = self.get_value(move[1])
        gcd = math.gcd(value1, value2)
        new_board = deepcopy(self.board)
        new_board[move[0][0]][move[0][1]] = int(value1/gcd)
        new_board[move[1][0]][move[1][1]] = int(value2/gcd)
        new_board_object = Board(new_board)

        history_moves = deepcopy(self.history_moves)
        history_moves.append(move)
        new_board_object.history_moves = history_moves

        history_boards = deepcopy(self.history_boards)
        history_boards.append(new_board)
        new_board_object.history_boards = history_boards

        return new_board_object

    def print(self):
        print(self.prettify(self.board, []))

    def prettify(self, board, highlighted_positions = []):
        highlighted_set = set()
        for position in highlighted_positions:
            highlighted_set.add(tuple(position))

        max_digits = len(str(max([max(r) for r in board])))
        rows_str = []
        for row_id in range(1, self.height - 1):
            row_str = ''
            elements_str = []
            for column_id in range(1, self.width - 1):
                element = board[row_id][column_id]
                if element == PLACEHOLDER:
                    element_str = ''
                else:
                    element_str = str(element)

                digits = len(element_str)

                if (row_id, column_id) in highlighted_set:
                    element_str = f'{colorama.Fore.GREEN}{element_str}{colorama.Style.RESET_ALL}'
                element_str = ' ' * (max_digits - digits) + element_str

                elements_str.append(element_str)
            
            row_str = '  '.join(elements_str)
            rows_str.append(row_str)
        
        board_str = '\n'.join(rows_str)
        return board_str

    def print_history(self):
        for i in range(len(self.history_moves)):
            if i > 0:
                print()
                input("Press Enter to continue...")
            board = self.history_boards[i]
            move = self.history_moves[i]
            print(self.prettify(board, move))


    def is_solved(self):
        return len(self.pieces) == 0