from solver import Solver, GridSolver, NumberGridState
from math import sqrt

class JigsawSudokuSolver(GridSolver):
    def solve(self, puzzle):
        grid_values, regions = puzzle.split(";")
        width = height = int(sqrt(len(regions.split(","))))
        state = NumberGridState([[0 for x in range(width)] for y in range(height)], 0, 0)
        self.decode_regions(regions, width, height)
        state.grid = self.decode_grid_values(grid_values, width, height)
        self.solve_recursive(state)
    def get_next_states(self, state):
        states = []
        for i in range(len(state.grid)):
            if self.can_place(state, state.x, state.y, i + 1):
                new_state = NumberGridState(state.grid, state.x, state.y)
                new_state.set2(i + 1)
                states.append(new_state)
        return states
    def can_place(self, state, x, y, num):
        #Check row
        if num in state.grid[y]:
            return False
        #Check column
        for Y in range(len(state.grid[0])):
            if state.grid[Y][x] == num:
                return False
        #Check region
        for n in self.get_region(state, x, y):
            if n == num:
                return False
        return True

puzzle_easy = '3c1e4c2e5c3;1,2,2,3,3,1,4,2,3,3,1,4,2,2,3,1,4,5,5,5,1,4,4,5,5'
#ID: 3470939

puzzle_medium = 'b6e3c4_6_6a1o5a7_3_1c5e2b;1,2,2,2,3,3,3,1,1,1,2,2,3,3,1,4,1,4,2,3,3,1,4,4,4,2,5,5,4,4,6,6,6,5,5,6,6,6,6,5,5,5,7,7,7,7,7,7,7'
#ID: 5428968

puzzle_hard = 'b4d8_3_9c6d3a1h8a4d7c1c8d8a5h8a4d3c9_6_9d4b;1,1,2,2,2,3,3,3,3,1,1,4,4,2,3,3,5,3,1,1,4,4,2,2,3,5,5,1,1,4,4,4,2,3,5,5,6,1,4,4,2,2,5,5,5,6,6,6,6,7,8,8,5,8,6,6,7,7,7,8,8,8,8,6,7,7,7,8,8,9,9,9,6,7,7,9,9,9,9,9,9'
#ID: 865914

puzzle_ultra = 'c5d12_4f11_2_12a10d7a14a12a3_9b14b4_8c8h11_2b11a6e5a13b10a14b8_12c1a6_13b13_5a7_10a6a11_12_3d2_8_1a11a13_10a14_12b11_8a14c4_12b7a12b10a4e5a8b4_6h10c9_1b2b3_7a8a9a1d8a5_2_11f3_7d14c;1,1,1,1,2,2,2,2,3,3,3,3,3,3,1,1,1,1,2,2,2,3,3,3,4,3,3,3,1,1,1,2,2,2,2,4,4,3,4,4,5,3,1,1,6,6,6,7,2,2,4,4,4,5,5,5,6,1,6,6,7,7,2,4,4,5,5,5,8,8,6,6,6,6,7,7,7,7,4,5,5,8,8,8,9,9,6,7,7,7,10,4,4,5,5,5,8,8,9,9,6,6,6,7,10,10,4,10,5,8,8,8,9,9,11,7,7,7,11,10,10,10,5,12,8,8,9,9,11,11,11,11,11,10,10,10,10,12,12,8,9,9,9,11,11,11,11,10,12,10,12,12,12,8,9,13,13,11,13,11,11,10,12,12,12,14,12,12,9,13,13,13,13,13,13,13,13,14,14,14,12,12,9,13,13,13,14,14,14,14,14,14,14,14,14,14'

JigsawSudokuSolver().solve(puzzle_ultra)