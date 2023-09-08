from solver import Solver, GridSolver, NumberGridState
from math import sqrt

class KillerSudokuSolver(GridSolver):
    def solve(self, puzzle):
        _, regions, grid_values = puzzle.split(";")
        width = height = int(sqrt(len(regions.split(","))))
        state = NumberGridState([[0 for x in range(width)] for y in range(height)], 0, 0)
        self.decode_regions(regions, width, height)
        self.region_totals = self.decode_grid_values(grid_values, width, height)
        for region in self.get_all_region_points():
            for x, y in region:
                self.region_totals[y][x] = max([self.region_totals[Y][X] for X,Y in region])
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
        #Check square
        for X in range(3):
            for Y in range(3):   
                if state.grid[y // 3 * 3 + Y][x // 3 * 3 + X] == num:
                    return False
        #Check region
        region = self.get_region(state, x, y)
        if num in region or sum(region) + num > self.region_totals[y][x] or 0 not in region and sum(region) + num != self.region_totals[y][x]:
            return False
        
        return True

puzzle_easy = 'zzzc;1,1,2,2,3,4,4,5,6,7,8,9,9,3,10,11,5,6,7,8,12,13,13,10,11,14,14,7,15,12,16,17,17,18,19,19,20,15,21,16,22,23,18,18,24,20,25,21,26,22,23,27,27,24,28,25,29,26,30,31,31,32,33,28,29,29,34,30,30,35,32,33,36,36,34,34,35,35,35,37,37;3a17a9_7a16_14_15_11_7b16_6d10_7c5b15a10_9a20_6a15a3a16_7b12a11a12b7b5a15a8_8a12_12c16b22b14f7a'

puzzle_hard = 'zzzc;1,2,2,3,3,4,5,6,7,1,8,9,9,10,4,5,6,7,11,8,12,12,10,13,14,14,7,11,15,16,16,13,13,17,18,18,19,15,20,21,22,22,17,23,18,19,15,20,21,24,25,26,23,27,19,28,20,29,24,25,26,23,27,28,28,28,29,30,30,31,32,32,33,33,29,29,34,34,31,32,32;9_10a13a6_12_5_13a9_15a14d6a11b16_15c15_12c5_15a21a11_6_7b16e10_14_10a11a12a21i10a12_21a15c7d'
#ID: 2867419

KillerSudokuSolver().solve(puzzle_easy)