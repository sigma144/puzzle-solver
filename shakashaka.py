from solver import Solver, GridSolver, DIRECTIONS

UP_LEFT = 'a'; UP_RIGHT = 'b'; DOWN_LEFT = 'c'; DOWN_RIGHT = 'd'; RECT = '+'; DIAMOND = '.' 
REPR = {'a':'/', 'b':'\\', 'c':'\\', 'd':'/', '+':' ', '.':' '}
CORNERS = {'a':{'a':1, 'b':1, 'c':1, 'd':-1}, 'b':{'a':1, 'b':1, 'c':-1, 'd':1}, 'c':{'a':1, 'b':-1, 'c':1, 'd':1}, 'd':{'a':-1, 'b':1, 'c':1, 'd':1}, '+':{'a':1, 'b':1, 'c':1, 'd':1}}

class ShakashakaState:
    def __init__(self, array, corners, x, y):
        self.grid = []
        for row in array:
            self.grid.append(row[:])
        self.corners = []
        for row in corners:
            self.corners.append(row[:])
        self.x = x; self.y = y; self.width = len(self.grid[0]); self.height = len(self.grid)
    def __repr__(self):
        string = ""
        for row in self.grid:
            for num in row:
                string += REPR[num] if num in REPR else num if num != 0 else "-"
                #string += ' '
            string += "\n"
        return string

class ShakashakaSolver(GridSolver):
    def solve(self, puzzle, width, height):
        starting_state = ShakashakaState([[0 for x in range(width)] for y in range(height)],
            [[1 if x == 0 or x == width or y == 0 or y == height else 0 for x in range(width+1)] for y in range(height+1)], 0, 0)
        position = 0
        for char in puzzle:
            if char >= '0' and char <= '9' or char == 'B':
                x, y = position % width, position // height
                starting_state.grid[y][x] = char
                starting_state.corners[y][x] = 1
                starting_state.corners[y][x+1] = 1
                starting_state.corners[y+1][x] = 1
                starting_state.corners[y+1][x+1] = 1
                position += 1
            else:
                position += ord(char) - ord('a') + 1
        self.solve_recursive(starting_state)
    def get_next_states(self, state):
        states = []
        if state.x > 0 and state.y > 0 and state.grid[state.y][state.x-1] == RECT and state.grid[state.y-1][state.x] == RECT and state.grid[state.y-1][state.x-1] == RECT:
            valid_moves = RECT
        else:
            valid_moves = 'abcd+.'
        for move in valid_moves:
            if self.can_place(state, state.x, state.y, move):
                new_state = ShakashakaState(state.grid, state.corners, state.x, state.y)
                new_state.grid[state.y][state.x] = move
                if move != DIAMOND:
                    new_state.corners[state.y+1][state.x] = CORNERS[move][DOWN_LEFT]
                    new_state.corners[state.y+1][state.x+1] = CORNERS[move][DOWN_RIGHT]
                else:
                    if new_state.corners[state.y+1][state.x] == 1 or new_state.corners[state.y][state.x+1] == 1:
                        new_state.corners[state.y+1][state.x+1] = -1
                    if state.x > 0 and state.grid[state.y][state.x-1] == DIAMOND:
                        new_state.corners[state.y+1][state.x] = -1
                states.append(new_state)
        return states
    def can_place(self, state, x, y, move):
        if move == RECT:
            if y > 0 and x < state.width - 1 and state.grid[y-1][x] == RECT and state.grid[y-1][x+1] == RECT and state.grid[y][x+1] != 0:
                return False
            total = 0
            if x > 0 and state.grid[y][x-1] == RECT:
                total += 1
            if y > 0 and state.grid[y-1][x] == RECT:
                total += 1
            if x > 0 and y > 0 and state.grid[y-1][x-1] == RECT:
                total += 1
            if total == 2:
                return False
        if move == DIAMOND:
            if state.corners[y][x] == 1 and state.corners[y][x+1] == 1 or state.corners[y][x+1] == 1 and state.corners[y+1][x+1] == 1 or \
                state.corners[y+1][x] == 1 and state.corners[y+1][x+1] == 1 or state.corners[y][x] == 1 and state.corners[y+1][x] == 1:
                return False
            if x > 0 and state.grid[y][x-1] == DIAMOND and state.corners[y][x] == 1:
                return False
            if y > 0 and state.grid[y-1][x] == DIAMOND and (state.corners[y][x] == 1 or state.corners[y][x+1] == 1):
                return False
        else:
            if state.corners[y][x] and CORNERS[move][UP_LEFT] != state.corners[y][x] or state.corners[y][x+1] and CORNERS[move][UP_RIGHT] != state.corners[y][x+1] or \
                state.corners[y+1][x] and CORNERS[move][DOWN_LEFT] != state.corners[y+1][x] or state.corners[y+1][x+1] and CORNERS[move][DOWN_RIGHT] != state.corners[y+1][x+1]:
                return False
        #Check triangle counts
        for dir in DIRECTIONS:
            if self.on_grid(state, y + dir[1], x + dir[0]) and not self.check_triangle_count(state, x + dir[0], y + dir[1], move in [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]):
                return False
        return True
    def check_triangle_count(self, state, x, y, add_tri):
        if state.grid[y][x] not in ['0', '1', '2', '3', '4']:
            return True
        count = ord(state.grid[y][x]) - ord('0')
        count_tri = 1 if add_tri else 0
        count_non = 0 if add_tri else 1
        for dir in DIRECTIONS:
            if self.on_grid(state, y + dir[1], x + dir[0]):
                val = state.grid[y + dir[1]][x + dir[0]]
                if val in [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]:
                    count_tri += 1
                elif val != 0:
                    count_non += 1
            else:
                count_non += 1
        if count_tri > count or count_non > (4 - count):
            return False
        return True

puzzle_easy = 'Bg2c3l4dBb2oBbBqBf2dBbBi0c2'
#10x10 - ID: 5398853

puzzle_medium = 'BaBc1bBaB1f2fBb2mB2b3b2f2bBm2b1b0eBdBhBbBiBc3cBBd3eBe3e4d2cBeBbBd4h4i4c2d2eBgBd2gBnBa2h3b4i4b4hBlBc4d4c1gBdBeBi2bBg2bBgBbBb4f3fBgBe2c0Bd3cB'
#20x20 - ID: 8694176

puzzle_hard = 'dBbBBbBcBaBd2cBbBBbBbBgBfBjBc1bBe3d4m2aBe2p03f1BgBiBbBkBbBbBcBg0b3eBdBgBbBlBjB2eBfBc4dBaBc4n0h1aBf4b4b4uBbBbBdBjBbBaBaBlBaBb4bBdBi3cBiBcBiBfB0dBu1c3cBeBBh3lBhBb0c3a3eBd2c2eBoBb3fBa0Bj1xBaBaBB1kBg3dBa1d2a2dBb1bBaBBr2fBaBd2hBaBn21dBd1BjBg2fBc2eBfBa0eBdBd1a1cB2kBa2bBfBfBiBjBaBlBfBcBiBe3gBdBcBcBb1a'
#30x30 - Daily Puzzle 10/05/20

puzzle_ultra = 'bBc1bBaBdBfBf2cBb0Bc3b2kBeBgBd3lBkBbBkBBnBgBh1bBe4cBa1cBi1fBk20eB1kBbBb1e1fBb4b4fBBh1iBaBfBBjBcBbBeBdBrBbBb1aBgBbBe3bBa0fBb4d3dBbBBcBf3fBaBc1aBhBbBi1gBb4kBiBc1c3e3iBfBb4fBdBgB2e1Bb1d2BjBlBb4c2g3e2gBBaBcBgBBhBi2g3f1cBh20fBl2iBe1fBdBdBc2gBbBbBb3fBb2BcBb3d4f4i3nBc2fBdBi3e3fBbBBBaBb4gBf3f3fBd4mBdBc2c3b4o0g4cBq3b4eBa2iBBBg3b1BBaBbBbBc2i21cBa3dBcBe3fBaBcBeBgBdBk1b2BcBBcBaBc1b3t3fBk1BaBc1c1n0g2c0aBbBhBa111dBa1a1c3c1aBaBbBp1tBnBh4b3k4n4eB2b2d2jBaBBlBaBjBbBiBdBcBm3cBgBa2cBBh2a3e1i3bBu1s2lBbBjBcB1dBb4eBeBBbBb3dBb4c1Ba3cBp3h3mBjBcBa3hBg3gBq0aBfBaBa2o4iBc21e2aBa2n4c2bBe10gBpBeB02d4bBBbBcBaB2bBeBb4m3r4cBbBaB2bBb4c4q2d4bBhBf2fBe0aBeBe0lBjBdBi4c1cBbBe3g4bBeBaBaBc2mBbBdBoBbBbBo4jBbBc1eB1cBk3n3lBgByBc3e4bBe4i1bBd4c1fBfBf3c3dBBcBbBf4b4c3b4dBaBb3rBzlBfBbBc3cBb3bBf3cBBc4bBcBdBaBa2dBcBBh3fBeBe12kBaBBi3eBhBe3gBb2eBbBc1B'
#50x50 - Monthly Puzzle 10/2020

ShakashakaSolver().solve(puzzle_medium, 20, 20)