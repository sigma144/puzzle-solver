import time, psutil, pickle
from dataclasses import dataclass
from collections import deque

class Catalog:
    catalog = used = None
    level = 0
    @staticmethod
    def init(lvl=1):
        Catalog.catalog = [None]; Catalog.used = {}
        Catalog.set_compression_level(lvl)
    @staticmethod
    def add(val):
        if val in Catalog.used:
            return Catalog.used[val]
        Catalog.catalog.append(val)
        Catalog.used[val] = len(Catalog.catalog) - 1
        return len(Catalog.catalog) - 1
    @staticmethod
    def tadd(val):
        tval = tuple(val)
        if tval in Catalog.used:
            return Catalog.used[tval]
        Catalog.catalog.append(val)
        Catalog.used[tval] = len(Catalog.catalog) - 1
        return len(Catalog.catalog) - 1
    @staticmethod
    def get(num):
        return Catalog.catalog[num]
    @staticmethod
    def pack0(state):
        state._grid = tuple(tuple(row) for row in state._grid)
    @staticmethod
    def unpack0(state):
        array = state._grid
        state._grid = list(list(row) for row in state._grid)
        state._readonly = True
        return array
    @staticmethod
    def pack1(state):
        arr = [Catalog.tadd(row) for row in state._grid]
        state._grid = tuple(arr)
        return
    @staticmethod
    def unpack1(state):
        array = state._grid
        grid = [Catalog.get(n) for n in array]
        state._grid = grid
        state._readonly = True
        return array
    @staticmethod
    def pack2(state):
        num = 0
        for row in state._grid[::-1]:
            num <<= 16
            num |= Catalog.tadd(row)
        state._grid = num
        return
    @staticmethod
    def unpack2(state):
        array = state._grid
        grid = []
        while state._grid:
            grid.append(Catalog.get(state._grid & 0xFFFF))
            state._grid >>= 16
        state._grid = grid
        state._readonly = True
        return array
    @staticmethod
    def pack(state): pass
    @staticmethod
    def unpack(state): pass
    @staticmethod
    def set_compression_level(lvl):
        Catalog.level = lvl
        if lvl == 0:
            Catalog.pack = Catalog.pack0
            Catalog.unpack = Catalog.unpack0
        elif lvl == 1:
            Catalog.pack = Catalog.pack1
            Catalog.unpack = Catalog.unpack1
        elif lvl == 2:
            Catalog.pack = Catalog.pack2
            Catalog.unpack = Catalog.unpack2

class GridState:
    def __init__(self, grid):
        self._grid = grid.copy()
        self._vars = {}
        self._track = {}
        self._temp = {}
        self._score = 1
    def __hash__(self):
        if self._vars:
            return hash(self._grid) ^ hash(pickle.dumps(self._vars))
        return hash(self._grid)
    def __eq__(self, state):
        return self._grid == state._grid and self._vars == state._vars
    def __repr__(self):
        array = Catalog.unpack(self)
        s = '\n'.join([''.join([s[0] for s in row]) for row in self._grid])
        if self._vars:
            s += '\nVars: ' + str(self._vars)
        if hasattr(self, '_temp') and self._temp:
            s += '\nTemp: ' + str(self._temp)
        self._grid = array
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
    def set_score(self, val):
        self._score = val

class Solver:
    def setup(self, puzzle): return puzzle #Override if initial setup is necessary
    def get_next_states(self, state): return {} #Must override
    def check_finish(self, state): return False #Must override
    def lower_bound(self, state): return 0 #(Optional) Minimum moves to solve
    _red = '\033[91m'; _blue = '\033[94m'; _black = '\033[00m'; _green = '\033[92m'
    solver = None
    def solve_optimal(self, puzzle, debug=0, use_score=0, optimize_score=0, max_depth=0, compression=1, **kwargs):
        start_time = time.time()
        Catalog.init(compression)
        Solver.solver = self
        self.kwargs = kwargs
        self._puzzle = puzzle
        if optimize_score:
            use_score = True
        if debug:
            return self.debug()
        starting_state = self.setup(puzzle)
        starting_state.previous = None
        Catalog.pack(starting_state)
        print(starting_state)
        print("Solving...")
        count_iterate = 0
        depth_time = time.time()
        depth_last = 0
        depth_size = 0
        depth_start = 0
        if max_depth == 0: max_depth = 999999999
        def finish_solve(state):
            Catalog.pack(state)
            elapsed = time.time() - start_time
            move_list, _ = self.trace_moves(state)
            score = sum([s._score for s in move_list[1:]])
            if optimize_score:
                print("Solved with score", str(score)+"!")
                print("Moves:", len(move_list)-1)
            else:
                print("Solved in", len(move_list)-1, "moves!")
                if use_score:
                    print("Score:", score)
            print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
            del self._prev_states, self._state_queue, self._next_queue
            return move_list
        try:
            if use_score:
                self._prev_states = {starting_state: starting_state}
                self._state_queue = deque()
                self._state_queue.append(starting_state)
                self._next_queue = {(0, 0): self._state_queue}
                self._depth = (0, 0)
                starting_state._score = (0, 0)
                while True:
                    count_iterate += 1
                    state = self._state_queue.pop()
                    if state._score is not None:
                        del state._score
                        packed_array = Catalog.unpack(state)
                        if self.check_finish(state):
                            del state._temp, state._track
                            return finish_solve(state)
                        next = self.get_next_states(state)
                        state._grid = packed_array
                        for _, s in next.items():
                            s.previous = state
                            if optimize_score:
                                score = (self._depth[0] + s._score, self._depth[1] + 1)
                            else:
                                score = (self._depth[0] + 1, self._depth[1] + s._score)
                            if score[0] + self.lower_bound(s) > max_depth:
                                continue
                            s._score = score
                            Catalog.pack(s)
                            if self._prev_states.setdefault(s, s) is s:
                                self._next_queue.setdefault(score, deque()).appendleft(s)
                                if score[0] == self._depth[0]:
                                    depth_size += 1
                            else:
                                existing_state = self._prev_states[s]
                                if score < getattr(existing_state, '_score', (-1, -1)):
                                    existing_state._score = None
                                    self._prev_states[s] = s
                                    self._next_queue.setdefault(score, deque()).appendleft(s)
                                    if score[0] == self._depth[0]:
                                        depth_size += 1
                        if count_iterate % 50000 == 0:
                            memuse = int(psutil.virtual_memory()[2])
                            print(state)
                            print("Depth "+str(self._depth[0])+": " + str(int((count_iterate-depth_start)/depth_size*100)) + "%,", str(count_iterate // 1000) + "k states checked, total time {:.2f}s".format(time.time() - start_time) + ',', f'RAM {memuse}%,', "catalog size " + str(len(Catalog.catalog)))
                        del state._temp, state._track, state._readonly
                    if len(self._state_queue) == 0:
                        #self._prev_states = set()
                        del self._next_queue[self._depth]
                        if len(self._next_queue) == 0: break #No solution found
                        least_score = min(self._next_queue.keys())
                        self._state_queue = self._next_queue[least_score]
                        if self._depth[0] != least_score[0]:
                            self._depth = least_score
                            depth_size = sum({len(q) for sc, q in self._next_queue.items() if sc[0] == least_score[0]})
                            depth_start = count_iterate
                            elapsed = time.time() - depth_time
                            time_diff = elapsed - depth_last
                            depth_last = elapsed
                            depth_time = time.time()
                            print("Depth "+str(self._depth[0])+': '+str(count_iterate)+' iterations, {:.2f}s, '.format(time.time()-start_time) \
                                +"depth time {:.2f}".format(elapsed)+'s '+(Solver._green if time_diff<0 else Solver._red) \
                                +'('+('+' if time_diff>=0 else '')+'{:.2f}s)'.format(time_diff)+Solver._black)
                        self._depth = least_score
            else:
                self._prev_states = {starting_state}   
                self._state_queue = [starting_state]
                self._next_queue = deque()
                self._depth = 0
                while True:
                    count_iterate += 1
                    state = self._state_queue.pop()
                    packed_array = Catalog.unpack(state)
                    next = self.get_next_states(state)
                    state._grid = packed_array
                    for _, s in next.items():
                        s.previous = state
                        if self.check_finish(s):
                            del state._temp, state._track
                            del s._temp, s._track
                            return finish_solve(s)
                        if self._depth + self.lower_bound(s) > max_depth:
                            continue
                        Catalog.pack(s)
                        if len(self._prev_states) != (self._prev_states.add(s) or len(self._prev_states)):
                            self._next_queue.appendleft(s)
                        del s._score
                    if count_iterate % 50000 == 0:
                        memuse = int(psutil.virtual_memory()[2])
                        print(state)
                        print("Depth "+str(self._depth)+": " + str(int((count_iterate-depth_start)/depth_size*100)) + "%,", str(count_iterate // 1000) + "k states checked, total time {:.2f}s".format(time.time() - start_time) + ',', f'RAM {memuse}%,', "catalog size " + str(len(Catalog.catalog)))
                    del state._temp, state._track, state._readonly
                    if len(self._state_queue) == 0:
                        #self._prev_states = set()
                        if len(self._next_queue) == 0: break #No solution found
                        self._state_queue = self._next_queue
                        self._next_queue = deque()
                        self._depth += 1
                        depth_size = len(self._state_queue)
                        depth_start = count_iterate
                        elapsed = time.time() - depth_time
                        time_diff = elapsed - depth_last
                        depth_last = elapsed
                        depth_time = time.time()
                        print("Depth "+str(self._depth)+': '+str(count_iterate)+' iterations, {:.2f}s, '.format(time.time()-start_time) \
                            +"depth time {:.2f}".format(elapsed)+'s '+(Solver._green if time_diff<0 else Solver._red) \
                            +'('+('+' if time_diff>=0 else '')+'{:.2f}s)'.format(time_diff)+Solver._black)
        except Exception as e:
            try:
                Catalog.pack(state)
                self.trace_moves(state)
            except:
                print('<Tracing moves failed>')
            print("Exception thrown while solving!")
            print(repr(e))
            raise e
        print("No solution exists.")
        elapsed = time.time() - start_time
        print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
        return []
    def trace_moves(self, s, prnt=1, diff=1, diff_trail=0):
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
        if move_list:
            packed_arrays = []
            for m in move_list:
                packed_arrays.append(Catalog.unpack(m))
                m._track = {}
                m._temp = {}
            names = []
            new_list = [self.setup(self._puzzle)]
            for m in move_list[1:]:
                states = self.get_next_states(new_list[-1])
                for k,v in states.items():
                    if v == m:
                        names.append(str(k))
                        new_list.append(v)
                        break
                else:
                    print('Tracing moves failed! Check for accidental mutation of state in get_next_states.')
                    break
            if prnt: print(' '.join(names))
            for i, m in enumerate(move_list):
                m._grid = packed_arrays[i]
            move_list = new_list
        return move_list, names
    def increase_compression(self):
        lvl = Catalog.level
        prev = self._prev_states
        self._prev_states = {}
        if lvl == 0:
            while prev:
                s = prev.pop()
                Catalog.pack1(s)
                self._prev_states.add(s)
        elif lvl == 1:
            while prev:
                s = prev.pop()
                Catalog.unpack1(s)
                Catalog.pack2(s)
                self._prev_states.add(s)
        else:
            print('STATES CANNOT BE FURTHER COMPRESSED')
            return
        Catalog.set_compression_level(lvl + 1)

    def debug(self):
        prev_moves = []
        state = self.setup(self._puzzle)
        state.previous = None
        move_input = None
        while True:
            finished = self.check_finish(state)
            if finished: moves = {}
            else: moves = self.get_next_states(state)
            Catalog.pack(state)
            moves = {str(k):v for k,v in moves.items()}
            for v in moves.values():
                Catalog.pack(v)
                v.previous = state
            print(state)
            if prev_moves: print('Moves: ' + ' '.join(prev_moves))
            if finished:
                print(Solver._green + f'Puzzle solved in {len(prev_moves)} moves!' + Solver._black)
            move = None
            while move not in moves:
                if not move_input:
                    move_input = input(' '.join(moves.keys()) + ': ')
                if not move_input:
                    if state.previous is not None:
                        state = state.previous
                        prev_moves.pop()
                    break
                for m in sorted(moves.keys(), key=len, reverse=True):
                    if move_input.startswith(m):
                        move = m
                        move_input = move_input[len(move)+1:]
                        break
                else: move_input = None
            if move:
                prev_moves.append(move)
                state = moves[move]
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