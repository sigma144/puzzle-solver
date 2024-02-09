from solver import GridSolver, NumberGridState
from math import sqrt

class FutoshikiSolver(GridSolver):
    def solve(self, puzzle):
        if puzzle[-1] == ",":
            puzzle = puzzle[:-1]
        grid_values = puzzle.split(",")
        width = height = int(sqrt(len(grid_values)))
        state = NumberGridState([[0 for x in range(width)] for y in range(height)], 0, 0)
        self.less = [[[] for x in range(width)] for y in range(height)]
        self.greater = [[[] for x in range(width)] for y in range(height)]
        for i, num in enumerate(grid_values):
            x, y = i % width, i // height
            state.grid[y][x] = int(num[0])
            if len(num) > 1:
                for char in num[1:]:
                    dir = {"U":(0, -1), "D":(0, 1), "L":(-1, 0), "R":(1, 0)}[char]
                    self.greater[y][x].append((x + dir[0], y + dir[1]))
                    self.less[y + dir[1]][x + dir[0]].append((x, y))
        self.solve_recursive(state)

    def get_next_states(self, state):
        states = []
        for i in range(len(state.grid)):
            if i + 1 not in self.get_row(state, state.y) and i + 1 not in self.get_column(state, state.x):
                new_state = NumberGridState(state.grid, state.x, state.y)
                new_state.set(state.x, state.y, i + 1)
                states.append(new_state)
        return states

    def check_state(self, state):
        num = state.grid[state.y][state.x]
        less_dir = self.less[state.y][state.x]
        if len(less_dir) > 0 and num == len(state.grid):
            return False
        greater_dir = self.greater[state.y][state.x]
        if len(greater_dir) > 0 and num == 1:
            return False

        for x2, y2 in less_dir:
            num2 = state.grid[y2][x2]
            if num2 > 0 and num2 < num:
                return False
        for x2, y2 in greater_dir:
            num2 = state.grid[y2][x2]
            if num2 > 0 and num2 > num:
                return False
                
        for y in range(len(state.grid)):
            if state.grid[y][state.x] == 0:
                for x2, y2 in self.less[y][state.x]:
                    num2 = state.grid[y2][x2]
                    if num2 == 0:
                        continue
                    row, column = self.get_row(state, y), self.get_column(state, state.x)
                    for i in range(0, num2): 
                        if i not in row and i not in column:
                            break
                    else:
                        return False
                for x2, y2 in self.greater[y][state.x]:
                    num2 = state.grid[y2][x2]
                    if num2 == 0:
                        continue
                    row, column = self.get_row(state, y), self.get_column(state, state.x)
                    for i in range(num2 + 1, len(state.grid) + 1):
                        if i not in row and i not in column:
                            break
                    else:
                        return False
        for x in range(len(state.grid)):
            if state.grid[state.y][x] == 0:
                for x2, y2 in self.less[state.y][x]:
                    num2 = state.grid[y2][x2]
                    if num2 == 0:
                        continue
                    row, column = self.get_row(state, state.y), self.get_column(state, x)
                    for i in range(0, num2): 
                        if i not in row and i not in column:
                            break
                    else:
                        return False
                for x2, y2 in self.greater[state.y][x]:
                    num2 = state.grid[y2][x2]
                    if num2 == 0:
                        continue
                    row, column = self.get_row(state, state.y), self.get_column(state, x)
                    for i in range(num2 + 1, len(state.grid) + 1):
                        if i not in row and i not in column:
                            break
                    else:
                        return False
        return True

puzzle_easy = '0R,0R,0R,0,0D,0,0,0,0,0,0,0U,0D,0,0,0,0,0L,0,3U,0U,0,0,0R,0,'
#5x5 Hard Futoshiki Puzzle ID: 7,818,562

puzzle_medium = '0,0,2,0,0L,0R,0,0U,0R,0,0,0,0,0,0,0,5RD,0,0,0U,0,0,0L,0,0,0,0,0,0,3,4,0,0,0,0,0,0,0L,5UL,0U,6R,0,0,6,0,2,0R,0R,0,'
#7x7 Hard Futoshiki Puzzle ID: 2,470,060

puzzle_hard = '2R,0,0,0,0,0,0,0,4L,0,0L,9,0D,0,0D,0,0,0U,0,0,0,0,0,0,0,0L,0,7UD,0L,0UD,0,0,0L,0,0,0U,0,0,0,0U,7L,0,0,2,0D,0R,0R,0D,0,0,0R,0,0,0L,6D,0,0D,2U,0L,0U,0D,9,0,0,0D,0R,0,0,0,0L,6,0L,0,0,0U,0,0,0,0,0,0,'
#9x9 Hard Futoshiki Puzzle ID: 279,528

FutoshikiSolver().solve(puzzle_medium)