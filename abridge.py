import pickle
from solvernew import Solver, GridState

class AbridgeSolver(Solver):
    def setup(self, puzzle):
        state = GridState(puzzle)
        self.open_tiles = []
        state.set_temp('tiles', 0)
        state.set_temp('circles', 0)
        for x, y in state.all_points():
            val = state.get(x, y)
            if val in '#*':
                continue
            self.open_tiles.append((x, y))
            if val != ' ':
                state.inc_temp('tiles')
            if val == 'O':
                state.inc_temp('circles')
        self.detect_traps(state)
        #for l in [self.trapsU, self.trapsD, self.trapsL, self.trapsR]: print('\n'.join([''.join([str(int(n)) for n in row]) for row in l])+'\n')
        return state
    def get_next_states(self, state):
        states = {}
        move = state.get_var('move')
        for p in self.open_tiles:
            val = state.get(p[0], p[1])[0]
            if val in ' #X' or move == p:
                continue
            new_state = state.copy()
            new_state.set_var('move', p)
            states[p] = new_state
        if move is None:
            return states
        x, y = move
        val = state.get(x, y)[0]
        if val == '^':
            states['^'] = self.copy_and_push(state, x, y, 0, -1)
        elif val == '<':
            states['<'] = self.copy_and_push(state, x, y, -1, 0)
        elif val == '>':
            states['>'] = self.copy_and_push(state, x, y, 1, 0)
        elif val == 'v':
            states['v'] = self.copy_and_push(state, x, y, 0, 1)
        elif val == 'B':
            states['^'] = self.copy_and_push(state, x, y, 0, -1)
            states['<'] = self.copy_and_push(state, x, y, -1, 0)
            states['>'] = self.copy_and_push(state, x, y, 1, 0)
            states['v'] = self.copy_and_push(state, x, y, 0, 1)
        elif val == 'Y':
            states['<^'] = self.copy_and_push(state, x, y, -1, -1)
            states['<v'] = self.copy_and_push(state, x, y, -1, 1)
            states['^>'] = self.copy_and_push(state, x, y, 1, -1)
            states['v>'] = self.copy_and_push(state, x, y, 1, 1)
        elif val == 'O':
            states['^'] = self.copy_and_push(state, x, y+1, 0, -1)
            states['<'] = self.copy_and_push(state, x+1, y, -1, 0)
            states['>'] = self.copy_and_push(state, x-1, y, 1, 0)
            states['v'] = self.copy_and_push(state, x, y-1, 0, 1)
        return {k:v for k,v in states.items() if v is not None}
    def check_finish(self, state):
        return state.get_temp('tiles') == 0
    def push(self, state, x, y, dx, dy):
        nextx, nexty = x+dx, y+dy
        val, nextval = state.get(x, y), state.get(nextx, nexty)
        if nextval == '#':
            return False
        if val == '#' or val == '*': #Can't pull wall or exit
            return self.push(state, nextx, nexty, dx, dy)
        elif nextval == ' ':
            if not state.get_temp('circles'):
                if self.is_trapped(nextx, nexty, val[0]):
                    return False
            state.set(nextx, nexty, val)
            state.set(x, y, ' ')
            return True
        elif nextval == '*':
            state.dec_temp('tiles', 1)
            if val[0] == 'O':
                state.dec_temp('circles', 1)
            state.set(x, y, ' ')
            return True
        else:
            if not self.push(state, nextx, nexty, dx, dy):
                return False
            state.set(nextx, nexty, val)
            state.set(x, y, ' ')
            return True
    def copy_and_push(self, state, x, y, dx, dy):
        new_state = state.copy()
        result = self.push(new_state, x, y, dx, dy)
        if not result: return None
        new_state.set_var('move', (x+dx, y+dy))
        if state.get(x, y)[-1] == 'c': new_state.set(x, y, '#')
        return new_state
    def is_trapped(self, x, y, tile):
        if tile == '^' and self.trapsU[y][x] or \
            tile == 'v' and self.trapsD[y][x] or \
            tile == '<' and self.trapsL[y][x] or \
            tile == '>' and self.trapsR[y][x]:
            return True
        if tile == 'X':
            if self.trapsU[y][x] or self.trapsD[y][x] or \
                self.trapsL[y][x] or self.trapsR[y][x]:
                return True
        return False
    def can_escape(self, state, x, y, dx, dy, diagonal=False):
        val = state.get(x, y)
        if val == '#' or val == '*': return True
        if state.get(x-dx, y-dy) == '#' and (state.get(x+dy, y+dx) == '#' or state.get(x-dy, y-dx) == '#'):
            if not diagonal: return False
            if (state.get(x+dx+dy, y+dx+dy) == '#' or state.get(x-dx-dy, y-dx-dy) == '#') and \
                (state.get(x+dx-dy, y-dx+dy) == '#' or state.get(x-dx+dy, y+dx-dy) == '#'):
                return False
        for dx2, dy2 in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (dx, dy) == (dx2, dy2): continue
            if self.trapped_in_direction(state, x, y, dx2, dy2, diagonal):
                return False
        return True
    def trapped_in_direction(self, state, x, y, dx, dy, diagonal=False):
        if state.get(x+dx, y+dy) != '#': return False
        for dx2, dy2 in [(dy, dx), (-dy, -dx)]:
            x2 = x; y2 = y
            while state.get(x2, y2) != '#':
                if state.get(x2+dx, y2+dy) != '#':
                    return False
                if state.get(x2, y2) == '*':
                    return False
                x2 += dx2; y2 += dy2
            if diagonal and state.get(x2+dx, y2+dy) != '#':
                return False
        return True
    def detect_traps(self, state):
        self.trapsL = [[True for _ in range(state.size()[0])] for row in range(state.size()[1])]
        self.trapsR = [[True for _ in range(state.size()[0])] for row in range(state.size()[1])]
        self.trapsU = [[True for _ in range(state.size()[0])] for row in range(state.size()[1])]
        self.trapsD = [[True for _ in range(state.size()[0])] for row in range(state.size()[1])]
        diagonal = state.find('Y', 0)
        for x, y in state.all_points():
            self.trapsL[y][x] = not self.can_escape(state, x, y, 1, 0, diagonal)
            self.trapsR[y][x] = not self.can_escape(state, x, y, -1, 0, diagonal)
            self.trapsU[y][x] = not self.can_escape(state, x, y, 0, 1, diagonal)
            self.trapsD[y][x] = not self.can_escape(state, x, y, 0, -1, diagonal)

def from_strs(strs):
    map = {}
    return [[map.get(c) or c for c in s] for s in strs]

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
'###',
'# #',
'#*#',
'# #',
'#^#',
'###',
])

#import cProfile
#import pstats
#profiler = cProfile.Profile()
#profiler.enable()
AbridgeSolver().solve_optimal(puzzle_x, debug=1)
#profiler.disable()
#stats = pstats.Stats(profiler)
#stats.sort_stats('cumulative').print_stats(10)  # Print top 10 stats

puzzle_blank = from_strs([
'#######',
'#     #',
])