import pickle
from solver import Solver, Catalog

CHARS = ' #*X^v<>BYOUDLRWSF+-{}byoudlrwsf'
SPACE, WALL, EXIT, BLOCK, UP, DOWN, LEFT, RIGHT, SQUARE, DIAMOND, CIRCLE,  \
SYMUP, SYMDOWN, SYMLEFT, SYMRIGHT, SYMSQUARE, SYMDIAMOND, SYMCIRCLE, \
CORRUP, CORRDOWN, CORRLEFT, CORRRIGHT, CORRSQUARE, CORRDIAMOND, CORRCIRCLE, \
CSYMUP, CSYMDOWN, CSYMLEFT, CSYMRIGHT, CSYMSQUARE, CSYMDIAMOND, CSYMCIRCLE \
    = range(len(CHARS))

trapsL = trapsR = trapsU = trapsD = []

class AbridgeState:
    def __hash__(self):
        #return hash(pickle.dumps(self.board)) 
        return hash(self.board) 
    def __eq__(self, state):
        return self.board == state.board
    def hash_score(self):
        return hash(pickle.dumps(self.board)) ^ hash(self.controlled_tile)
    def eq_score(self, state):
        return self.controlled_tile == state.controlled_tile and self.board == state.board 
    def __repr__(self) -> str:
        #if use_catalog: return '\n'.join([''.join([CHARS[n] for n in Catalog.get(row)]) for row in self.board])
        return '\n'.join([''.join([CHARS[n] for n in row]) for row in self.board])
        #return '\n'.join([''.join([CHARS[n] for n in row]) for row in self.board]) + str(self.controlled_tile) + str(self.state_score)
    def set(self, x, y, val):
        self.board[y] = self.board[y][:]
        self.board[y][x] = val
    def copy(self):
        state = AbridgeState()
        state.board = self.board[:]
        state.tiles_left = self.tiles_left
        state.circles_left = self.circles_left
        #state.symhints = self.symhints
        #state.controlled_tile = self.controlled_tile
        #state.state_score = self.state_score
        return state
    def push(self, x, y, dx, dy):
        nextx, nexty = x+dx, y+dy
        if self.board[nexty][nextx] == WALL:
            return False
        if self.board[y][x] == WALL or self.board[y][x] == EXIT:
            return self.push(nextx, nexty, dx, dy)
        elif self.board[nexty][nextx] == SPACE:
            if self.circles_left == 0:
                if self.is_trapped(nextx, nexty, self.board[y][x]):
                    return False
            self.set(nextx, nexty, self.board[y][x])
            self.set(x, y, SPACE)
            return True
        elif self.board[nexty][nextx] == EXIT:
            if self.board[y][x] == CIRCLE or self.board[y][x] == SYMCIRCLE:
                if self.circles_left == 1:
                    for y2 in range(len(self.board)):
                        for x2 in range(len(self.board[0])):
                            if x2 == x-dx and y2 == y-dy: continue
                            if self.is_trapped(x2, y2, self.board[y2][x2]):
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
    def copy_and_push(self, x, y, dx, dy, corrupt=False, mirror=False, pull=False):
        new_state = self.copy()
        if mirror and not pull:
            pair = self.find_mirror_symbol(x, y)
            if pair is not None and self.board[y][x] == self.board[pair[1]][pair[0]]:
                if dy > 0 and y < pair[1] or dy < 0 and y > pair[1]:
                    return None
                if dy == 0 and (dx > 0 and x < pair[0] or dx < 0 and x > pair[0]):
                    return None
        if mirror and pull:
            pair = self.find_mirror_symbol(x+dx, y+dy)
            if pair == (x, y):
                pull = False
            elif pair is not None:
                if dy > 0 and y+dy < pair[1] or dy < 0 and y+dy > pair[1]:
                    return None
                if dy == 0 and (dx > 0 and x+dx < pair[0] or dx < 0 and x+dx > pair[0]):
                    return None
        cx, cy = (x + dx, y + dy) if pull else (x, y)
        if mirror and pair is not None:
            if pair[1] > cy or pair[1] == cy and pair[0] > cx:
                cx, cy = pair
        #if new_state.controlled_tile != (cx, cy):
        #    new_state.state_score += 1
        #new_state.controlled_tile = (cx + dx, cy + dy)
        result = new_state.push(x, y, dx, dy)
        if not result: return None
        if mirror and not pull:
            if pair is None:
                new_state.set(x+dx, y+dy, self.unsym(new_state.board[y+dy][x+dx]))
                if corrupt: new_state.set(x, y, WALL)
                #if use_catalog: new_state.board = [Catalog.tadd(r) for r in new_state.board]
                return new_state
            x2, y2 = pair
            dx2, dy2 = dx, dy
            if self.uncorrupt(self.board[y2][x2]) == SYMUP: dx2, dy2 = (0, -1)
            elif self.uncorrupt(self.board[y2][x2]) == SYMDOWN: dx2, dy2 = (0, 1)
            elif self.uncorrupt(self.board[y2][x2]) == SYMLEFT: dx2, dy2 = (-1, 0)
            elif self.uncorrupt(self.board[y2][x2]) == SYMRIGHT: dx2, dy2 = (1, 0)
            result = new_state.push(x2, y2, dx2, dy2)
            if not result: return None
            if self.uncorrupt(new_state.board[y2+dy2][x2+dx2]) != new_state.board[y2+dy2][x2+dx2]: new_state.set(x2,y2, WALL)
            new_state.symhints = {k:v for k,v in new_state.symhints.items()}
            new_state.symhints.pop((x, y), None)
            new_state.symhints.pop((x2, y2), None)
            new_state.symhints[(x+dx, y+dy)] = (x2+dx2, y2+dy2)
            new_state.symhints[(x2+dx2, y2+dy2)] = (x+dx, y+dy)
        if mirror and pull:
            if pair is None:
                if new_state.board[y+dy+dy][x+dx+dx] == SYMCIRCLE:
                    new_state.set(x+dx+dx, y+dy+dy, CIRCLE)
                #if use_catalog: new_state.board = [Catalog.tadd(r) for r in new_state.board]
                return new_state
            x2, y2 = pair
            result = new_state.push(x2-dx, y2-dy, dx, dy)
            if not result: return None
            new_state.symhints = {k:v for k,v in new_state.symhints.items()}
            new_state.symhints.pop((x, y), None)
            new_state.symhints.pop((x2, y2), None)
            new_state.symhints[(x+dx, y+dy)] = (x2+dx, y2+dy)
            new_state.symhints[(x2+dx, y2+dy)] = (x+dx, y+dy)
        #if new_state.board[5][3] == UP or new_state.board[5][3] == LEFT:
        #    if new_state.board[5][2] == SPACE and new_state.board[5][1] == SPACE: return None
        #if new_state.board[5][2] == DOWN:
        #    if new_state.board[5][1] == SPACE: return None
        #if new_state.board[2][10] == UP or new_state.board[2][10] == RIGHT:
        #    if new_state.board[2][11] == SPACE and new_state.board[2][12] == SPACE and new_state.board[2][13] == SPACE:
        #        if new_state.board[3][10] == DOWN and new_state.board[3][11] == DOWN: return None
        #if new_state.board[2][11] == UP or new_state.board[2][11] == RIGHT:
        #    if new_state.board[2][12] == SPACE and new_state.board[2][13] == SPACE: return None
        #if new_state.board[2][12] == DOWN:
        #    if new_state.board[2][13] == SPACE: return None
        #if (new_state.board[4][10] == DOWN or new_state.board[4][10] == RIGHT) and new_state.board[3][11] == DOWN:
        #    if new_state.board[4][11] == SPACE: return None
        #if (new_state.board[4][9] == DOWN or new_state.board[4][9] == RIGHT) and new_state.board[3][10] == DOWN and new_state.board[3][11] == DOWN:
        #    if new_state.board[4][10] == SPACE and new_state.board[4][11] == SPACE: return None
        #if new_state.board[3][3] == DOWN or new_state.board[3][3] == LEFT:
        #    if new_state.board[3][2] == SPACE and new_state.board[3][1] == SPACE: return None
        if corrupt: new_state.set(x, y, WALL)
        #if use_catalog: new_state.board = [Catalog.tadd(r) for r in new_state.board]
        return new_state
    def is_trapped(self, x, y, tile):
        if tile == UP and trapsU[y][x] or \
            tile == DOWN and trapsD[y][x] or \
            tile == LEFT and trapsL[y][x] or \
            tile == RIGHT and trapsR[y][x]:
            return True
        if tile == BLOCK:
            if trapsU[y][x] or trapsD[y][x] or \
                trapsL[y][x] or trapsR[y][x]:
                return True
        return False
    def can_escape(self, x, y, dx, dy, diagonal=False):
        if self.board[y][x] == WALL or self.board[y][x] == EXIT: return True
        if self.board[y-dy][x-dx] == WALL and (self.board[y+dx][x+dy] == WALL or self.board[y-dx][x-dy] == WALL):
            if not diagonal: return False
            if (self.board[y+dy+dx][x+dx+dy] == WALL or self.board[y-dy-dx][x-dx-dy] == WALL) and \
                (self.board[y+dy-dx][x+dx-dy] == WALL or self.board[y-dy+dx][x-dx+dy] == WALL):
                return False
        for dx2, dy2 in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (dx, dy) == (dx2, dy2): continue
            if self.trapped_in_direction(x, y, dx2, dy2, diagonal):
                return False
        return True
    def trapped_in_direction(self, x, y, dx, dy, diagonal=False):
        if self.board[y+dy][x+dx] != WALL: return False
        for dx2, dy2 in [(dy, dx), (-dy, -dx)]:
            x2 = x; y2 = y
            while self.board[y2][x2] != WALL:
                if self.board[y2+dy][x2+dx] != WALL:
                    return False
                if self.board[y2][x2] == EXIT:
                    return False
                x2 += dx2; y2 += dy2
            if diagonal and self.board[y2+dy][x2+dx] != WALL:
                return False
        return True
    def uncorrupt(self, symbol):
        if symbol >= CORRUP: return symbol - 14
        return symbol
    def unsym(self, symbol):
        if symbol >= SYMUP: return symbol - 7
        return symbol
    def find_mirror_symbol(self, x, y):
        symbol = self.uncorrupt(self.board[y][x])
        for h in [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            hint = self.symhints.get(h, None)
            if hint:
                symbol2 = self.uncorrupt(self.board[hint[1]][hint[0]])
                if symbol == symbol2 or symbol in [SYMUP, SYMDOWN, SYMLEFT, SYMRIGHT] and symbol2 in [SYMUP, SYMDOWN, SYMLEFT, SYMRIGHT]:
                    if (x, y) != hint: return hint
        for y2 in range(1, len(self.board)-1):
            for x2 in range(1, len(self.board[0])-1):
                if x == x2 and y == y2: continue
                symbol2 = self.uncorrupt(self.board[y2][x2])
                if symbol == symbol2 or symbol in [SYMUP, SYMDOWN, SYMLEFT, SYMRIGHT] and symbol2 in [SYMUP, SYMDOWN, SYMLEFT, SYMRIGHT]:
                    if (x2, y2) != hint: return x2, y2
        return None

class AbridgeSolver(Solver):
    def setup(self, board):
        #if use_catalog: Catalog.init()
        starting_state = AbridgeState()
        board = [[CHARS.index(c) for c in row] for row in board]
        starting_state.board = board
        self.open_tiles = [(x, y) for y, row in enumerate(board) for x, val in enumerate(row) if val != WALL and val != EXIT]
        starting_state.tiles_left = sum([sum([val not in [SPACE, WALL, EXIT] for val in row]) for row in board])
        self.tiles_max = starting_state.tiles_left
        starting_state.circles_left = sum([sum([val == CIRCLE or val == SYMCIRCLE for val in row]) for row in board])
        starting_state.symhints = {}
        starting_state.controlled_tile = None
        starting_state.state_score = 0
        for y, row in enumerate(starting_state.board):
            for x, val in enumerate(row):
                if starting_state.unsym(val) != val:
                    hint = starting_state.find_mirror_symbol(x, y)
                    starting_state.symhints[(x, y)] = hint
                    starting_state.symhints[hint] = (x, y)
        self.detect_traps(starting_state)
        for l in [trapsU, trapsD, trapsL, trapsR]: print('\n'.join([''.join([str(int(n)) for n in row]) for row in l])+'\n')
        #if use_catalog: starting_state.board = [Catalog.tadd(r) for r in starting_state.board]
        return starting_state
    def get_next_states(self, state):
        states = []
        state = state.copy()
        #if use_catalog: state.board = [Catalog.get(r) for r in state.board]
        for x, y in self.open_tiles:
            val = state.board[y][x]
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
                states.append(state.copy_and_push(x, y+1, 0, -1, pull=True))
                states.append(state.copy_and_push(x+1, y, -1, 0, pull=True))
                states.append(state.copy_and_push(x-1, y, 1, 0, pull=True))
                states.append(state.copy_and_push(x, y-1, 0, 1, pull=True))
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
                if states[-1] is None and states[-2] is None and states[-3] is None and states[-4] is None:
                    if (state.board[y-1][x] == WALL or state.board[y+1][x] == WALL) and \
                        (state.board[y][x-1] == WALL or state.board[y][x+1] == WALL):
                        return []
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
                states.append(state.copy_and_push(x, y+1, 0, -1, mirror=True, pull=True))
                states.append(state.copy_and_push(x+1, y, -1, 0, mirror=True, pull=True))
                states.append(state.copy_and_push(x-1, y, 1, 0, mirror=True, pull=True))
                states.append(state.copy_and_push(x, y-1, 0, 1, mirror=True, pull=True))
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
        return [s for s in states if s is not None]
    
    def detect_traps(self, state):
        global trapsL; trapsL = [[True for _ in row] for row in state.board]
        global trapsR; trapsR = [[True for _ in row] for row in state.board]
        global trapsU; trapsU = [[True for _ in row] for row in state.board]
        global trapsD; trapsD = [[True for _ in row] for row in state.board]
        diagonal = any([DIAMOND in row or SYMDIAMOND in row or CORRDIAMOND in row for row in state.board])
        for y, row in enumerate(state.board):
            for x, _ in enumerate(row):
                trapsL[y][x] = not state.can_escape(x, y, 1, 0, diagonal)
                trapsR[y][x] = not state.can_escape(x, y, -1, 0, diagonal)
                trapsU[y][x] = not state.can_escape(x, y, 0, 1, diagonal)
                trapsD[y][x] = not state.can_escape(x, y, 0, -1, diagonal)
    def check_finish(self, state):
        return state.tiles_left <= 0
    #def score_state(self, state):
    #    return state.state_score
    def purge_state_check(self, state, purge_num):
        #if purge_num <= 1:
        #    return state.board[4][9] == UP or state.board[4][10] == UP or state.board[4][11] == UP
        return state.tiles_left <= self.tiles_max - purge_num

def from_strs(strs):
    return [[c for c in s] for s in strs]

puzzle_doubles = [ #Failed even after 45000K+ iterations, this will need a LOT of state pruning
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

puzzle_follow_the_leader = [ #Approximated
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

puzzle_scattered = [ #Approximated
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

puzzle_knockback = [ #Approximated
    ['#','#','#','#','#','#','#'],
    ['#','>','>','X',' ','#','#'],
    ['#',' ','#','^',' ',' ','#'],
    ['#',' ','O','#','X',' ','#'],
    ['#',' ','#',' ','*','#','#'],
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
    ['#',' ',' ','v',' ',' ','#'],
    ['#','>',' ',' ',' ',' ','#'],
    ['#','>',' ',' ',' ','<','#'],
    ['#',' ','^','*','^',' ','#'],
    ['#','#','#','#','#','#','#'],
]

puzzle_x = from_strs([
'############',
'#   #   ####',
'# #   # ####',
'#  ###  ####',
'## ### #   #',
'## ###   # #',
'## ####### #',
'#    # v # #',
'#    >  <XX#',
'#    #^WW#*#',
'############',
])

USE_SCORE = 0
if USE_SCORE:
    AbridgeState.__eq__ = AbridgeState.eq_score
    AbridgeState.__hash__ = AbridgeState.hash_score
USE_CACHE = 0

import cProfile
import pstats
#profiler = cProfile.Profile()
#profiler.enable()
AbridgeSolver().solve_optimal(puzzle_expedition, debug=0, showprogress=1, use_score=USE_SCORE, catalog_variable="board")
#profiler.disable()
#stats = pstats.Stats(profiler)
#stats.sort_stats('cumulative').print_stats(10)  # Print top 10 stats

puzzle_blank = [
    ['#','#','#','#','#','#','#'],
    ['#',' ',' ',' ',' ',' ','#'],
]