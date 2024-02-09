from solver import GridSolver, NumberGridState, DIRECTIONS
from math import sqrt

class RenzokuSolver(GridSolver):
    def solve(self, puzzle):
        if puzzle[-1] == ",":
            puzzle = puzzle[:-1]
        grid_values = puzzle.split(",")
        width = height = int(sqrt(len(grid_values)))
        state = NumberGridState([[0 for x in range(width)] for y in range(height)], 0, 0)
        self.adjacent = [[[] for x in range(width)] for y in range(height)]
        self.non_adjacent = [[[(x + dir[0], y + dir[1]) for dir in DIRECTIONS if state.on_grid(x + dir[0], y + dir[1])] for x in range(width)] for y in range(height)]
        for i, num in enumerate(grid_values):
            x, y = i % width, i // height
            state.grid[y][x] = int(num[0])
            if len(num) > 1:
                for char in num[1:]:
                    if char.isdigit():
                        state.grid[y][x] = int(char) + 10 * state.grid[y][x]
                        continue
                    dir = {"U":(0, -1), "D":(0, 1), "L":(-1, 0), "R":(1, 0)}[char]
                    self.adjacent[y][x].append((x + dir[0], y + dir[1]))
                    self.non_adjacent[y][x].remove((x + dir[0], y + dir[1]))
        self.solve_recursive(state)

    def get_next_states(self, state):
        states = []
        for i in range(len(state.grid)):
            if i + 1 not in self.get_row(state, state.y) and i + 1 not in self.get_column(state, state.x):
                new_state = NumberGridState(state.grid, state.x, state.y)
                new_state.set2(i + 1)
                states.append(new_state)
        return states

    def check_state(self, state):

        num = state.grid[state.y][state.x]
        adjacent = self.adjacent[state.y][state.x]
        non_adjacent = self.non_adjacent[state.y][state.x]

        for x2, y2 in adjacent:
            num2 = state.grid[y2][x2]
            if num2 > 0 and abs(num - num2) > 1:
                return False
        for x2, y2 in non_adjacent:
            num2 = state.grid[y2][x2]
            if num2 > 0 and abs(num - num2) == 1:
                return False

        for y in range(len(state.grid)):
            if state.grid[y][state.x] == 0:
                for x2, y2 in self.adjacent[y][state.x]:
                    num2 = state.grid[y2][x2]
                    if num2 == 0:
                        continue
                    row, column = self.get_row(state, y), self.get_column(state, state.x)
                    if (num2 + 1 in row or num2 + 1 in column) and (num2 - 1 in row or num2 - 1 in column):
                        return False
        for x in range(len(state.grid)):
            if state.grid[state.y][x] == 0:
                for x2, y2 in self.adjacent[state.y][x]:
                    num2 = state.grid[y2][x2]
                    if num2 == 0:
                        continue
                    row, column = self.get_row(state, state.y), self.get_column(state, x)
                    if (num2 + 1 in row or num2 + 1 in column) and (num2 - 1 in row or num2 - 1 in column):
                        return False

        return True
        
puzzle_easy = '3,0R,0DL,0R,0L,0RD,0RDL,0UL,0RD,0L,0UR,0UL,0R,0UDL,5,0D,0R,0RDL,0UDL,0,0UR,0L,0UR,0URL,0L,'
#ID: 518195

puzzle_medium = '0RD,0RL,0RDL,0DL,0,0R,0DL,0U,0,0UR,0UL,0,0D,0U,0,0R,0L,0R,0L,0U,7,5,0D,0,0RD,0DL,0D,0D,2D,0U,0R,0URL,0UDL,0U,0U,0U,0,0RD,0L,0UD,0RD,0DL,0,0R,0UL,0,0U,0UR,0UL,'
#ID: 3581143

puzzle_hard = '0D,0,0,0R,0L,0RD,0L,0,0D,0U,0D,0D,0R,0L,0U,0R,0L,0U,7,0U,0U,0,9,0R,0L,0R,0L,0,0,0R,0L,0D,0,0,0D,0,0R,0L,0,0D,0U,0,0,0UD,0,0R,0L,0,0UR,0L,0,0,0UR,0L,0,6,0R,0L,0,8,0,0,0,0R,0RL,0DL,6,1,0,0R,0L,0,6,0,0UR,0L,0,7,0,0,0,'
#ID: 4284402

puzzle_ultra = '0D,0,0D,0,2,0,0D,0,0,0,0,0,0R,0L,0D,0U,0D,0UD,0R,0L,0,0U,0D,0R,0L,0,0D,0D,0,0U,2,13UD,0U,0RD,0RL,0DL,1,0U,0RD,9DL,0,0U,0U,8,0,10,0UR,0DL,0U,0,3U,0,0D,0UR,0UDL,0D,0D,0D,0,0,0,0,0UR,0L,0,0R,0L,0U,0,0U,0U,0UR,0UL,0,0,0R,0L,0D,0,0,0D,0,0D,0RD,0L,0,0,0R,0L,0,0,0R,0UL,4,0D,0U,0,0UD,0U,0R,0L,0,0D,0R,0DL,0,15,0,12,0U,0,0,0U,1,0,9D,0,0U,14D,0U,11,6R,0L,0,12R,0L,0,0,0D,0D,0U,0,0D,0U,0,0,4D,0,0,3,9,0RD,0L,6U,0U,0,0,0U,13,0,0D,0U,0,13,0R,0DL,0U,0,0D,15R,0L,0,0,9D,0,0U,0,4,9,15,0U,14,0D,0U,0D,12,0,0D,0U,0,9,5,0,0,0D,12,4,0U,0,0U,2,0,0UD,0D,0D,0,0,0,0,0URD,0L,0,0,0,0,0,0D,0U,0U,0U,7,1,0,15,9U,0,3,13,0,10R,0L,0U,0,0,0,'

RenzokuSolver().solve(puzzle_hard)