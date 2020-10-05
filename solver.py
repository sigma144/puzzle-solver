from math import sqrt

class Solver:
    def solve_optimal(self, starting_state): #Implement __hash__ and __eq__ for states
        self.prev_states = set()
        self.state_queue = []
        starting_state.previous = None
        self.state_queue = [starting_state]
        while len(self.state_queue) > 0:
            state = self.state_queue.pop(0)
            next = self.get_next_states(state)
            for s in next:
                s.previous = state
                if self.check_finish(s):
                    #Done solving, print linked list of moves
                    move_list = [s]
                    while s.previous != None:
                        move_list.insert(0, s.previous)
                        s = s.previous
                    for move in move_list:
                        print(move, end = " ")
                    return
            for s in next:
                if not s in self.prev_states and self.check_state(s):
                    if len(self.state_queue) > 10000:
                        print("State queue max size exceeded, cannot solve.")
                        return
                    self.state_queue.append(s)
                    self.prev_states.add(s)
        print("No solution exists.")

    def solve_recursive(self, starting_state):
        state = self._solve_recursive(starting_state)
        if state == None:
            print("No solution exists.")
        else:
            print(state)

    def _solve_recursive(self, state): #Helper function
        next = self.get_next_states(state)
        if self.check_finish(state):
            return state
        for s in next:
            if self.check_state(s):
                result = self._solve_recursive(s)
                if result:
                    return result
        return None

    def solve_iterative(self, starting_state):
        last_state = starting_state
        state = last_state
        while True:
            state = self.next_state(state)
            if state == None:
                state = self.prev_level(last_state)
                if state == None:
                    print("No solution exists.")
                    return
            else:
                state = self.next_level(state)
                if state == None:
                    print(last_state)
                    return
                last_state = state

    #Recursive/optimal solving functions

    def get_next_states(self, state):
        return []

    def check_state(self, state):
        return True

    def check_finish(self, state):
        return True

    #Iterative solving functions

    def next_state(self, state):
        return state

    def next_level(self, state):
        return state

    def prev_level(self, state):
        return state

class BinaryGridState:
    def __init__(self, grid, x, y):
        self.grid = [row[:] for row in grid]
        self.x = x
        self.y = y

    def __repr__(self):
        string = ""
        for row in self.grid:
            for char in row:
               string += "0" if char == 1 else "-" 
            string += "\n"
        return string

class NumberGridState:
    def __init__(self, grid, x, y):
        self.grid = [row[:] for row in grid]
        self.x = x
        self.y = y

    def __repr__(self):
        string = ""
        for row in self.grid:
            for char in row:
               string += chr(char - 10 + ord('A')) if char > 9 else str(char) if char > 0 else "-" 
            string += "\n"
        return string

class GridSolver:

    #Subclass must implement these functions as needed
    def get_next_states(self, state):
        return []

    def check_state(self, state):
        return True

    def check_finish(self, state):
        return True

    #Solving functions

    def solve_recursive(self, starting_state): #State must have "grid", "x", and "y" variables
        starting_state.x = starting_state.y = 0
        state = self._solve_recursive(starting_state)
        if state == None:
            print("No solution exists.")
        else:
            print(state)

    def _solve_recursive(self, state):
        while state.grid[state.y][state.x] != 0:
            state.x += 1
            if state.x >= len(state.grid[state.y]):
                state.x = 0
                state.y += 1
                if state.y >= len(state.grid):
                    return state if self.check_finish(state) else None
        next = self.get_next_states(state)
        for s in next:
            if self.check_state(s):
                result = self._solve_recursive(s)
                if result:
                    return result
        return None

    #Reverse version, in case it is faster

    def solve_recursive_r(self, starting_state): #State must have "grid", "x", and "y" variables
        starting_state.x = len(starting_state.grid[0]) - 1
        starting_state.y = len(starting_state.grid) - 1
        state = self._solve_recursive_r(starting_state)
        if state == None:
            print("No solution exists.")
        else:
            print(state)

    def _solve_recursive_r(self, state):
        while state.grid[state.y][state.x] != 0:
            state.x -= 1
            if state.x < 0:
                state.x = len(state.grid[0]) - 1
                state.y -= 1
                if state.y < 0:
                    return state if self.check_finish(state) else None
        next = self.get_next_states(state)
        for s in next:
            if self.check_state(s):
                result = self._solve_recursive_r(s)
                if result:
                    return result
        return None

    #Helper functions

    def get_row(self, state, y):
        return state.grid[y]

    def get_column(self, state, x):
        return [row[x] for row in state.grid]

    def get_region(self, state, x, y):
        return [state.grid[y][x] for x, y in self.get_region_points(x, y)]

    def get_region_points(self, x, y):
        return self._regions[y][x]

    def get_all_region_points(self):
        return self._region_list

    def _get_region(self, walls, x, y):
        points = set()
        self._get_region_r(walls, x, y, points)
        return points

    def _get_region_r(self, walls, x, y, points):
        if (x, y) in points:
            return
        points.add((x, y))
        if x < len(walls[y]) - 1 and not walls[y][x] & WALL_RIGHT:
            self._get_region_r(walls, x + 1, y, points)
        if x > 0 and not walls[y][x] & WALL_LEFT:
            self._get_region_r(walls, x - 1, y, points)
        if y < len(walls) - 1 and not walls[y][x] & WALL_DOWN:
            self._get_region_r(walls, x, y + 1, points)
        if y > 0 and not walls[y][x] & WALL_UP:
            self._get_region_r(walls, x, y - 1, points)

    def verify_walls(self, walls):
        for y, row in enumerate(walls):
            for x, cell in enumerate(row):
                if cell & WALL_UP and y > 0 and not walls[y - 1][x] & WALL_DOWN:
                    raise Exception("Error from " + str((x, y)) + str([walls[y][x]]) + " to " + str((x, y - 1)) + str([walls[y - 1][x]]))
                if cell & WALL_DOWN and y < len(walls) - 1 and not walls[y + 1][x] & WALL_UP:
                    raise Exception("Error from " + str((x, y)) + str([walls[y][x]]) + " to " + str((x, y + 1)) + str([walls[y + 1][x]]))
                if cell & WALL_LEFT and x > 0 and not walls[y][x - 1] & WALL_RIGHT:
                    raise Exception("Error from " + str((x, y)) + str([walls[y][x]]) + " to " + str((x - 1, y)) + str([walls[y][x - 1]]))
                if cell & WALL_RIGHT and x < len(walls[y]) - 1 and not walls[y][x + 1] & WALL_LEFT:
                    raise Exception("Error from " + str((x, y)) + str([walls[y][x]]) + " to " + str((x + 1, y)) + str([walls[y][x + 1]]))
        self._regions = [[self._get_region(walls, x, y) for x in range(len(walls[y]))] for y in range(len(walls))]
        self._region_list = []
        covered = set()
        for y, row in enumerate(self._regions):
            for x, region in enumerate(row):
                if (x, y) in covered:
                    continue
                self._region_list.append(region)
                for point in region:
                    covered.add(point)

    def decode_regions(self, region_ids, width = 0, height = 0):
        region_ids = [int(num.strip("\n")) for num in region_ids.split(",")]
        if width == 0 or height == 0:
            width = height = int(sqrt(len(region_ids)))
        num_regions = max(region_ids)
        self._regions = [[None for x in range(width)] for y in range(height)]
        self._region_list = [set() for i in range(num_regions)]
        for i, num in enumerate(region_ids):
            self._region_list[num - 1].add((i % width, i // width))
        for region in self._region_list:
            for x, y in region:
                self._regions[y][x] = region

    def decode_grid_values(self, grid_values, width, height, default = 0):
        grid = [[default for x in range(width)] for y in range(height)]
        position = 0
        num = 0
        for char in grid_values:
            if char >= '0' and char <= '9':
                num = num * 10 + int(char)
            else:
                if num > 0:
                    grid[position // height][position % width] = num
                    num = 0
                    position += 1
                if char != "_":
                    position += ord(char) - ord('a') + 1
        return grid

    def decode_grid_digits(self, state, grid_values, width, height):
        position = 0
        for char in grid_values:
            if char >= '0' and char <= '9':
                state.grid[position // height][position % width] = int(char)
                position += 1
            else:
                position += ord(char) - ord('a') + 1

    def on_grid(self, state, x, y):
        return y >= 0 and y < len(state.grid) and x >= 0 and x < len(state.grid[y])

    def rows(self, state):
        return state.grid

    def columns(self, state):
        return [[row[x] for row in state.grid] for x in range(len(state.grid[0]))]

    def regions(self, state):
        return [[state.grid[y][x] for x, y in region] for region in self.get_all_region_points()]

WALL_UP = 1
WALL_RIGHT = 2
WALL_DOWN = 4
WALL_LEFT = 8
#Open up = 14
#Open right = 13
#Open down = 11
#Open left = 7

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIRECTIONS8 = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
DIRECTIONS8_HALF = [(-1, 0), (-1, -1), (0, -1), (1, -1), ]