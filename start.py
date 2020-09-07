#!/usr/bin/env python3

import sys

sys.path.append('lib')
from board import *
from solver import *

def main():
    if len(sys.argv) == 1:
        print('Please run start.py input_csv_file.csv')
        return

    csv_filename = sys.argv[1]
    solver = Solver(csv_filename)
    if not solver.board.is_valid():
        print('Board is invalid')
        return
    solver.solve()

if __name__ == "__main__":
    main()
