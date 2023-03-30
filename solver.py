from math import sqrt
import time

class Solver:
    def solve_optimal(self, starting_state, prnt=True, diff=True, diff_trail=False): #Implement __hash__ and __eq__ for states
        self.prev_states = set()
        self.state_queue = []
        starting_state.previous = None
        self.state_queue = [starting_state]
        count_iterate = 0
        depth = 0
        depth_target = 1
        print("Solving...")
        start_time = time.time()
        while len(self.state_queue) > 0:
            count_iterate += 1
            state = self.state_queue.pop(0)
            next = self.get_next_states(state)
            for s in next:
                s.previous = state
                if self.check_finish(s):
                    elapsed = time.time() - start_time
                    #Done solving, print linked list of moves
                    move_list = [s]
                    while s.previous is not None:
                        move_list.insert(0, s.previous)
                        s = s.previous
                    if prnt:
                        if diff:
                            strs = [str(m) for m in move_list]
                            print(strs[0])
                            for i, m2 in enumerate(strs[1:]):
                                newstr = ""
                                m1 = strs[i]
                                for i2 in range(min(len(m1), len(m2))):
                                    if m1[i2] == m2[i2]: newstr += m1[i2]
                                    elif m2[i2] == ' ' and diff_trail: newstr += '\033[94m'+m1[i2]+'\033[00m'
                                    else: newstr += '\033[91m'+m2[i2]+'\033[00m'
                                if len(m1) > len(m2) and diff_trail: newstr += '\033[94m'+m1[len(m2):]+'\033[00m'
                                if len(m1) < len(m2): newstr += '\033[91m'+m2[len(m1):]+'\033[00m'
                                print(newstr)
                        else:
                            for m in move_list: print(m)
                    print("Solved in", len(move_list)-1, "moves!")
                    print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
                    return move_list
            for s in next:
                if not s in self.prev_states and self.check_state(s):
                    self.state_queue.append(s)
                    self.prev_states.add(s)
            if count_iterate == depth_target:
                depth += 1
                print("Depth " + str(depth) + '...')
                depth_target = count_iterate + len(self.state_queue)
        print("No solution exists.")
        elapsed = time.time() - start_time
        print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
        return []

    def solve_optimal_debug(self, starting_state): #Implement __hash__ and __eq__ for states
        self.prev_states = set()
        self.state_queue = []
        starting_state.previous = None
        self.state_queue = [starting_state]
        count_iterate = 0
        print("Solving...")
        start_time = time.time()
        while len(self.state_queue) > 0:
            print("QUEUE SIZE:", len(self.state_queue))
            state = self.state_queue.pop(0)
            print(state)
            input()
            next = self.get_next_states(state)
            for s in next:
                s.previous = state
                if self.check_finish(s):
                    elapsed = time.time() - start_time
                    #Done solving, print linked list of moves
                    move_list = [s]
                    while s.previous is not None:
                        move_list.insert(0, s.previous)
                        s = s.previous
                    for move in move_list:
                        print(move)
                    print("Solved in", len(move_list)-1, "moves!")
                    print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
                    return move_list
            for s in next:
                if not s in self.prev_states and self.check_state(s):
                    self.state_queue.append(s)
                    self.prev_states.add(s)
        print("No solution exists.")
        elapsed = time.time() - start_time
        print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
        return []

    def solve_recursive(self, starting_state, depth=0):
        self.depth = depth
        print("Solving...")
        start_time = time.time()
        state = self._solve_recursive(starting_state)
        elapsed = time.time() - start_time
        if state == None:
            print("No solution exists.")
        else:
            print(state)
        print("Solved in {:.2f} seconds".format(elapsed))

    def _solve_recursive(self, state): #Helper function
        result = self.iterate_state(state, depth=self.depth)
        while result == True:
            result = self.iterate_state(state, depth=self.depth)
        if result == None or not self.check_state(state):
            return None
        if self.check_finish(state):
            return state
        next = self.get_next_states(state)
        for s in next:
            result = self._solve_recursive(s)
            if result:
                return result
        return None

    #Recursive/optimal solving functions

    def get_next_states(self, state):
        return []

    def check_state(self, state):
        return True

    def check_finish(self, state):
        return True

    def iterate_state(self, state, depth):
        return False #State did not change
        #return True: State changed
        #return None: State is invalid

class BinaryGridState:
    def __init__(self, grid, x, y):
        self.grid = [row[:] for row in grid]
        self.x = x
        self.y = y
        self.width = len(self.grid[0])
        self.height = len(self.grid)
    def __repr__(self):
        string = ""
        for row in self.grid:
            for char in row:
               string += "0" if char == 1 else '-' if char == -1 else "." 
            string += "\n"
        return string
    def on_grid(self, x, y):
        return x >= 0 and y >= 0 and x < len(self.grid[0]) and y < len(self.grid)

class NumberGridState:
    def __init__(self, grid, x, y):
        self.grid = [row[:] for row in grid]
        self.x = x
        self.y = y
        self.width = len(self.grid[0])
        self.height = len(self.grid)
    def __repr__(self):
        string = ""
        for row in self.grid:
            for char in row:
               string += chr(char - 10 + ord('A')) if char > 9 else str(char) if char > 0 else "-" 
            string += "\n"
        return string
    def on_grid(self, x, y):
        return x >= 0 and y >= 0 and x < len(self.grid[0]) and y < len(self.grid)

class GridSolver:

    #Subclass must implement these functions as needed
    def get_next_states(self, state):
        return []

    def check_state(self, state):
        return True

    def check_finish(self, state):
        return True

    def iterate_state(self, state):
        return False #State did not change
        #return True: State changed
        #return None: State is invalid

    #Solving functions

    def solve_iterative(self, start_state, depth=100):
        print("Solving...")
        self.count_iterate = 0
        self.solution = None
        start_time = time.time()
        start_state.x = start_state.y = 0
        state = self._solve_iterative(start_state, depth)
        elapsed = time.time() - start_time
        if state == None:
            print("No solution exists.")
        else:
            print(state)
        print("Solved in {:.2f} seconds".format(elapsed))
        print(f"{self.count_iterate} iterations.")

    def _solve_iterative(self, state, max_depth):
        state.x = state.y = 0
        result = self.iterate_state(state)
        while result:
            self.count_iterate += 1
            result = self.iterate_state(state)
        depth = 0
        open_space = False
        while not self.solution:
            if state.grid[state.y][state.x] == 0:
                self.count_iterate += 1
                result = self.iterate_state(state)
                while result:
                    state.x = state.y = 0
                    open_space = False
                    result = self.iterate_state(state)
                next = self.get_next_states(state)
                if len(next) == 1:
                    state = next[0]
                    state.x = state.y = 0
                    open_space = False
                    continue
                elif len(next) == 0:
                    return None
                else:
                    open_space = True
                if depth >= 1:
                    #Bifurcate
                    nextSol = None
                    for s in next:
                        result = self._solve_iterative(s, depth-1)
                        if result:
                            if nextSol:
                                open_space = True
                                break
                            nextSol = s
                    else:
                        if nextSol == None:
                            return None
                        self.count_iterate += 1
                        open_space = False
                        state = nextSol
                        state.x = state.y = 0
                        depth = 0
            state.x += 1
            if state.x >= len(state.grid[state.y]):
                state.x = 0
                state.y += 1
            if state.x == 0 and state.y >= len(state.grid):
                if not open_space:
                    self.solution = state
                    return state
                if depth == max_depth:
                    return state
                depth += 1
                state.x = state.y = 0
        return self.solution

    def _solve_iterative_debug(self, state, max_depth):
        state.x = state.y = 0
        result = self.iterate_state(state)
        while result:
            print(state)
            input("Place! Logic 1A.")
            self.count_iterate += 1
            result = self.iterate_state(state)
        depth = 0
        open_space = False
        while not self.solution:
            if state.grid[state.y][state.x] == 0:
                self.count_iterate += 1
                result = self.iterate_state(state)
                while result:
                    print(state)
                    input("Place! Using iteration.")
                    state.x = state.y = 0
                    open_space = False
                    result = self.iterate_state(state)
                next = self.get_next_states(state)
                if len(next) == 1:
                    state = next[0]
                    print(state)
                    input("Place! Only valid move.")
                    state.x = state.y = 0
                    open_space = False
                    continue
                elif len(next) == 0:
                    print(state)
                    input(f"Invalid state! ({state.x} {state.y})")
                    return None
                else:
                    open_space = True
                if depth >= 1:
                    #Bifurcate
                    print(f"Bifurcate {depth}, ({state.x}, {state.y}), [{state.nums[state.y][state.x]}]")
                    nextSol = None
                    for s in next:
                        result = self._solve_iterative_debug(s, depth-1)
                        print(result != None)
                        if result:
                            if nextSol:
                                open_space = True
                                print("Inconclusive.")
                                break
                            nextSol = s
                    else:
                        if nextSol == None:
                            input(f"Invalid state! {state.x} {state.y}")
                            return None
                        self.count_iterate += 1
                        open_space = False
                        print(nextSol)
                        input(f"Place! Depth={depth}")
                        state = nextSol
                        state.x = state.y = 0
                        depth = 0
            state.x += 1
            if state.x >= len(state.grid[state.y]):
                state.x = 0
                state.y += 1
            if state.x == 0 and state.y >= len(state.grid):
                if not open_space:
                    self.solution = state
                    input("Solved!")
                    return state
                if depth == max_depth:
                    print("Max Depth Eceeded!!!!")
                    return state
                depth += 1
                state.x = state.y = 0
        return self.solution

    def solve_recursive(self, starting_state, depth=0): #State must have "grid", "x", and "y" variables
        print("Solving...")
        self.count_recurse = -1; self.count_iterate = 0
        start_time = time.time()
        starting_state.x = starting_state.y = 0
        state = self._solve_recursive(starting_state, depth)
        elapsed = time.time() - start_time
        if state == None:
            print("No solution exists.")
        else:
            print(state)
        print("Solved in {:.2f} seconds".format(elapsed))
        print(f"{self.count_recurse} recursions.")

    def _solve_recursive(self, state, depth):
        self.count_recurse += 1
        #result = self.iterate_state(state)
        #while result:
        #    self.count_iterate += 1
        #    result = self.iterate_state(state)
        if depth > 0:
            result = self._iterate_valid_placements(state, depth)
            if result != False: state = result
        if state == None: return None
        while state.grid[state.y][state.x] != 0:
            state.x += 1
            if state.x >= len(state.grid[state.y]):
                state.x = 0
                state.y += 1
                if state.y >= len(state.grid):
                    return state if self.check_finish(state) else None
        next = self.get_next_states(state)
        for s in next:
            result = self._solve_recursive(s, depth)
            if result:
                return result
        return None

    def solve_recursive_debug(self, starting_state): #State must have "grid", "x", and "y" variables
        starting_state.x = starting_state.y = 0
        state = self._solve_recursive_debug(starting_state)
        if state == None:
            print("No solution exists.")
        else:
            print(state)
        print("Solved!")

    def _solve_recursive_debug(self, state):
        result = self.iterate_state(state)
        while result == True:
            result = self.iterate_state(state)
        if result == None or not self.check_state(state):
            print("Invalid state found.")
            print(state)
            input()
            return None
        while state.grid[state.y][state.x] != 0:
            state.x += 1
            if state.x >= len(state.grid[state.y]):
                state.x = 0
                state.y += 1
                if state.y >= len(state.grid):
                    return state if self.check_finish(state) else None
        next = self.get_next_states(state)
        if len(next) == 0:
            print("Invalid state found.")
            print(state)
            print(state.x, state.y)
            input()
        for s in next:
            result = self._solve_recursive_debug(s)
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
        result = self.iterate_state(state)
        while result == True:
            result = self.iterate_state(state)
        if result == None or not self.check_state(state):
            return None
        while state.grid[state.y][state.x] != 0:
            state.x -= 1
            if state.x < 0:
                state.x = len(state.grid[0]) - 1
                state.y -= 1
                if state.y < 0:
                    return state if self.check_finish(state) else None
        next = self.get_next_states(state)
        for s in next:
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

    def rows(self, state):
        return [row[:] for row in state.grid]

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
DIRECTIONS8_HALF = [(-1, 0), (-1, -1), (0, -1), (1, -1)]