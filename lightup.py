from solver import Solver, GridSolver, BinaryGridState, DIRECTIONS
LIGHT = -2
WALL = -3

class LightUpSolver(GridSolver):
    def solve(self, puzzle, width, height):
        state = BinaryGridState([[0 for x in range(width)] for y in range(height)], 0, 0)
        self.light_counts = [[-1 for x in range(width)] for y in range(height)]
        position = 0
        for char in puzzle:
            if char >= '0' and char <= '9':
                self.light_counts[position // height][position % width] = int(char)
                state.grid[position // height][position % width] = WALL
                position += 1
            elif char == "B":
                state.grid[position // height][position % width] = WALL
                position += 1
            else:
                position += ord(char) - ord('a') + 1
        self.solve_recursive(state)
    def get_next_states(self, state):
        states = []
        #Place light
        new_state = BinaryGridState(state.grid, state.x, state.y)
        new_state.set2(1)
        for dir in DIRECTIONS:
            x, y = state.x + dir[0], state.y + dir[1]
            while new_state.on_grid(x, y) and new_state.grid[y][x] != WALL:
                new_state.set(x, y, LIGHT)
                x += dir[0]
                y += dir[1]
        states.append(new_state)
        #Don't place light
        new_state = BinaryGridState(state.grid, state.x, state.y)
        new_state.set2(-1)
        states.append(new_state)
        return states
    def check_state(self, state):
        for y, row in enumerate(self.light_counts):
            for x, num in enumerate(row):
                if num != -1:
                    adjacent = [state.grid[y + dir[1]][x + dir[0]] for dir in DIRECTIONS if state.on_grid(y + dir[1], x + dir[0])]
                    total_light = adjacent.count(1)
                    if total_light > num:
                        return False
                    total_space = adjacent.count(-1) + adjacent.count(LIGHT) + adjacent.count(WALL)
                    if len(adjacent) - total_space < num:
                        return False
        return True
    def check_finish(self, state):
        for row in state.grid:
            if 0 in row or -1 in row:
                return False
        return True

puzzle_test = 'aBi0a2a2q1aBa3i1a'
#7x7 - ID: 7640459

puzzle_easy = 'a1e2cBfB11b1i0b01xB1b0i1b3B1fBc0eBa'
#10x10 - ID: 4477731 

puzzle_medium = 'aBe0a0bBa3bBa2gBb0aBd0aBfBg1aBa1e3aBBf1aBe2aBgBj2g0aBe3aBfB1aBeBaBa3g1f1aBdBaBbBgBa4b1aBb2aBeBa'
#14x14 - ID: 7790712

LightUpSolver().solve(puzzle_medium, 14, 14)