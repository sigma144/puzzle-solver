from solver import Solver, GridSolver, BinaryGridState, DIRECTIONS
from math import sqrt

class HeyawakeSolver(GridSolver):
    def solve(self, board):
        regions = [r.split(',') for r in board.split(';')]
        width = height = int(sqrt(sum([int(r[1])*int(r[2]) for r in regions])))
        starting_state = BinaryGridState([[0 for x in range(width)] for y in range(height)], 0, 0)
        region_ids = [0 for x in range(width*height)]
        region_totals = []
        pos = 0
        for i,r in enumerate(regions):
            while region_ids[pos]:
                pos += 1
            num, w, h = r
            for x in range(int(w)):
                for y in range(int(h)):
                    region_ids[pos + x + y*width] = str(i+1)
            region_totals.append('b' if num == 'b' else int(num))
        self.decode_regions(','.join(region_ids), width, height)
        self.region_totals = [[0 for x in range(width)] for y in range(height)]
        for i, region in enumerate(self.get_all_region_points()):
            for x, y in region:
                self.region_totals[y][x] = region_totals[i]
        self.solve_recursive(starting_state)
    def get_next_states(self, state):
        states = []
        if self.can_place_white(state, state.x, state.y):
            new_state = BinaryGridState(state.grid, state.x, state.y)
            new_state.grid[state.y][state.x] = -1
            states.append(new_state)
        if self.can_place_black(state, state.x, state.y):
            new_state = BinaryGridState(state.grid, state.x, state.y)
            new_state.grid[state.y][state.x] = 1
            if state.x < len(state.grid[0]) - 1:
                new_state.grid[state.y][state.x + 1] = -1
            states.append(new_state)
        return states
    def can_place_white(self, state, x, y):
        #Check row
        if x > 1 and state.grid[y][x-1] == -1 and self.get_region_points(x, y) is not self.get_region_points(x-1, y):
            r = self.get_region_points(x-1, y)
            for X in range(x-2, -1, -1):
                if state.grid[y][X] == 1:
                    break
                if self.get_region_points(X, y) is not r:
                    return False
        #Check column
        if y > 1 and state.grid[y-1][x] == -1 and self.get_region_points(x, y) is not self.get_region_points(x, y-1):
            r = self.get_region_points(x, y-1)
            for Y in range(y-2, -1, -1):
                if state.grid[Y][x] == 1:
                    break
                if self.get_region_points(x, Y) is not r:
                    return False
        #Check region
        if self.region_totals[y][x] != 'b':
            region = self.get_region(state, x, y)
            if region.count(-1) >= len(region) - self.region_totals[y][x]:
                return False
        return True
    def can_place_black(self, state, x, y):
        if y > 0 and state.grid[y-1][x] == 1:
            return False
        if x < len(state.grid[0]) - 1 and not self.can_place_white(state, x+1, y):
            return False
        #Check region
        if self.region_totals[y][x] != 'b':
            region = self.get_region(state, x, y)
            if region.count(1) >= self.region_totals[y][x]:
                return False
        #Check connectivity
        if y == 0:
            return True
        if y == len(state.grid) - 1:
            if (x > 0 and state.grid[y-1][x-1] == 1 or x < len(state.grid[0]) - 1 and state.grid[y-1][x+1] == 1) and not self.check_boundary(state, x, y-1):
                return False
        elif (x == 0 or state.grid[y-1][x-1] == 1) and (x == len(state.grid[0]) - 1 or state.grid[y-1][x+1] == 1) and not self.check_boundary(state, x, y-1):
            return False
        return True
    def check_boundary(self, state, x, y):
        if (x == 0 or state.grid[y][x-1] == 1) and (x == len(state.grid[0]) - 1 or state.grid[y][x+1] == 1) and (y == 0 or state.grid[y-1][x] == 1):
            return False
        destx, desty = (x+1, y+1) if x < len(state.grid[0]) - 1 and state.grid[y][x+1] == 1 else (x-1, y+1)
        #Flow right
        if x < len(state.grid[0]) - 1:
            result = self.flow_boundary(state, x, y, destx, desty, False)
            if result != None:
                return result
        #Flow left
        if x > 0:
            result = self.flow_boundary(state, x, y, destx, desty, True)
            if result != None:
                return result
        return False
    def flow_boundary(self, state, startx, starty, destx, desty, flow_left):
        dir = 2 if flow_left else 0
        x, y = startx, starty
        rot1 = 1 if flow_left else 3
        rot2 = 3 if flow_left else 1
        while True:
            dx, dy = x + DIRECTIONS[dir][0], y + DIRECTIONS[dir][1]
            if not self.on_grid(state, dx, dy):
                return None
            elif state.grid[dy][dx] == 1 or dx == startx and dy == starty + 1:
                dir = (dir + rot1) % 4
            elif dx == destx and dy == desty:
                return True
            elif dx == startx and dy == starty:
                return False
            else:
                x, y = dx, dy
                dir = (dir + rot2) % 4

puzzle_easy = 'b,1,1;b,1,1;b,1,2;2,3,2;1,2,1;2,1,4;2,3,3;b,1,2;1,1,1;b,1,2;1,1,1;1,5,1'
#Hard 6x6 - ID: 5266560

puzzle_medium = 'b,4,2;2,5,1;1,2,3;2,4,1;b,3,1;b,2,1;b,1,2;2,2,2;b,1,2;2,4,1;2,3,3;2,1,7;b,1,1;1,1,6;b,3,1;b,2,3;b,1,2;2,4,1;2,2,2;b,1,2;b,1,4;2,2,2;b,1,2;2,3,2;b,1,2;1,3,1;b,1,3;b,1,4;b,1,2;b,2,1;b,3,1;b,3,1;b,1,2;b,2,4;2,4,1;3,2,3;1,2,1;b,4,2;1,1,2;2,2,3;1,2,1;b,1,1;2,2,5;b,2,5;b,1,2;b,1,2;3,2,4;b,3,2;b,2,2;1,1,3;b,1,3;b,2,2;0,1,2;1,2,2;0,2,2'
#Hard 15x15 - ID: 7805533

puzzle_hard = 'b,1,3;0,2,1;b,1,1;b,3,2;b,1,2;b,3,2;3,11,1;b,2,1;b,1,8;b,3,3;b,2,2;b,2,1;0,1,2;b,3,2;3,3,3;b,1,1;1,1,1;2,1,5;b,2,3;b,1,1;b,3,1;1,1,1;b,1,1;b,2,4;0,1,2;b,3,1;b,1,4;b,5,2;1,1,3;0,2,1;b,1,3;1,2,1;2,1,6;3,2,3;b,5,1;b,1,2;b,2,1;b,1,2;b,1,3;b,1,3;b,1,5;2,1,4;1,2,4;b,2,1;2,1,4;1,1,4;b,1,5;b,1,4;b,1,3;b,3,2;2,2,3;b,2,2;1,2,1;b,1,3;b,2,2;3,3,2;b,1,2;2,1,3;b,2,3;1,1,6;b,2,2;b,1,1;b,1,4;2,1,6;2,3,2;0,2,1;b,2,3;b,3,3;b,4,1;b,2,6;2,3,3;b,2,1;b,1,2;b,3,1;3,1,5;3,2,5;b,3,1;b,2,6;1,3,1;b,1,2;b,2,1;b,1,3;b,1,2;b,2,1;2,3,2;b,1,5;b,2,4;b,5,1;0,1,2;b,1,2;b,1,1;2,2,2;0,2,1;b,1,3;b,2,1;b,2,1;b,1,3;0,1,1;b,1,1;b,1,5;b,1,2;3,3,2;2,4,1;b,4,2;b,5,1;3,4,2;1,2,1;b,2,1;b,1,2;b,1,4;b,1,3;b,5,1;0,2,1;3,4,3;2,6,1;b,4,3;2,1,5;b,5,1;0,1,4;b,1,2;b,6,1;2,3,1;b,2,4;1,1,4;b,5,3;b,2,1;b,1,4;1,2,2;2,2,2;1,3,2;1,3,2;0,2,1;b,2,1;b,1,1;b,3,2;1,1,1;b,1,1;4,6,2;b,4,1;b,1,1;b,2,1;b,2,1;b,1,1;b,4,1;2,5,1;3,6,1;0,3,1'
#25x25 Daily Puzzle - 10/05/20

HeyawakeSolver().solve(puzzle_medium)