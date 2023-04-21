import pickle
from solver import Solver

trapsL = trapsR = trapsU = trapsD = []

class AbridgeState:
    def __hash__(self):
        return hash(pickle.dumps(self.board))
    def __eq__(self, state):
        return self.board == state.board
    def __repr__(self) -> str:
        return '\n'.join([''.join(row) for row in self.board])
    def set(self, x, y, val):
        self.board[y] = self.board[y][:]
        self.board[y][x] = val
    def copy(self):
        state = AbridgeState()
        state.board = self.board[:]
        state.tiles_left = self.tiles_left
        state.circles_left = self.circles_left
        return state
    def push(self, x, y, dx, dy):
        nextx, nexty = x+dx, y+dy
        if self.board[nexty][nextx] == '#':
            return False
        if self.board[y][x] == '#' or self.board[y][x] == '*':
            return self.push(nextx, nexty, dx, dy)
        elif self.board[nexty][nextx] == ' ':
            if self.circles_left == 0:
                if self.board[y][x] == '^' and trapsU[nexty][nextx] or \
                    self.board[y][x] == 'v' and trapsD[nexty][nextx] or \
                    self.board[y][x] == '<' and trapsL[nexty][nextx] or \
                    self.board[y][x] == '>' and trapsR[nexty][nextx]:
                    return False
                if self.board[y][x] == 'X':
                    if trapsU[nexty][nextx] or trapsD[nexty][nextx] or \
                        trapsL[nexty][nextx] or trapsR[nexty][nextx]:
                        return False
            self.set(nextx, nexty, self.board[y][x])
            self.set(x, y, ' ')
            return True
        elif self.board[nexty][nextx] == '*':
            if self.board[y][x] == 'O' or self.board[y][x] == 'F':
                #Trap check
                if self.circles_left == 1:
                    for y2 in range(len(self.board)):
                        for x2 in range(len(self.board[0])):
                            if x2 == x-dx and y2 == y-dy: continue
                            if self.board[y2][x2] == '^' and trapsU[y2][x2] or \
                            self.board[y2][x2] == 'v' and trapsD[y2][x2] or \
                            self.board[y2][x2] == '<' and trapsL[y2][x2] or \
                            self.board[y2][x2] == '>' and trapsR[y2][x2]:
                                return False
                            if self.board[y2][x2] == 'X':
                                if trapsU[y2][x2] or trapsD[y2][x2] or \
                                    trapsL[y2][x2] or trapsR[y2][x2]:
                                    return False
                self.circles_left -= 1
            self.set(x, y, ' ')
            self.tiles_left -= 1
            return True
        else:
            if not self.push(nextx, nexty, dx, dy):
                return False
            self.set(nextx, nexty, self.board[y][x])
            self.set(x, y, ' ')
            return True
    def copy_and_push(self, x, y, dx, dy, corrupt=False, mirror=False, mirror_pull=False):
        new_state = self.copy()
        result = new_state.push(x, y, dx, dy)
        if not result: return None
        if mirror:
            pair = self.find_mirror_symbol(x, y)
            if pair is None:
                new_state.set(x+dx, y+dy, {'U':'^','D':'v','L':'<','R':'>','W':'B','S':'Y','l':'{','r':'}','u':'+','d':'-','w':'b','s':'y','*':'*'}[new_state.board[y+dy][x+dx]])
                if corrupt: new_state.set(x, y, '#')
                return new_state
            x2, y2 = pair
            dx2, dy2 = dx, dy
            if self.board[y2][x2].upper() == 'U': dx2, dy2 = (0, -1)
            elif self.board[y2][x2].upper() == 'D': dx2, dy2 = (0, 1)
            elif self.board[y2][x2].upper() == 'L': dx2, dy2 = (-1, 0)
            elif self.board[y2][x2].upper() == 'R': dx2, dy2 = (1, 0)
            result = new_state.push(x2, y2, dx2, dy2)
            if not result: return None
            if new_state.board[y2+dy2][x2+dx2] in 'wslrud': new_state.set(x2,y2, '#')
        if mirror_pull:
            pair = self.find_mirror_symbol(x+dx, y+dy)
            if pair is None:
                if new_state.board[y+dy+dy][x+dx+dx] == 'F':
                    new_state.set(x+dx+dx, y+dy+dy, 'O')
                return new_state
            x2, y2 = pair
            result = new_state.push(x2-dx, y2-dy, dx, dy)
            if not result: return None
        if corrupt: new_state.set(x, y, '#')
        return new_state
    def can_escape(self, x, y, dx, dy):
        if self.board[y][x] == '*' or self.board[y][x] == "#" \
            or self.board[y-dy][x-dx] != '#':
            return True
        for dx2, dy2 in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if dx2 == dx or dy2 == dy: continue
            if self.board[y-dy2][x-dx2] == '#' and self.board[y-dy-dy2][x-dx-dx2] == '#': continue
            x2 = x; y2 = y
            while self.board[y2][x2] != '#':
                if self.board[y2-dy][x2-dx] != '#':
                    return True
                if self.board[y2-dy-dy2][x2-dx-dx2] != '#' and self.board[y2+dy+dy2][x2+dx+dx2] != '#':
                    return True
                if self.board[y2][x2] == '*':
                    return True
                x2 += dx2; y2 += dy2
        return False
    def find_mirror_symbol(self, x, y):
        symbol = self.board[y][x].upper()
        for y2 in range(len(self.board)):
            for x2 in range(len(self.board[0])):
                if x == x2 and y == y2: continue
                if self.board[y2][x2].upper() == symbol or self.board[y2][x2].upper() in 'UDLR' and symbol in 'UDLR':
                    return x2, y2
        return None

class AbridgeSolver(Solver):
    def solve(self, board):
        starting_state = AbridgeState()
        starting_state.board = [row[:] for row in board]
        starting_state.tiles_left = sum([sum([val not in ' #*' for val in row]) for row in board])
        starting_state.circles_left = sum([sum([val == 'O' or val == 'F' for val in row]) for row in board])
        self.detect_traps(starting_state)
        self.corrupt_states = {}
        #print(trapsD); print(trapsL); print(trapsR); print(trapsU)
        self.solve_optimal(starting_state)
        #self.solve_optimal_debug(starting_state)
    def get_next_states(self, state):
        states = []
        for y, row in enumerate(state.board):
            for x, val in enumerate(row):
                #if val == 'X':
                #    if (state.board[y-1][x] == '#' or state.board[y+1][x] == '#') and \
                #        (state.board[y][x-1] == '#' or state.board[y][x+1] == '#'):
                #        return []
                if val == ' ' or val == '#' or val == '*' or val == 'X':
                    continue
                if val == '^':
                    states.append(state.copy_and_push(x, y, 0, -1))
                elif val == '<':
                    states.append(state.copy_and_push(x, y, -1, 0))
                elif val == '>':
                    states.append(state.copy_and_push(x, y, 1, 0))
                elif val == 'v':
                    states.append(state.copy_and_push(x, y, 0, 1))
                elif val == 'B':
                    states.append(state.copy_and_push(x, y, 0, -1))
                    states.append(state.copy_and_push(x, y, -1, 0))
                    states.append(state.copy_and_push(x, y, 1, 0))
                    states.append(state.copy_and_push(x, y, 0, 1))
                elif val == 'Y':
                    states.append(state.copy_and_push(x, y, -1, -1))
                    states.append(state.copy_and_push(x, y, -1, 1))
                    states.append(state.copy_and_push(x, y, 1, -1))
                    states.append(state.copy_and_push(x, y, 1, 1))
                elif val == 'O':
                    states.append(state.copy_and_push(x, y+1, 0, -1))
                    states.append(state.copy_and_push(x+1, y, -1, 0))
                    states.append(state.copy_and_push(x-1, y, 1, 0))
                    states.append(state.copy_and_push(x, y-1, 0, 1))
                #Corrupted
                elif val == '+':
                    states.append(state.copy_and_push(x, y, 0, -1, corrupt=True))
                elif val == '{':
                    states.append(state.copy_and_push(x, y, -1, 0, corrupt=True))
                elif val == '}':
                    states.append(state.copy_and_push(x, y, 1, 0, corrupt=True))
                elif val == '-':
                    states.append(state.copy_and_push(x, y, 0, 1, corrupt=True))
                elif val == 'b':
                    states.append(state.copy_and_push(x, y, 0, -1, corrupt=True))
                    states.append(state.copy_and_push(x, y, -1, 0, corrupt=True))
                    states.append(state.copy_and_push(x, y, 1, 0, corrupt=True))
                    states.append(state.copy_and_push(x, y, 0, 1, corrupt=True))
                    if states[-1] is None and states[-2] is None and states[-3] is None and states[-4] is None:
                        if (state.board[y-1][x-1] == '#' or state.board[y+1][x+1] == '#') and \
                            (state.board[y+1][x-1] == '#' or state.board[y-1][x+1] == '#'):
                            return []
                elif val == 'y':
                    states.append(state.copy_and_push(x, y, -1, -1, corrupt=True))
                    states.append(state.copy_and_push(x, y, -1, 1, corrupt=True))
                    states.append(state.copy_and_push(x, y, 1, -1, corrupt=True))
                    states.append(state.copy_and_push(x, y, 1, 1, corrupt=True))
                    if states[-1] == None and states[-2] == None and states[-3] == None and states[-4] == None:
                        if (state.board[y-1][x] == '#' or state.board[y+1][x] == '#') and \
                            (state.board[y][x-1] == '#' or state.board[y][x+1] == '#'):
                            return []
                #Mirror
                elif val == 'U':
                    states.append(state.copy_and_push(x, y, 0, -1, mirror=True))
                elif val == 'L':
                    states.append(state.copy_and_push(x, y, -1, 0, mirror=True))
                elif val == 'R':
                    states.append(state.copy_and_push(x, y, 1, 0, mirror=True))
                elif val == 'D':
                    states.append(state.copy_and_push(x, y, 0, 1, mirror=True))
                elif val == 'W':
                    states.append(state.copy_and_push(x, y, 0, -1, mirror=True))
                    states.append(state.copy_and_push(x, y, -1, 0, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, 0, mirror=True))
                    states.append(state.copy_and_push(x, y, 0, 1, mirror=True))
                elif val == 'S':
                    states.append(state.copy_and_push(x, y, -1, -1, mirror=True))
                    states.append(state.copy_and_push(x, y, -1, 1, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, -1, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, 1, mirror=True))
                elif val == 'F':
                    states.append(state.copy_and_push(x, y+1, 0, -1, mirror_pull=True))
                    states.append(state.copy_and_push(x+1, y, -1, 0, mirror_pull=True))
                    states.append(state.copy_and_push(x-1, y, 1, 0, mirror_pull=True))
                    states.append(state.copy_and_push(x, y-1, 0, 1, mirror_pull=True))
                #Corrupted mirror
                elif val == 'u':
                    states.append(state.copy_and_push(x, y, 0, -1, corrupt=True, mirror=True))
                elif val == 'l':
                    states.append(state.copy_and_push(x, y, -1, 0, corrupt=True, mirror=True))
                elif val == 'r':
                    states.append(state.copy_and_push(x, y, 1, 0, corrupt=True, mirror=True))
                elif val == 'd':
                    states.append(state.copy_and_push(x, y, 0, 1, corrupt=True, mirror=True))
                elif val == 'w':
                    states.append(state.copy_and_push(x, y, 0, -1, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, -1, 0, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, 0, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, 0, 1, corrupt=True, mirror=True))
                elif val == 's':
                    states.append(state.copy_and_push(x, y, -1, -1, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, -1, 1, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, -1, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, 1, corrupt=True, mirror=True))
        #return [s for s in states if s != None and self.check_corrupt_redundancy(s)]
        return [s for s in states if s is not None]
    def detect_traps(self, state):
        global trapsL; trapsL = [[True for _ in row] for row in state.board]
        global trapsR; trapsR = [[True for _ in row] for row in state.board]
        global trapsU; trapsU = [[True for _ in row] for row in state.board]
        global trapsD; trapsD = [[True for _ in row] for row in state.board]
        for y, row in enumerate(state.board):
            for x, _ in enumerate(row):
                trapsL[y][x] = not state.can_escape(x, y, 1, 0)
                trapsR[y][x] = not state.can_escape(x, y, -1, 0)   
                trapsU[y][x] = not state.can_escape(x, y, 0, 1)   
                trapsD[y][x] = not state.can_escape(x, y, 0, -1)
        #print(trapsL); print(trapsR); print(trapsU); print(trapsD) 
    def check_corrupt_redundancy(self, state):
        state2 = state.copy()
        state2.board = [[' ' if t == '#' else t for t in row] for row in state.board]
        h = hash(state2)
        if h in self.corrupt_states:
            return False
            for s in self.corrupt_states[h]:
                if self.is_subset(s, state):
                    #if hash(s) != hash(state):
                    #    input(str(s)+"\n"+str(state) + "Subset, Skip 2nd")
                    return False
                #else:
                #    input(str(s)+"\n"+str(state) + "Not subset")
            for s in self.corrupt_states[h][:]:
                if self.is_subset(state, s):
                    #input(str(s)+"\n"+str(state) + "Superset, erase 1st")
                    self.corrupt_states[h].remove(s)
            self.corrupt_states[h].append(state)
            #print(len(self.corrupt_states[h]))
            #input(str(state)+"\nAdd")
        else:
            self.corrupt_states[h] = [state]
            #input(str(state)+"\nAdd (First)")
        return True

    def is_subset(self, state1, state2):
        for row1, row2 in zip(state1.board, state2.board):
            for t1, t2 in zip(row1, row2):
                if t1 == '#' and t2 != '#':
                    return False
        return True

    def check_finish(self, state):
        return state.tiles_left <= 0

puzzle_doubles = [ #Failed
    ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
    ['#','#','#','v','v',' ',' ',' ',' ','#','#','#','#','#','#'],
    ['#','#','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ','#','v','v','#','#','#'],
    ['#','#','#','#','#','#',' ',' ',' ',' ',' ',' ','#','#','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ','#','#','#','#','#','#'],
    ['#','#','#',' ',' ','>','<',' ',' ','#','#','#','#','#','#'],
    ['#','#','#','^','^',' ',' ','^','^','#','#','#','#','#','#'],
    ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
]

puzzle_zipper = [ #Failed
    ['#','#','#','#','#','#','#'],
    ['#','#',' ',' ',' ','#','#'],
    ['#','>',' ','Y',' ','#','#'],
    ['#','#',' ','Y',' ','<','#'],
    ['#','>',' ','v',' ','#','#'],
    ['#','#',' ',' ',' ','<','#'],
    ['#','#',' ','*',' ','#','#'],
    ['#','#','#','#','#','#','#'],
]

puzzle_follow_the_leader = [ #Failed
    ['#','#','#','#','#','#','#','#','#'],
    ['#',' ',' ',' ','#',' ',' ',' ','#'],
    ['#',' ','#',' ',' ',' ','*',' ','#'],
    ['#','^',' ',' ','#','v',' ',' ','#'],
    ['#',' ','#','#','#','#','#','#','#'],
    ['#',' ',' ','>',' ','<',' ',' ','#'],
    ['#',' ','#',' ','#',' ','#',' ','#'],
    ['#',' ','Y',' ','#',' ',' ','O','#'],
    ['#','#','#','#','#','#','#','#','#'],
]

puzzle_teamwork = [ #Failed
    ['#','#','#','#','#','#','#','#'],
    ['#',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ','#',' ','#',' ',' ','#'],
    ['#',' ','#','v','#',' ','B','#'],
    ['#',' ','O','#','^','#','#','#'],
    ['#','<',' ',' ',' ','Y','*','#'],
    ['#','#','#','#','#','#','#','#'],
]

puzzle_spiral = [ #Failed
    ['#','#','#','#','#','#','#','#','#'],
    ['#',' ',' ',' ',' ',' ','y',' ','#'],
    ['#','y',' ',' ','#',' ',' ',' ','#'],
    ['#',' ','#',' ',' ',' ','#',' ','#'],
    ['#','b',' ',' ','*',' ',' ','b','#'],
    ['#',' ','#',' ',' ',' ','#',' ','#'],
    ['#',' ',' ',' ','#',' ',' ','y','#'],
    ['#',' ','y',' ',' ',' ',' ',' ','#'],
    ['#','#','#','#','#','#','#','#','#'],
]

puzzle_scattered = [ #Failed
    ['#','#','#','#','#','#','#','#','#'],
    ['#','b',' ',' ',' ',' ',' ','b','#'],
    ['#',' ',' ','#','#','#',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ','y','#','*','y',' ',' ','#'],
    ['#',' ','-',' ','#',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ','#',' ',' ','#'],
    ['#','b',' ',' ','#',' ',' ','b','#'],
    ['#','#','#','#','#','#','#','#','#'],
]

puzzle_backstab = [ #Failed
    ['#','#','#','#','#','#','#','#','#'],
    ['#','B','X','#',' ','X',' ',' ','#'],
    ['#','#',' ','Y','#','#','X','#','#'],
    ['#','O',' ','X','#','X',' ',' ','#'],
    ['#','#',' ','#','#','#',' ','#','#'],
    ['#','#',' ',' ','#',' ',' ',' ','#'],
    ['#',' ',' ','*',' ',' ','#',' ','#'],
    ['#','#','#','#','#','#','#','#','#'],
]

puzzle_knockback = [ #Failed
    ['#','#','#','#','#','#','#'],
    ['#','>','>','X',' ','#','#'],
    ['#',' ','#','^',' ',' ','#'],
    ['#',' ','O','#','X',' ','#'],
    ['#',' ','#',' ','O','#','#'],
    ['#','Y','X',' ',' ',' ','#'],
    ['#','#','#','#','#','#','#'],
]

puzzle_expedition = [
    ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
    ['#','#',' ','#','#',' ','#','#','#','#','#',' ',' ',' ','#','#'],
    ['#',' ',' ',' ',' ',' ','#','#','#','#','#',' ','*',' ','#','#'],
    ['#','#',' ','#','#',' ',' ',' ',' ','#','#',' ',' ',' ','X','#'],
    ['#',' ',' ','#','#','#','#','#',' ','#','#','#','#',' ',' ','#'],
    ['#','#',' ','#','#','#',' ',' ',' ','#','#',' ','X','X',' ','#'],
    ['#','#',' ','#','#',' ',' ','#','#','#','#',' ','#','#','#','#'],
    ['#','O',' ','#','#','#',' ',' ',' ',' ',' ',' ','#','#','#','#'],
    ['#','O',' ','B','#','#','#','v','#','#','#','#','#','#','#','#'],
    ['#','X','Y','#','#','#',' ','X',' ','#','#','#','#','#','#','#'],
    ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
]

puzzle_dead_ends = [
    ['#','#','#','#','#','#','#','#','#','#','#'],
    ['#','#','#','#',' ','^',' ','#','#','#','#'],
    ['#','#','#','#',' ',' ',' ','#','#','#','#'],
    ['#','#','#','#',' ',' ',' ','#','#','#','#'],
    ['#',' ',' ',' ','F','#','W',' ',' ',' ','#'],
    ['#','<',' ',' ','#','*','#',' ',' ',' ','#'],
    ['#',' ',' ',' ','W',' ','F',' ',' ',' ','#'],
    ['#','#','#','#',' ',' ',' ','#','#','#','#'],
    ['#','#','#','#',' ',' ',' ','#','#','#','#'],
    ['#','#','#','#',' ',' ',' ','#','#','#','#'],
    ['#','#','#','#','#','#','#','#','#','#','#'],
]

puzzle_butterfly_effect = [
    ['#','#','#','#','#','#','#','#','#','#','#'],
    ['#','*',' ',' ','#','#','#',' ',' ','*','#'],
    ['#',' ',' ','#',' ','#',' ','#',' ',' ','#'],
    ['#',' ','#','S',' ','#',' ','S','#',' ','#'],
    ['#','#',' ',' ','W','#','F',' ',' ','#','#'],
    ['#','#','#','#','#','#','#','#','#','#','#'],
    ['#','*','#',' ',' ','#',' ',' ','#','*','#'],
    ['#',' ','#',' ',' ','#',' ',' ','#',' ','#'],
    ['#',' ',' ',' ',' ','#',' ',' ',' ',' ','#'],
    ['#',' ','#','U','W','#','F','U','#',' ','#'],
    ['#','#','#','#','#','#','#','#','#','#','#'],
]

puzzle_invasion = [ #Failed
    ['#','#','#','#','#','#','#','#','#'],
    ['#',' ',' ',' ','*',' ',' ',' ','#'],
    ['#','X','X','#','#','X','#','X','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ','F','W',' ','F','W',' ','#'],
    ['#',' ','S','U',' ','S','U',' ','#'],
    ['#','#','#','#','#','#','#','#','#'],
]

puzzle_control_panel = [ #Failed
    ['#','#','#','#','#','#','#','#','#','#','#','#'],
    ['#',' ',' ',' ','#',' ',' ',' ','#','#','#','#'],
    ['#',' ','#',' ',' ',' ','#',' ','#','#','#','#'],
    ['#',' ',' ','#','#','#',' ',' ','#','#','#','#'],
    ['#','#',' ','#','#','#',' ','#',' ',' ',' ','#'],
    ['#','#',' ','#','#','#',' ',' ',' ','#',' ','#'],
    ['#','#',' ','#','#','#','#','#','#','#',' ','#'],
    ['#',' ',' ',' ',' ','#',' ','v',' ','#',' ','#'],
    ['#',' ',' ',' ',' ','>',' ',' ','<','X','X','#'],
    ['#',' ',' ',' ',' ','#','^','W','W','#','*','#'],
    ['#','#','#','#','#','#','#','#','#','#','#','#'],
]

puzzle_a_little_extra = [ #Testing
    ['#','#','#','#','#','#','#','#','#'],
    ['#','#',' ','#','#',' ',' ','*','#'],
    ['#',' ','*',' ','#',' ',' ','#','#'],
    ['#','U','S',' ','#','X','S','U','#'],
    ['#',' ','#',' ','#',' ','#',' ','#'],
    ['#',' ','F',' ','#',' ','F',' ','#'],
    ['#','#','#','#','#','#','#','#','#'],
]

puzzle_misdirection = [ #Testing
    ['#','#','#','#','#','#','#','#','#'],
    ['#',' ',' ','#',' ',' ','#',' ','#'],
    ['#','>','#',' ','#',' ',' ',' ','#'],
    ['#',' ',' ','#',' ',' ','#',' ','#'],
    ['#',' ','#',' ','*',' ',' ',' ','#'],
    ['#',' ',' ','#',' ',' ','#',' ','#'],
    ['#',' ','#','X','#',' ',' ','<','#'],
    ['#',' ',' ','#','Y','b','#',' ','#'],
    ['#','#','#','#','#','#','#','#','#'],
]


puzzle_jumble = [ #Testing
    ['#','#','#','#','#','#','#'],
    ['#','#','*','>',' ','#','#'],
    ['#','X','O','>','#','#','#'],
    ['#','X',' ',' ','B','Y','#'],
    ['#','#','#','#','#','#','#'],
]

puzzle_test = [ #Testing
    ['#','#','#','#','#','#','#','#','#'],
    ['#','*','#','*','^',' ','#','*','#'],
    ['#',' ','#',' ','#',' ','#',' ','#'],
    ['#',' ','#','D',' ',' ','#',' ','#'],
    ['#','W','#','W','#','#','#','U','#'],
    ['#','#','#','#','#','#','#','#','#'],
]

AbridgeSolver().solve(puzzle_misdirection)

puzzle_blank = [
    ['#','#','#','#','#','#','#'],
    ['#',' ',' ',' ',' ',' ','#'],
]