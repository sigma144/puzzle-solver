import time, psutil, pickle
from dataclasses import dataclass
from collections import deque

class Catalog:
    catalog = used = None
    level = 0
    @staticmethod
    def init():
        Catalog.catalog = []; Catalog.used = {}
    @staticmethod
    def add(val):
        if val in Catalog.used:
            return Catalog.used[val]
        Catalog.catalog.append(val)
        Catalog.used[val] = len(Catalog.catalog) - 1
        return len(Catalog.catalog) - 1
    @staticmethod
    def sadd(val):
        sval = pickle.dumps(val)
        if sval in Catalog.used:
            return Catalog.used[sval]
        Catalog.catalog.append(val)
        Catalog.used[sval] = len(Catalog.catalog) - 1
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

class GridState:
    def __init__(self, grid):
        self._grid = grid.copy()
        self._vars = Catalog.sadd({})
        self._temp = {}
        self._score = 1
        self._packed = tuple(Catalog.tadd(row) for row in grid)
        self._write = set()
    def __hash__(self):
        if self._vars:
            return hash(self._grid) ^ hash(self._vars)
        return hash(self._grid)
    def __eq__(self, state):
        return self._grid == state._grid and self._vars == state._vars
    def __repr__(self):
        s = '\n'.join([''.join([s[0] for s in Catalog.get(row)]) for row in self._grid])
        if self._vars:
            s += '\nVars: ' + str(Catalog.get(self._vars))
        if hasattr(self, '_temp') and self._temp:
            s += '\nTemp: ' + str(self._temp)
        return s
    def copy(self):
        state = GridState.__new__(GridState)
        state._grid = self._grid.copy()
        state._vars = self._vars
        state._temp = self._temp
        state._score = 1
        state._packed = self._packed
        state._write = self._write.copy() if hasattr(self, '_write') else set()
        return state
    def pack(self):
        arr = [Catalog.tadd(row) if i in self._write else self._packed[i] for i, row in enumerate(self._grid)]
        self._grid = tuple(arr)
        del self._write, self._packed
    def unpack(self):
        self._packed = self._grid
        self._grid = [Catalog.get(n) for n in self._grid]
        self._readonly = True
    def repack(self):
        self._grid = self._packed
        del self._packed
    def get(self, x, y):
        if y < 0 or x < 0 or y >= len(self._grid) or x >= len(self._grid[y]):
            return None
        return self._grid[y][x]
    def set(self, x, y, val):
        if hasattr(self, '_readonly'): raise Exception('State is read only')
        self._grid[y] = self._grid[y].copy()
        self._grid[y][x] = val
        self._write.add(y)
    def set_and_track(self, x, y, val):
        if hasattr(self, '_readonly'): raise Exception('State is read only')
        self._grid[y] = self._grid[y].copy()
        self._grid[y][x] = val
        self._temp = self._temp.copy()
        self._temp[val] = (x, y)
        self._write.add(y)
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
        if val in self._temp:
            return self._temp[val]
        for y in range(len(self._grid)):
            for x in range(len(self._grid[y])):
                if self._grid[y][x] == val:
                    self._temp = self._temp.copy()
                    self._temp[val] = (x, y)
                    return (x, y)
    def count(self, val):
        total = 0
        for y in range(len(self._grid)):
            for x in range(len(self._grid[y])):
                if self._grid[y][x] == val:
                    total += 1
        return total
    def get_var(self, var):
        return Catalog.get(self._vars).get(var)
    def set_var(self, var, val):
        if hasattr(self, '_readonly'): raise Exception('State is read only')
        self._vars = Catalog.get(self._vars).copy()
        self._vars[var] = val
        self._vars = Catalog.sadd(self._vars)
    def inc_var(self, var, num=1):
        if hasattr(self, '_readonly'): raise Exception('State is read only')
        self._vars = Catalog.get(self._vars).copy()
        self._vars[var] += num
        self._vars = Catalog.sadd(self._vars)
    def dec_var(self, var, num=1):
        if hasattr(self, '_readonly'): raise Exception('State is read only')
        self._vars = Catalog.get(self._vars).copy()
        self._vars[var] -= num
        self._vars = Catalog.sadd(self._vars)
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
    def solve_optimal(self, puzzle, debug=0, use_score=0, optimize_score=0, max_depth=0, **kwargs):
        start_time = time.time()
        Catalog.init()
        Solver.solver = self
        self.kwargs = kwargs
        self._puzzle = puzzle
        if optimize_score:
            use_score = True
        if debug:
            return self.debug()
        starting_state = self.setup(puzzle)
        starting_state.previous = None
        starting_state.pack()
        print(starting_state)
        print("Solving...")
        count_iterate = 0
        depth_time = time.time()
        depth_last = 0
        depth_size = 0
        depth_start = 0
        if max_depth == 0: max_depth = 999999999
        def finish_solve(state):
            state._write = {i for i in range(len(state._grid))}
            state.pack()
            elapsed = time.time() - start_time
            moves, names = self.trace_moves(state)
            print(' '.join(names))
            score = sum([s._score for s in moves[1:]])
            if optimize_score:
                print("Solved with score", str(score)+"!")
                print("Moves:", len(moves)-1)
            else:
                print("Solved in", len(moves)-1, "moves!")
                if use_score:
                    print("Score:", score)
            print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
            del self._prev_states, self._state_queue, self._next_queue
            self.replay_moves(moves)
            return moves
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
                        state.unpack()
                        if self.check_finish(state):
                            del state._temp
                            return finish_solve(state)
                        next = self.get_next_states(state)
                        state.repack()
                        for _, s in next.items():
                            s.previous = state
                            if optimize_score:
                                score = (self._depth[0] + s._score, self._depth[1] + 1)
                            else:
                                score = (self._depth[0] + 1, self._depth[1] + s._score)
                            if score[0] + self.lower_bound(s) > max_depth:
                                continue
                            s._score = score
                            s.pack()
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
                        del state._temp, state._readonly
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
                    state.unpack()
                    next = self.get_next_states(state)
                    state.repack()
                    for _, s in next.items():
                        s.previous = state
                        if self.check_finish(s):
                            del state._temp
                            del s._temp
                            return finish_solve(s)
                        if self._depth + self.lower_bound(s) > max_depth:
                            continue
                        s.pack()
                        if len(self._prev_states) != (self._prev_states.add(s) or len(self._prev_states)):
                            self._next_queue.appendleft(s)
                        del s._score
                    if count_iterate % 50000 == 0:
                        memuse = int(psutil.virtual_memory()[2])
                        print(state)
                        print("Depth "+str(self._depth)+": " + str(int((count_iterate-depth_start)/depth_size*100)) + "%,", str(count_iterate // 1000) + "k states checked, total time {:.2f}s".format(time.time() - start_time) + ',', f'RAM {memuse}%,', "catalog size " + str(len(Catalog.catalog)))
                    del state._temp, state._readonly
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
        except FileNotFoundError as e:
            try:
                Catalog.pack(state)
                _, names = self.trace_moves(state)
                print(state)
                print(' '.join(names))
            except:
                print('<Tracing moves failed>')
            print("Exception thrown while solving!")
            print(repr(e))
            raise e
        except KeyboardInterrupt:
            print('Solve terminated.')
            print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
            return []
        print("No solution exists.")
        elapsed = time.time() - start_time
        print(count_iterate, "iterations,", "{:.2f} seconds.".format(elapsed))
        return []
    def trace_moves(self, s):
        moves = [s]
        while s.previous is not None:
            moves.insert(0, s.previous)
            s = s.previous
        names = []
        if moves:
            for m in moves:
                m.unpack()
                m._temp = {}
            new_list = [self.setup(self._puzzle)]
            for m in moves[1:]:
                states = self.get_next_states(new_list[-1])
                for k,v in states.items():
                    if v == m:
                        names.append(str(k))
                        new_list.append(v)
                        break
                else:
                    print('Tracing moves failed! Check for accidental mutation of state in get_next_states.')
                    break
            for m in moves:
                m.repack()
            moves = new_list
            for m in moves:
                m._write = {i for i in range(len(m._grid))}
                m.pack()
                del m._temp
        return moves, names
    def replay_moves(self, moves, diff=1, diff_trail=0):
        if not diff:
            for m, _ in moves:
                print(m)
                input()
            return
        strs = [str(m) for m in moves]
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
            input()
            print(newstr)
    def debug(self):
        prev_moves = []
        state = self.setup(self._puzzle)
        state.previous = None
        move_input = None
        while True:
            finished = self.check_finish(state)
            if finished: moves = {}
            else: moves = self.get_next_states(state)
            state.pack()
            moves = {str(k):v for k,v in moves.items()}
            for v in moves.values():
                v.pack()
                v.previous = state
            if not move_input:
                print(state)
                if prev_moves: print('Moves: ' + ' '.join(prev_moves))
            if finished:
                print(Solver._green + f'Puzzle solved in {len(prev_moves)} moves!' + Solver._black)
                moves, _ = self.trace_moves(state)
                self.replay_moves(moves)
                return
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
                else:
                    move_input = None
                    break
            if move:
                prev_moves.append(move)
                state = moves[move]
            state.unpack()
    
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