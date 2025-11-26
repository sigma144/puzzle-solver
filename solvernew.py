import time, psutil, pickle
from dataclasses import dataclass

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
    def tadd(val):
        global _catalog, _used
        tval = tuple(val)
        if tval in _used:
            return _used[tval]
        _catalog.append(val)
        _used[tval] = len(_catalog) - 1
        return len(_catalog) - 1
    @staticmethod
    def get(num):
        global _catalog
        return _catalog[num]
    @staticmethod
    def pack(state):
        assert isinstance(state._grid[0], list)
        arr = [Catalog.tadd(row) for row in state._grid]
        state._grid = tuple(arr)
        return
    @staticmethod
    def unpack(state):
        assert isinstance(state._grid[0], int)
        array = state._grid
        grid = [Catalog.get(n) for n in array]
        state._grid = grid
        state._readonly = True
        return array

class GridState:
    def __init__(self, grid):
        self._grid = grid.copy()
        self._vars = {}
        self._track = {}
        self._temp = {}
    def __hash__(self):
        if self._vars:
            return hash(self._grid) ^ hash(pickle.dumps(self._vars))
        return hash(self._grid)
    def __eq__(self, state):
        return self._grid == state._grid and self._vars == state._vars
    def __repr__(self):
        assert isinstance(self._grid[0], int)
        s = '\n'.join([''.join([s[0] for s in Catalog.get(row)]) for row in self._grid])
        if self._vars:
            s += '\nVars: ' + str(self._vars)
        if hasattr(self, '_temp') and self._temp:
            s += '\nTemp: ' + str(self._temp)
        return s
    def copy(self):
        state = GridState(self._grid)
        state._vars = self._vars
        state._track = self._track
        state._temp = self._temp
        return state
    def get(self, x, y):
        if y < 0 or x < 0 or y >= len(self._grid) or x >= len(self._grid[y]):
            return None
        return self._grid[y][x]
    def set(self, x, y, val):
        if hasattr(self, '_readonly'): raise Exception('State is read only')
        self._grid[y] = self._grid[y].copy()
        self._grid[y][x] = val
    def set_and_track(self, x, y, val):
        if hasattr(self, '_readonly'): raise Exception('State is read only')
        self._grid[y] = self._grid[y].copy()
        self._grid[y][x] = val
        self._track = self._track.copy()
        self._track[val] = (x, y)
    def size(self):
        return len(self._grid[0]), len(self._grid)
    def all_points(self):
        class Gen:
            def __init__(s):
                s.x = 0; s.y = 0
                s.width = len(self._grid[0])
                s.height = len(self._grid)
            def __iter__(s):
                while True:
                    yield (s.x, s.y)
                    s.x += 1
                    if s.x >= s.width:
                        s.x = 0
                        s.y += 1
                        if s.y >= s.height:
                            break
        return Gen()
    def find(self, val, index=None):
        if index is not None:
            for y in range(len(self._grid)):
                for x in range(len(self._grid[y])):
                    if self._grid[y][x][index] == val:
                        return (x, y)
        for y in range(len(self._grid)):
            for x in range(len(self._grid[y])):
                if self._grid[y][x] == val:
                    return (x, y)
    def find_and_track(self, val):
        if val in self._track:
            return self._track[val]
        for y in range(len(self._grid)):
            for x in range(len(self._grid[y])):
                if self._grid[y][x] == val:
                    self._track = self._track.copy()
                    self._track[val] = (x, y)
                    return (x, y)
    def count(self, val):
        total = 0
        for y in range(len(self._grid)):
            for x in range(len(self._grid[y])):
                if self._grid[y][x] == val:
                    total += 1
        return total
    def get_var(self, var):
        return self._vars.get(var)
    def set_var(self, var, val):
        if hasattr(self, '_readonly'): raise Exception('State is read only')
        self._vars = self._vars.copy()
        self._vars[var] = val
    def inc_var(self, var, num=1):
        if hasattr(self, '_readonly'): raise Exception('State is read only')
        self._vars = self._vars.copy()
        self._vars[var] += num
    def dec_var(self, var, num=1):
        if hasattr(self, '_readonly'): raise Exception('State is read only')
        self._vars = self._vars.copy()
        self._vars[var] -= num
    def get_temp(self, var):
        return self._temp.get(var)
    def set_temp(self, var, val):
        self._temp = self._temp.copy()
        self._temp[var] = val
    def inc_temp(self, var, num=1):
        if var not in self._temp: return
        self._temp = self._temp.copy()
        self._temp[var] += num
    def dec_temp(self, var, num=1):
        if var not in self._temp: return
        self._temp = self._temp.copy()
        self._temp[var] -= num

class Solver:
    def setup(self, puzzle): return puzzle #Override if initial setup is necessary
    def get_next_states(self, state): return {} #Must override
    def check_finish(self, state): return False #Must override
    def score_state(self, state): return None #Optimize value other than move count
    _red = '\033[91m'; _blue = '\033[94m'; _black = '\033[00m'; _green = '\033[92m'
    solver = None
    def solve_optimal(self, puzzle, debug=0, use_score=0, optimize_score=0, **kwargs):
        start_time = time.time()
        Catalog.init()
        Solver.solver = self
        self.kwargs = kwargs
        self._puzzle = puzzle
        if debug:
            return self.debug()
        starting_state = self.setup(puzzle)
        starting_state.previous = None
        Catalog.pack(starting_state)
        print(starting_state)
        print("Solving...")
        self._prev_states = {starting_state}
        self._state_queue = [starting_state]
        self._next_queue = []
        self._depth = 0
        self._score = 0
        best_score = None
        best_state = None
        count_iterate = 0
        depth_time = time.time()
        depth_last = 0
        depth_size = 0
        depth_start = 0
        self._solving = True
        if use_score or optimize_score: #Check
            use_score = True
            starting_state._invalidate = False
            score = (0, self.score_state(starting_state))
            if optimize_score: score = (score[1], score[0])
            self._prev_states = {starting_state: (starting_state, score)}
            self._next_queue = {score: self._state_queue}
            self._score = score
        def finish_solve(state):
            elapsed = time.time() - start_time
            move_list = self.trace_moves(state)
            if optimize_score:
                print("Solved with score", str(self.score_state(state))+"!")
                print("Moves:", len(move_list)-1)
            else:
                print("Solved in", len(move_list)-1, "moves!")
                if self.score_state(state) is not None:
                    print("Score:", str(self.score_state(state)))
            print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
            return move_list
        try:
            if use_score:
                pass
            else:
                while self._solving:
                    count_iterate += 1
                    state = self._state_queue.pop()
                    packed_array = Catalog.unpack(state)
                    next = self.get_next_states(state)
                    for _, s in next.items():
                        s.previous = state
                        if self.check_finish(s):
                            state._grid = packed_array
                            del state._temp, state._track
                            del s._temp, s._track
                            return finish_solve(s)
                        Catalog.pack(s)
                        if len(self._prev_states) != (self._prev_states.add(s) or len(self._prev_states)):
                            self._next_queue.append(s)
                    state._grid = packed_array
                    if count_iterate % 50000 == 0:
                        print(state)
                        print("Depth "+str(self._depth)+": " + str(int((count_iterate-depth_start)/depth_size*100)) + "%,", str(count_iterate // 1000) + "k states checked, total time {:.2f}s".format(time.time() - start_time) + (", catalog size " + str(len(_catalog)) if _catalog else ""))
                        memuse = psutil.virtual_memory()[2]
                        if memuse >= 90:
                            print(Solver._red + "HIGH MEMORY USE, PERFORMANCE MAY BE SLOW" + Solver._black)
                    if len(self._state_queue) == 0:
                        #self._prev_states = set()
                        if len(self._next_queue) == 0: break
                        self._state_queue = self._next_queue
                        self._next_queue = []
                        self._depth += 1
                        depth_size = len(self._state_queue)
                        depth_start = count_iterate
                        elapsed = time.time() - depth_time
                        time_diff = elapsed - depth_last
                        depth_last = elapsed
                        depth_time = time.time()
                        print("Depth "+str(self._depth)+': '+str(count_iterate)+' iterations, {:.2f}s, '.format(time.time()-start_time)+"depth time {:.2f}".format(elapsed)+'s '+(Solver._green if time_diff<0 else Solver._red)+'('+('+' if time_diff>=0 else '')+'{:.2f}s)'.format(time_diff)+Solver._black)
                    del state._temp, state._track, state._readonly
        except Exception as e:
            self.trace_moves(state)
            print("Exception thrown while solving!")
            print(repr(e))
            raise e
        if self._solving:
            print("No solution exists.")
        else:
            print("Solve terminated.")
        if best_state is not None:
            print("Best state", best_state)
        elapsed = time.time() - start_time
        print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
        return []
    def trace_moves(self, s, prnt=1, diff=1, diff_trail=0, use_names=1):
        Catalog.pack(s)
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
                    print()
                    print(newstr)
            else:
                for m in move_list: print(m)
        if use_names and move_list:
            for m in move_list:
                Catalog.unpack(m)
                m._track = {}
                m._temp = {}
            names = []
            state = self.setup(self._puzzle)
            for m in move_list[1:]:
                states = self.get_next_states(state)
                for k,v in states.items():
                    if v == m:
                        names.append(str(k))
                        state = v
                        break
                else:
                    print('Tracing moves failed! Check for accidental mutation of state in get_next_states.')
                    break
            print(' '.join(names))
        return move_list
    def debug(self):
        moves = []
        state = self.setup(self._puzzle)
        state.previous = None
        while True:
            if self.check_finish(state): states = {}
            else: states = self.get_next_states(state)
            Catalog.pack(state)
            states = {str(k):v for k,v in states.items()}
            for k,v in states.items():
                #print(k)
                Catalog.pack(v)
                v.previous = state
                #print(v)
                #print()
            print(state)
            if moves: print('Moves: ' + ' '.join(moves))
            if self.check_finish(state):
                print(Solver._green + f'Puzzle solved in {len(moves)} moves!' + Solver._black)
            move = None
            while move not in states:
                move = input(' '.join(states.keys()) + ': ')
                if not move and state.previous is not None:
                    state = state.previous
                    moves.pop()
                    break
            if move:
                moves.append(move)
                state = states[move]
            Catalog.unpack(state)
    
@dataclass
class Vec2:
    x = 0; y = 0
    def __init__(self, x, y, z): self.x = x; self.y = y
    def __add__(self, v): return Vec3(self.x + v.x, self.y + v.y)
    def __sub__(self, v): return Vec3(self.x - v.x, self.y - v.y)
    def __mul__(self, v): return Vec3(self.x*v, self.y*v)
    def __neg__(self): return Vec3(-self.x, -self.y)
    def __repr__(self): return f"({self.x}, {self.y})"
    def __iter__(self): return iter((self.x, self.y))
    def __hash__(self): return hash((self.x, self.y))
    def __eq__(self, v): return isinstance(v, Vec3) and v.x == self.x and v.y == self.y
    def __lt__(self, v): return self.y < v.y if self.y != v.y else self.x < v.x
    def __ge__(self, v): return self.y > v.y if self.y != v.y else self.x >= v.x
    def __contains__(self, v): return 0 <= v.x < self.x and 0 <= v.y < self.y

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

DLEFT = Vec3(-1, 0, 0); DRIGHT = Vec3(1, 0, 0); DUP = Vec3(0, -1, 0); DDOWN = Vec3(0, 1, 0)
DBELOW = Vec3(0, 0, -1); DABOVE = Vec3(0, 0, 1); DZERO = Vec3(0, 0, 0)
DIRECTIONS = {'>':(1, 0), 'v':(0, 1), '<':(-1, 0), '^':(0, -1)}
DIRECTIONS3D = [DLEFT, DRIGHT, DUP, DDOWN]
DIRECTIONS8 = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
DIRECTIONS8_HALF = [(-1, 0), (-1, -1), (0, -1), (1, -1)]