from math import sqrt
import time
from collections import deque
import heapq
import psutil
from dataclasses import dataclass
import pickle, bisect

_catalog = _used = None
class Catalog:
    @staticmethod
    def init():
        global _catalog, _used
        _catalog = []; _used = {}
    @staticmethod
    def add(val):
        global _catalog, _used
        if val in _used:
            return _used[val]
        _catalog.append(val)
        _used[val] = len(_catalog) - 1
        return len(_catalog) - 1
    @staticmethod
    def sadd(val):
        global _catalog, _used
        sval = repr(val)
        if sval in _used:
            return _used[sval]
        _catalog.append(val)
        _used[sval] = len(_catalog) - 1
        return len(_catalog) - 1
    @staticmethod
    def get(num):
        global _catalog
        return _catalog[num]

class Solver:
    _red = '\033[91m'; _blue = '\033[94m'; _black = '\033[00m'; _green = '\033[92m'
    #Implement __hash__ and __eq__ for states
    def solve_optimal(self, starting_state, debug=0, prnt=1, diff=1, diff_trail=0, showprogress=0, use_score=0, optimize_score=0, use_names=0, **kwargs):
        start_time = time.time()
        self.kwargs = kwargs
        starting_state = self.setup(starting_state)
        starting_state.previous = None
        print(starting_state)
        print("Solving...")
        prev_states = {starting_state}
        self._state_queue = deque()
        self._state_queue.append(starting_state)
        self._next_queue = deque()
        self._depth = 0
        self._score = 0
        self._moves = 0
        best_score = None
        best_state = None
        count_iterate = 0
        depth_time = time.time()
        depth_last = 0
        if use_score or optimize_score:
            use_score = True
            starting_state._invalidate = False
            score = (0, self.score_state(starting_state))
            if optimize_score: score = (score[1], score[0])
            prev_states = {starting_state: (starting_state, score)}
            self._next_queue = {score: self._state_queue}
            self._score = score
        def finish_solve(state):
            elapsed = time.time() - start_time
            move_list = self.trace_moves(state, prnt, diff, diff_trail, use_names)
            if optimize_score:
                print("Solved with score", str(self.score_state(state))+"!")
                print("Moves:", len(move_list)-1)
            else:
                print("Solved in", len(move_list)-1, "moves!")
                if self.score_state(state) is not None:
                    print("Score:", str(self.score_state(state)))
            print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
            return move_list
        while True:
            count_iterate += 1
            state = self._state_queue.popleft()
            if debug: print(state, "\n^ Current" + (': ' + state.name if use_names else '') + "\n")
            if use_score and state._invalidate: next = []
            else: next = self.get_next_states(state)
            hint = 0
            if debug:
                for i, s in enumerate(next):
                    print(s, "\n^ "+str(i+1)+ (': ' + s.name if use_names else '') + "\n")
                hint = input() or 0
                if hint: next = [next[min(int(hint) - 1, len(next) - 1)]]
            for s in next:
                s.previous = state
                if not self.check_state(s): continue
                if use_score:
                    s._invalidate = False
                    score = (self._moves + 1, self.score_state(s))
                    if optimize_score: score = (score[1], score[0])
                    if s in prev_states and not hint:
                        s2, score2 = prev_states[s]
                        if score < score2:
                            s2._invalidate = True
                        else: continue
                    if self.check_finish(s):
                        if best_score is None or score < best_score:
                            best_score = score
                            best_state = s
                    prev_states[s] = (s, score)
                    if score not in self._next_queue: self._next_queue[score] = deque()
                    self._next_queue[score].append(s)
                else:
                    if self.check_finish(s): return finish_solve(s)
                    if len(prev_states) != (prev_states.add(s) or len(prev_states)) or hint:
                        self._next_queue.append(s)
            if count_iterate % 20000 == 0:
                if showprogress:
                    print(state)
                    print("Depth "+str(self._depth)+",", str(count_iterate // 1000) + "k states checked, total time {:.2f}s".format(time.time() - start_time))
                memuse = psutil.virtual_memory()[2]
                if memuse >= 95:
                    print(Solver._red + "HIGH MEMORY USE, PERFORMANCE MAY BE SLOW" + Solver._black)
            if len(self._state_queue) == 0:
                if use_score:
                    self._next_queue.pop(self._score)
                    if len(self._next_queue) == 0: break
                    score = min(self._next_queue)
                    if score == best_score: return finish_solve(best_state)
                    self._state_queue = self._next_queue[score]
                    self._score = score
                    if optimize_score: self._moves = score[1]
                    else: self._moves = score[0]
                    if score[0] == self._depth: continue
                    self._depth = score[0]
                else:
                    if len(self._next_queue) == 0: break
                    self._state_queue = self._next_queue
                    self._next_queue = deque()
                    self._depth += 1
                elapsed = time.time() - depth_time
                time_diff = elapsed - depth_last
                depth_last = elapsed
                depth_time = time.time()
                print("Depth "+str(self._depth)+': '+str(count_iterate)+' iterations, {:.2f}s, '.format(time.time()-start_time)+"depth time {:.2f}".format(elapsed)+'s '+(Solver._green if time_diff<0 else Solver._red)+'('+('+' if time_diff>=0 else '')+'{:.2f}s)'.format(time_diff)+Solver._black)
        print("No solution exists.")
        if best_state is not None:
            print("Best state", best_state)
        elapsed = time.time() - start_time
        print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
        return []
    @staticmethod
    def trace_moves(s, prnt=0, diff=1, diff_trail=0, use_names=0):
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
                        elif m2[i2] == ' ' and diff_trail: newstr += Solver._red+m1[i2]+Solver._black
                        else: newstr += Solver._red+m2[i2]+Solver._black
                    if len(m1) > len(m2) and diff_trail: newstr += Solver._blue+m1[len(m2):]+Solver._black
                    if len(m1) < len(m2): newstr += Solver._red+m2[len(m1):]+Solver._black
                    print(newstr)
            elif use_names and move_list:
                print(', '.join([m.name for m in move_list[1:]]))
            else:
                for m in move_list: print(m)
        return move_list
    
    def solve_recursive(self, starting_state, debug=0):
        print("Solving...")
        self.count_recurse = -1
        start_time = time.time()
        state = self._solve_recursive(starting_state, debug)
        elapsed = time.time() - start_time
        if state is None:
            print("No solution exists.")
        else:
            print(state)
        print("Solved in {:.2f} seconds".format(elapsed))
        print(f"{self.count_recurse} recursions.")
        return state

    def _solve_recursive(self, state, debug=0):
        if debug:
            input(state)
        self.count_recurse += 1
        if state == None: return None
        if self.check_finish(state):
            return state
        next = self.get_next_states(state)
        for s in next:
            if not self.check_state(s):
                continue
            result = self._solve_recursive(s, debug)
            if result:
                return result
        return None

    #Recursive/optimal solving functions

    def setup(self, puzzle):
        return puzzle

    def get_next_states(self, state):
        return []

    def check_state(self, state):
        return True

    def check_finish(self, state):
        return True
    
    def score_state(self, state):
        return None

@dataclass
class Vec3:
    x = 0; y = 0; z = 0
    def __init__(self, x, y, z): self.x = x; self.y = y; self.z = z
    def __add__(self, v): return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)
    def __sub__(self, v): return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)
    def __mul__(self, v): return Vec3(self.x*v, self.y*v, self.z*v)
    def __neg__(self): return Vec3(-self.x, -self.y, -self.z)
    def __repr__(self): return f"({self.x}, {self.y}, {self.z})"
    def __iter__(self): return iter((self.x, self.y, self.z))
    def __hash__(self): return hash((self.x, self.y, self.z))
    def __eq__(self, v): return isinstance(v, Vec3) and v.x == self.x and v.y == self.y and v.z == self.z
    def __lt__(self, v): return self.z < v.z if self.z != v.z else self.y < v.y if self.y != v.y else self.x < v.x
    def __ge__(self, v): return self.z > v.z if self.z != v.z else self.y > v.y if self.y != v.y else self.x >= v.x
    def __contains__(self, v): return 0 <= v.x < self.x and 0 <= v.y < self.y and 0 <= v.z <= self.z

class BlockPushState:
    _symbols = None
    _nsymbols = None
    _stacks = None
    @staticmethod
    def _sym_to_int(val):
        result = BlockPushState._symbols.find(val)
        if result == -1: return -BlockPushState._nsymbols.find(val) - 1
        return result
    @staticmethod
    def _int_to_sym(val):
        return BlockPushState._symbols[val] if val >= 0 else BlockPushState._nsymbols[-val - 1]
    @staticmethod
    def build_puzzle(puzzle, exceptions={'':[0]}):
        if BlockPushState._stacks is not None:
            height = max([len(l) for l in list(BlockPushState._stacks.values()) + list(exceptions.values())])
        grid = [[[-1 for _ in range(len(puzzle[0]))] for _ in range(len(puzzle))] for _ in range(height)]
        for y, row in enumerate(puzzle):
            for x, val in enumerate(row):
                if val in exceptions:
                    for z, val in enumerate(exceptions[val]):
                        grid[z][y][x] = BlockPushState._sym_to_int(val)
                elif val in BlockPushState._stacks:
                    for z, val in enumerate(BlockPushState._stacks[val]):
                        grid[z][y][x] = BlockPushState._sym_to_int(val)
                else:
                    grid[0][y][x] = BlockPushState._sym_to_int(val)
        return BlockPushState(grid, Vec3(0, 0, 0))
    @staticmethod
    def define_params(symbols, nsymbols, dsymbols, stacks):
        BlockPushState._symbols = symbols
        BlockPushState._nsymbols = nsymbols if nsymbols else ' '
        BlockPushStateD._dsymbols = dsymbols
        BlockPushState._stacks = stacks
    def __init__(self, grid=None, origin=None):
        if isinstance(grid, BlockPushState):
            grid, origin = grid._grid, grid._origin
        self._grid = [layer[:] for layer in grid]
        self._origin = origin
    def __repr__(self):
        collapse = [[-1 for _ in row] for row in self._grid[0]]
        for layer in self._grid:
            for y, row in enumerate(layer):
                for x, val in enumerate(row):
                    if val != -1:
                        collapse[y][x] = val
        return '\n'+'\n'.join([''.join([BlockPushState._int_to_sym(c) for c in row]) for row in collapse])
    def __hash__(self):
        return hash(pickle.dumps(self._grid))
    def __eq__(self, state):
        return self._grid == state._grid
    def __iter__(self):
        class BPSIterator:
            def __init__(self, size, origin):
                self.size = size - origin
                self.origin = origin
                self.pos = Vec3(-origin.x - 1, -origin.y, -origin.z)
            def __next__(self):
                self.pos = Vec3(self.pos.x + 1, self.pos.y, self.pos.z)
                if self.pos.x >= self.size.x:
                    self.pos = Vec3(-self.origin.x, self.pos.y + 1, self.pos.z)
                if self.pos.y >= self.size.y:
                    self.pos = Vec3(-self.origin.x, -self.origin.y, self.pos.z + 1)
                if self.pos.z >= self.size.z:
                    raise StopIteration
                return self.pos
        return BPSIterator(Vec3(len(self._grid[0][0]), len(self._grid[0]), len(self._grid)), self._origin)
    def on_grid(self, pos):
        return pos.x >= 0 and pos.y >= 0 and pos.z >= 0 and pos.x < len(self._grid[0][0]) and pos.y < len(self._grid[0]) and pos.z < len(self._grid)
    def get(self, pos):
        pos = pos + self._origin
        if pos not in Vec3(len(self._grid[0][0]), len(self._grid[0]), len(self._grid)):
            return -1
        return self._grid[pos.z][pos.y][pos.x]
    def set(self, pos, val):
        x, y, z = pos + self._origin
        if z < 0: return False
        if z >= len(self._grid):
            self._grid = self._grid[:]
            self._grid.append([[-1 for _ in range(len(self._grid[0][0]))] for _ in range(len(self._grid[0]))])
            return self.set(pos, val)
        if y < 0:
            self._grid = [layer[:] for layer in self._grid]
            for z in range(len(self._grid)):
                self._grid[z].insert(0, [-1 for _ in range(len(self._grid[0][0]))])
            self._origin = Vec3(self._origin.x, self._origin.y + 1, self._origin.z)
            return self.set(pos, val)
        if y >= len(self._grid[0]):
            self._grid = [layer[:] for layer in self._grid]
            for z in range(len(self._grid)):
                self._grid[z].append([-1 for _ in range(len(self._grid[0][0]))])
            return self.set(pos, val)
        if x < 0:
            self._grid = [[row[:] for row in layer] for layer in self._grid]
            for z in range(len(self._grid)):
                for y in range(len(self._grid[0])):
                    self._grid[z][y].insert(0, -1)
            self._origin = Vec3(self._origin.x + 1, self._origin.y, self._origin.z)
            return self.set(pos, val)
        if x >= len(self._grid[0][0]):
            self._grid = [[row[:] for row in layer] for layer in self._grid]
            for z in range(len(self._grid)):
                for y in range(len(self._grid[0])):
                    self._grid[z][y].append(-1)
            return self.set(pos, val)
        self._grid[z][y] = self._grid[z][y][:]
        self._grid[z][y][x] = val
        return True
    def push(self, pos, dir): #Block push for 1x1 blocks
        result = self.can_push(pos, dir, self.get(pos))
        if result is False: return False
        if pos.z == 0 and dir.z < 0: return False
        next = pos+dir
        if not self.push(pos, next): return False
        if self.commit_push(next, dir, self.get(next)) is False: return False
        self.set(next, -1)
    def push_connected(self, pos, dir): #Block push for larger blocks
        to_commit = {}
        if not self._push_connected(pos, dir, to_commit):
            return False
        for p, val in to_commit.items():
            if self.commit_push(p+dir, dir, val) is False:
                return False
            if p-dir not in to_commit:
                self.set(p, -1)
        return True
    def _push_connected(self, pos, dir, to_commit): 
        if not isinstance(pos, list):
            pos = [pos]
        pos = set(sum([[p, p+dir] + self.get_connected(p, dir, self.get(p)) for p in pos], start=[]))
        for p in pos:
            if p in to_commit: continue
            result = self.can_push(p, dir, self.get(p))
            if result is False: return False
            if result is None: continue
            if p.z == 0 and dir.z < 0: return False
            to_commit[p] = self.get(p)
            if not self._push_connected(p, dir, to_commit):
                return False
        return True
    def can_push(self, pos, dir, val): #Implement in subclass
        if val == -1: return None #Doesn't move, but can be pushed onto
        return True
    def commit_push(self, pos, dir, val): #Implement if blocks need to change when pushed
        self.set(pos, val)
    def get_connected(self, pos, dir, val): #Implement to allow blocks to be attached to each other
        return []
    
class BlockPushStateD: #Separates static and dynamic state, better for large or arbitrary-size grids
    _dsymbols = None
    @staticmethod
    def _set_char(pos, val, static, dynamic):
        result = BlockPushState._symbols.find(val)
        if result == -1: result = -BlockPushState._nsymbols.find(val) - 1
        if val in BlockPushStateD._dsymbols: dynamic.append((pos, result))
        else: static[pos.z][pos.y][pos.x] = result
    _get_char = BlockPushState._int_to_sym
    @staticmethod
    def build_puzzle(puzzle, exceptions={'':[0]}):
        if BlockPushState._stacks is not None:
            height = max([len(l) for l in list(BlockPushState._stacks.values()) + list(exceptions.values())])
        grid = [[[-1 for _ in range(len(puzzle[0]))] for _ in range(len(puzzle))] for _ in range(height)]
        dynamic = []
        for y, row in enumerate(puzzle):
            for x, val in enumerate(row):
                if val in exceptions:
                    for z, val in enumerate(exceptions[val]):
                        BlockPushStateD._set_char(Vec3(x, y, z), val, grid, dynamic)
                elif val in BlockPushState._stacks:
                    for z, val in enumerate(BlockPushState._stacks[val]):
                        BlockPushStateD._set_char(Vec3(x, y, z), val, grid, dynamic)
                else:
                    BlockPushStateD._set_char(Vec3(x, y, 0), val, grid, dynamic)
        state = BlockPushStateD(grid, dynamic)
        state._origin = Vec3(0, 0, 0)
        return state
    def __init__(self, grid, dynamic=None):
        if isinstance(grid, BlockPushStateD):
            dynamic = grid._dynamic
            grid = grid._grid
        self._grid = grid
        self._dynamic = dynamic[:]
    def __repr__(self):
        collapse = [[-1 for _ in row] for row in self._grid[0]]
        for layer in self._grid:
            for y, row in enumerate(layer):
                for x, val in enumerate(row):
                    if val != -1:
                        collapse[y][x] = val
        for p, val in self._dynamic:
            if val != -1 and p in Vec3(len(collapse[0]), len(collapse), 10):
                collapse[p.y][p.x] = val
        return '\n'+'\n'.join([''.join([BlockPushStateD._get_char(c) for c in row]) for row in collapse])
    def __hash__(self):
        return hash(pickle.dumps(self._dynamic))
    def __eq__(self, state):
        return self._dynamic == state._dynamic
    __iter__ = BlockPushState.__iter__
    def get(self, pos):
        i = bisect.bisect_left(self._dynamic, pos, key=lambda p: p[0])
        if i < len(self._dynamic) and self._dynamic[i][0] == pos:
            return self._dynamic[i][1]
        if pos not in Vec3(len(self._grid[0][0]), len(self._grid[0]), len(self._grid)):
            return -1
        return self._grid[pos.z][pos.y][pos.x]
    def set(self, pos, val):
        i = bisect.bisect_left(self._dynamic, pos, key=lambda p: p[0])
        if i < len(self._dynamic) and self._dynamic[i][0] == pos:
            if val == -1:
                self._dynamic.pop(i)
            else: self._dynamic[i] = (pos, val)
        elif val != -1:
            self._dynamic.insert(i, (pos, val))
    push = BlockPushState.push
    push_connected = BlockPushState.push_connected
    _push_connected = BlockPushState._push_connected
    can_push = BlockPushState.can_push
    commit_push = BlockPushState.commit_push
    get_connected = BlockPushState.get_connected

class BinaryGridState:
    def __init__(self, grid, x, y):
        self.grid = grid[:]
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
    def __hash__(self):
        return hash(pickle.dumps((self.grid, self.x, self.y)))
    def on_grid(self, x, y):
        return x >= 0 and y >= 0 and x < len(self.grid[0]) and y < len(self.grid)
    def set(self, x, y, val):
        self.grid[y] = self.grid[y][:]
        self.grid[y][x] = val
    def set2(self, val):
        self.set(self.x, self.y, val)

class NumberGridState:
    def __init__(self, grid, x, y):
        self.grid = grid[:]
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
    def __hash__(self):
        return hash(pickle.dumps((self.grid, self.x, self.y)))
    def on_grid(self, x, y):
        return x >= 0 and y >= 0 and x < len(self.grid[0]) and y < len(self.grid)
    def set(self, x, y, val):
        self.grid[y] = self.grid[y][:]
        self.grid[y][x] = val
    def set2(self, val):
        self.set(self.x, self.y, val)

class GridSolver:

    #Subclass must implement these functions as needed
    def get_next_states(self, state):
        return []

    def check_state(self, state):
        return True

    def check_finish(self, state):
        return True

    #Solving functions

    def solve_iterative(self, start_state, depth=100, debug=False, showprogress=False):
        print("Solving...")
        self.count_iterate = 0
        self.solution = None
        start_time = time.time()
        start_state.x = start_state.y = 0
        state = self._solve_iterative(start_state, depth, debug, showprogress)
        elapsed = time.time() - start_time
        if state == None:
            print("No solution exists.")
        else:
            print(state)
        print("Solved in {:.2f} seconds".format(elapsed))
        print(f"{self.count_iterate} iterations.")

    def _solve_iterative(self, state, max_depth, debug, showprogress):
        state.x = state.y = 0
        depth = 0
        open_space = False
        while not self.solution:
            if state.grid[state.y][state.x] == 0:
                self.count_iterate += 1
                if showprogress and self.count_iterate % 20000 == 0:
                    print(state)
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
                        result = self._solve_iterative(s, depth-1, debug, showprogress)
                        if result:
                            if nextSol:
                                open_space = True
                                break
                            nextSol = s
                    else:
                        if nextSol == None:
                            return None
                        self.count_iterate += 1
                        if showprogress and self.count_iterate % 20000 == 0:
                            print(state)
                        open_space = False
                        state = nextSol
                        if debug:
                            print("Answer found at depth", depth, "("+str(state.x)+', '+str(state.y)+")")
                            input(state)
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
                if debug:
                    print("Could not solve at current depth", depth, "- increase depth")
                    input(state)
                depth += 1
                state.x = state.y = 0
        return self.solution

    def solve_recursive(self, starting_state, debug=0): #State must have "grid", "x", and "y" variables
        print("Solving...")
        self.count_recurse = -1
        start_time = time.time()
        starting_state.x = starting_state.y = 0
        state = self._solve_recursive(starting_state, debug)
        elapsed = time.time() - start_time
        if state is None:
            print("No solution exists.")
        else:
            print(state)
        print("Solved in {:.2f} seconds".format(elapsed))
        print(f"{self.count_recurse} recursions.")
        return state

    def _solve_recursive(self, state, debug=0):
        if debug:
            input(state)
        self.count_recurse += 1
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
            if not self.check_state(s):
                continue
            result = self._solve_recursive(s, debug)
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


def parse_edges(edgestr, place_endpoints=False, close_empty_edges=True):
    global _roomi
    _roomi = 2 if place_endpoints else 1
    edges = _parse_edges(0, [c for c in edgestr], 1 if place_endpoints else None, place_endpoints)
    if close_empty_edges: edges = epsilon_closure(edges)
    roomi = [e[0] for e in edges if e[0] is not None] + [e[2] for e in edges if e[2] is not None]
    roomi = sorted(list(set(roomi)))
    edges = [(roomi.index(s) if s is not None else s, c, roomi.index(e) if e is not None else e) for s, c, e in edges]
    return edges
def _parse_edges(start, edgechar, end, place_endpoints=False):
    global _roomi
    new = []
    edge = ''
    newstart = start
    while edgechar and edgechar[0] != ')':
        c = edgechar.pop(0)
        if c == '|':
            new.append((newstart, edge, end))
            edge = ''
            newstart = start
        if c == '(':
            new.append((newstart, edge, _roomi))
            edge = ''
            newstart = _roomi
            newend = _roomi + 1
            _roomi += 2
            newedges = _parse_edges(newstart, edgechar, newend)
            if not (edgechar and edgechar[0] not in ')|'):
                for i, e in enumerate(newedges):
                    if e[2] == newend:
                        if place_endpoints:
                            newedges[i] = (e[0], e[1], _roomi)
                            _roomi += 1
                        else: newedges[i] = (e[0], e[1], None)
            new += newedges
            newstart = newend
        if c not in '|() ':
            edge += c
    if edgechar: edgechar.pop(0)
    new.append((newstart, edge, end))
    return new
def epsilon_closure(edges):
    epsilon = [e for e in edges if len(e[1]) == 0 and e[2] is not None]
    edges = [e for e in edges if len(e[1]) > 0]
    initial_edges = edges[:]
    for start, _, end in epsilon:
        for i, e in enumerate(edges):
            if e[0] == end: edges[i] = (start, e[1], e[2])
            if e[2] == end: edges[i] = (e[0], e[1], start)
    if edges != initial_edges:
        return epsilon_closure(edges + epsilon)
    return edges

WALL_UP = 1
WALL_RIGHT = 2
WALL_DOWN = 4
WALL_LEFT = 8
#Open up = 14
#Open right = 13
#Open down = 11
#Open left = 7

DLEFT = Vec3(-1, 0, 0); DRIGHT = Vec3(1, 0, 0); DUP = Vec3(0, -1, 0); DDOWN = Vec3(0, 1, 0)
DBELOW = Vec3(0, 0, -1); DABOVE = Vec3(0, 0, 1); DZERO = Vec3(0, 0, 0)
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIRECTIONS3D = [DLEFT, DRIGHT, DUP, DDOWN]
DIRECTIONS8 = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
DIRECTIONS8_HALF = [(-1, 0), (-1, -1), (0, -1), (1, -1)]