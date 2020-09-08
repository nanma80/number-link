#!/usr/bin/env python3

import sys
import csv
import datetime

from board import *

class Solver(object):
    def __init__(self, filename):
        self.board = Board(self.import_csv(filename))

    def pad_board(self, input_board):
        board = [[PLACEHOLDER] + row + [PLACEHOLDER] for row in input_board ]
        board = [[PLACEHOLDER] * len(board[0])] + board + [[PLACEHOLDER] * len(board[0])]
        return board

    def import_csv(self, filename):
        with open(filename) as csv_file:
            input_board = []
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                input_board.append([int(element) for element in row])
        return self.pad_board(input_board)

    def solve(self):
        print('Board loaded:')
        self.board.print()
        self.queued_boards = set()
        self.boards_to_process = []
        self.queued_boards.add(self.board.to_string())
        self.boards_to_process.append(self.board)
        print('Solving...')

        loop_count = 0
        while len(self.boards_to_process) > 0:
            loop_count += 1

            current_board = self.boards_to_process.pop()

            if loop_count % 1000 == 0:
                print()
                current_board.print()
                print(f'{datetime.datetime.now()}\t{loop_count}\tstack: {len(self.boards_to_process)}\tset: {len(self.queued_boards)}\tleft: {len(current_board.pieces)}\tmoves: {len(current_board.history_moves)}')

            if current_board.is_solved():
                print('Solved!\n')
                current_board.print_history()
                return

            if len(current_board.valid_moves) == 0:
                continue

            for move in reversed(current_board.valid_moves):
                new_board = current_board.apply_move(move)
                if new_board.to_string() in self.queued_boards:
                    continue
                self.queued_boards.add(new_board.to_string())
                if new_board.is_solved():
                    print('Solved!\n')
                    new_board.print_history()
                    return
                if len(new_board.valid_moves) == 0:
                    continue
                if new_board.is_skewed():
                    continue
                self.boards_to_process.append(new_board)
            self.boards_to_process.sort(key=lambda x: -len(x.pieces))
        print('Unsolvable')
