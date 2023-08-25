import pickle
from solver import Solver

CHARS = ' #*X^v<>BYOUDLRWSF+-{}byoudlrwsf'
SPACE, WALL, EXIT, BLOCK, UP, DOWN, LEFT, RIGHT, SQUARE, DIAMOND, CIRCLE,  \
SYMUP, SYMDOWN, SYMLEFT, SYMRIGHT, SYMSQUARE, SYMDIAMOND, SYMCIRCLE, \
CORRUP, CORRDOWN, CORRLEFT, CORRRIGHT, CORRSQUARE, CORRDIAMOND, CORRCIRCLE, \
CSYMUP, CSYMDOWN, CSYMLEFT, CSYMRIGHT, CSYMSQUARE, CSYMDIAMOND, CSYMCIRCLE \
    = range(len(CHARS))

trapsL = trapsR = trapsU = trapsD = []

class AbridgeState:
    def __hash__(self):
        return hash(pickle.dumps(self.board))
    def __eq__(self, state):
        return self.board == state.board
    def __repr__(self) -> str:
        return '\n'.join([''.join([CHARS[n] for n in row]) for row in self.board])
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
        if self.board[nexty][nextx] == WALL:
            return False
        if self.board[y][x] == WALL or self.board[y][x] == EXIT:
            return self.push(nextx, nexty, dx, dy)
        elif self.board[nexty][nextx] == SPACE:
            if self.circles_left == 0:
                if self.board[y][x] == UP and trapsU[nexty][nextx] or \
                    self.board[y][x] == DOWN and trapsD[nexty][nextx] or \
                    self.board[y][x] == LEFT and trapsL[nexty][nextx] or \
                    self.board[y][x] == RIGHT and trapsR[nexty][nextx]:
                    return False
                if self.board[y][x] == BLOCK:
                    if trapsU[nexty][nextx] or trapsD[nexty][nextx] or \
                        trapsL[nexty][nextx] or trapsR[nexty][nextx]:
                        return False
            self.set(nextx, nexty, self.board[y][x])
            self.set(x, y, SPACE)
            return True
        elif self.board[nexty][nextx] == EXIT:
            if self.board[y][x] == CIRCLE or self.board[y][x] == SYMCIRCLE:
                #Trap check
                if self.circles_left == 1:
                    for y2 in range(len(self.board)):
                        for x2 in range(len(self.board[0])):
                            if x2 == x-dx and y2 == y-dy: continue
                            if self.board[y2][x2] == UP and trapsU[y2][x2] or \
                            self.board[y2][x2] == DOWN and trapsD[y2][x2] or \
                            self.board[y2][x2] == LEFT and trapsL[y2][x2] or \
                            self.board[y2][x2] == RIGHT and trapsR[y2][x2]:
                                return False
                            if self.board[y2][x2] == BLOCK:
                                if trapsU[y2][x2] or trapsD[y2][x2] or \
                                    trapsL[y2][x2] or trapsR[y2][x2]:
                                    return False
                self.circles_left -= 1
            self.set(x, y, SPACE)
            self.tiles_left -= 1
            return True
        else:
            if not self.push(nextx, nexty, dx, dy):
                return False
            self.set(nextx, nexty, self.board[y][x])
            self.set(x, y, SPACE)
            return True
    def copy_and_push(self, x, y, dx, dy, corrupt=False, mirror=False, mirror_pull=False):
        new_state = self.copy()
        result = new_state.push(x, y, dx, dy)
        if not result: return None
        if mirror:
            pair = self.find_mirror_symbol(x, y)
            if pair is None:
                new_state.set(x+dx, y+dy, self.unsym(new_state.board[y+dy][x+dx]))
                if corrupt: new_state.set(x, y, WALL)
                return new_state
            x2, y2 = pair
            dx2, dy2 = dx, dy
            if self.uncorrupt(self.board[y2][x2]) == SYMUP: dx2, dy2 = (0, -1)
            elif self.uncorrupt(self.board[y2][x2]) == SYMDOWN: dx2, dy2 = (0, 1)
            elif self.uncorrupt(self.board[y2][x2]) == SYMLEFT: dx2, dy2 = (-1, 0)
            elif self.uncorrupt(self.board[y2][x2]) == SYMRIGHT: dx2, dy2 = (1, 0)
            result = new_state.push(x2, y2, dx2, dy2)
            if not result: return None
            if new_state.board[y2+dy2][x2+dx2] in [CORRUP, CORRDOWN, CORRLEFT, CORRRIGHT, CORRSQUARE, CORRDIAMOND, CORRCIRCLE]: new_state.set(x2,y2, WALL)
        if mirror_pull:
            pair = self.find_mirror_symbol(x+dx, y+dy)
            if pair is None:
                if new_state.board[y+dy+dy][x+dx+dx] == SYMCIRCLE:
                    new_state.set(x+dx+dx, y+dy+dy, CIRCLE)
                return new_state
            x2, y2 = pair
            result = new_state.push(x2-dx, y2-dy, dx, dy)
            if not result: return None
        if corrupt: new_state.set(x, y, WALL)
        return new_state
    def can_escape(self, x, y, dx, dy):
        if self.board[y][x] == EXIT or self.board[y][x] == WALL \
            or self.board[y-dy][x-dx] != WALL:
            return True
        for dx2, dy2 in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if dx2 == dx or dy2 == dy: continue
            if self.board[y-dy2][x-dx2] == WALL and self.board[y-dy-dy2][x-dx-dx2] == WALL: continue
            x2 = x; y2 = y
            while self.board[y2][x2] != WALL:
                if self.board[y2-dy][x2-dx] != WALL:
                    return True
                if self.board[y2-dy-dy2][x2-dx-dx2] != WALL and self.board[y2+dy+dy2][x2+dx+dx2] != WALL:
                    return True
                if self.board[y2][x2] == EXIT:
                    return True
                x2 += dx2; y2 += dy2
        return False
    def uncorrupt(self, symbol):
        if symbol >= CORRUP: return symbol - 14
        return symbol
    def unsym(self, symbol):
        if symbol >= SYMUP: return symbol - 7
        return symbol
    def find_mirror_symbol(self, x, y):
        symbol = self.uncorrupt(self.board[y][x])
        for y2 in range(len(self.board)):
            for x2 in range(len(self.board[0])):
                if x == x2 and y == y2: continue
                symbol2 = self.uncorrupt(self.board[y2][x2])
                if symbol == symbol2 or symbol in [SYMUP, SYMDOWN, SYMLEFT, SYMRIGHT] and symbol2 in [SYMUP, SYMDOWN, SYMLEFT, SYMRIGHT]:
                    return x2, y2
        return None

class AbridgeSolver(Solver):
    def solve(self, board, debug=0):
        starting_state = AbridgeState()
        board = [[CHARS.index(c) for c in row] for row in board]
        starting_state.board = board
        starting_state.tiles_left = sum([sum([val not in [SPACE, WALL, EXIT] for val in row]) for row in board])
        starting_state.circles_left = sum([sum([val == CIRCLE or val == SYMCIRCLE for val in row]) for row in board])
        self.detect_traps(starting_state)
        self.corrupt_states = {}
        #print(trapsD); print(trapsL); print(trapsR); print(trapsU)
        self.solve_optimal(starting_state, debug=debug)
        #self.solve_optimal_debug(starting_state)
    def get_next_states(self, state):
        states = []
        for y, row in enumerate(state.board):
            for x, val in enumerate(row):
                if val == SPACE or val == WALL or val == EXIT or val == BLOCK:
                    continue
                if val == UP:
                    states.append(state.copy_and_push(x, y, 0, -1))
                elif val == LEFT:
                    states.append(state.copy_and_push(x, y, -1, 0))
                elif val == RIGHT:
                    states.append(state.copy_and_push(x, y, 1, 0))
                elif val == DOWN:
                    states.append(state.copy_and_push(x, y, 0, 1))
                elif val == SQUARE:
                    states.append(state.copy_and_push(x, y, 0, -1))
                    states.append(state.copy_and_push(x, y, -1, 0))
                    states.append(state.copy_and_push(x, y, 1, 0))
                    states.append(state.copy_and_push(x, y, 0, 1))
                elif val == DIAMOND:
                    states.append(state.copy_and_push(x, y, -1, -1))
                    states.append(state.copy_and_push(x, y, -1, 1))
                    states.append(state.copy_and_push(x, y, 1, -1))
                    states.append(state.copy_and_push(x, y, 1, 1))
                elif val == CIRCLE:
                    states.append(state.copy_and_push(x, y+1, 0, -1))
                    states.append(state.copy_and_push(x+1, y, -1, 0))
                    states.append(state.copy_and_push(x-1, y, 1, 0))
                    states.append(state.copy_and_push(x, y-1, 0, 1))
                #Corrupted
                elif val == CORRUP:
                    states.append(state.copy_and_push(x, y, 0, -1, corrupt=True))
                elif val == CORRLEFT:
                    states.append(state.copy_and_push(x, y, -1, 0, corrupt=True))
                elif val == CORRRIGHT:
                    states.append(state.copy_and_push(x, y, 1, 0, corrupt=True))
                elif val == CORRDOWN:
                    states.append(state.copy_and_push(x, y, 0, 1, corrupt=True))
                elif val == CORRSQUARE:
                    states.append(state.copy_and_push(x, y, 0, -1, corrupt=True))
                    states.append(state.copy_and_push(x, y, -1, 0, corrupt=True))
                    states.append(state.copy_and_push(x, y, 1, 0, corrupt=True))
                    states.append(state.copy_and_push(x, y, 0, 1, corrupt=True))
                    if states[-1] is None and states[-2] is None and states[-3] is None and states[-4] is None:
                        if (state.board[y-1][x-1] == WALL or state.board[y+1][x+1] == WALL) and \
                            (state.board[y+1][x-1] == WALL or state.board[y-1][x+1] == WALL):
                            return []
                elif val == CORRDIAMOND:
                    states.append(state.copy_and_push(x, y, -1, -1, corrupt=True))
                    states.append(state.copy_and_push(x, y, -1, 1, corrupt=True))
                    states.append(state.copy_and_push(x, y, 1, -1, corrupt=True))
                    states.append(state.copy_and_push(x, y, 1, 1, corrupt=True))
                    if states[-1] == None and states[-2] == None and states[-3] == None and states[-4] == None:
                        if (state.board[y-1][x] == WALL or state.board[y+1][x] == WALL) and \
                            (state.board[y][x-1] == WALL or state.board[y][x+1] == WALL):
                            return []
                #elif val == CORRCIRCLE:
                #    pass
                #Mirror
                elif val == SYMUP:
                    states.append(state.copy_and_push(x, y, 0, -1, mirror=True))
                elif val == SYMLEFT:
                    states.append(state.copy_and_push(x, y, -1, 0, mirror=True))
                elif val == SYMRIGHT:
                    states.append(state.copy_and_push(x, y, 1, 0, mirror=True))
                elif val == SYMDOWN:
                    states.append(state.copy_and_push(x, y, 0, 1, mirror=True))
                elif val == SYMSQUARE:
                    states.append(state.copy_and_push(x, y, 0, -1, mirror=True))
                    states.append(state.copy_and_push(x, y, -1, 0, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, 0, mirror=True))
                    states.append(state.copy_and_push(x, y, 0, 1, mirror=True))
                elif val == SYMDIAMOND:
                    states.append(state.copy_and_push(x, y, -1, -1, mirror=True))
                    states.append(state.copy_and_push(x, y, -1, 1, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, -1, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, 1, mirror=True))
                elif val == SYMCIRCLE:
                    states.append(state.copy_and_push(x, y+1, 0, -1, mirror_pull=True))
                    states.append(state.copy_and_push(x+1, y, -1, 0, mirror_pull=True))
                    states.append(state.copy_and_push(x-1, y, 1, 0, mirror_pull=True))
                    states.append(state.copy_and_push(x, y-1, 0, 1, mirror_pull=True))
                #Corrupted mirror
                elif val == CSYMUP:
                    states.append(state.copy_and_push(x, y, 0, -1, corrupt=True, mirror=True))
                elif val == CSYMLEFT:
                    states.append(state.copy_and_push(x, y, -1, 0, corrupt=True, mirror=True))
                elif val == CSYMRIGHT:
                    states.append(state.copy_and_push(x, y, 1, 0, corrupt=True, mirror=True))
                elif val == CSYMDOWN:
                    states.append(state.copy_and_push(x, y, 0, 1, corrupt=True, mirror=True))
                elif val == CSYMSQUARE:
                    states.append(state.copy_and_push(x, y, 0, -1, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, -1, 0, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, 0, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, 0, 1, corrupt=True, mirror=True))
                elif val == CSYMDIAMOND:
                    states.append(state.copy_and_push(x, y, -1, -1, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, -1, 1, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, -1, corrupt=True, mirror=True))
                    states.append(state.copy_and_push(x, y, 1, 1, corrupt=True, mirror=True))
                #elif val == CSYMCIRCLE:
                #    pass
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
        state2.board = [[SPACE if t == WALL else t for t in row] for row in state.board]
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
                if t1 == WALL and t2 != WALL:
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

#############################################################################

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

puzzle_testsym = [ #Testing
    ['#','#','#','#','#','#','#','#','#'],
    ['#','*','#','*','^',' ','#','*','#'],
    ['#',' ','#',' ','#',' ','#',' ','#'],
    ['#',' ','#','D',' ',' ','#',' ','#'],
    ['#','W','#','W','#','#','#','U','#'],
    ['#','#','#','#','#','#','#','#','#'],
]

puzzle_test = [
    ['#','#','#','#','#','#','#'],
    ['#',' ',' ',' ',' ',' ','#'],
    ['#',' ','R','*','L',' ','#'],
    ['#',' ',' ',' ',' ',' ','#'],
    ['#','#','#','#','#','#','#'],
]

AbridgeSolver().solve(puzzle_butterfly_effect, debug=0)

puzzle_blank = [
    ['#','#','#','#','#','#','#'],
    ['#',' ',' ',' ',' ',' ','#'],
]