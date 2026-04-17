import pickle
from solvernew import Solver, GridState, DIRECTIONS8, DIRECTIONS, DIRECTIONSDIAG

class AbridgeSolver(Solver):
    def setup(self, puzzle):
        state = GridState(puzzle)
        self.open_tiles = []
        state.set_temp('tiles', 0)
        state.set_temp('circles', 0)
        sym = False
        self.exits = []
        self.corrupt = False
        for x, y in state.all_points():
            val = state.get(x, y)
            if val == '#':
                continue
            if val == '*':
                self.exits.append((x, y))
                continue
            self.open_tiles.append((x, y))
            if val != ' ':
                state.inc_temp('tiles')
            if val[0] == 'O':
                state.inc_temp('circles')
            if 'c' in val:
                self.corrupt = True
            if 's' in val:
                sym = True
        if sym and len(self.exits) > 1:
            self.lower_bound = self.lower_bound_sym
        if state.get_temp('circles') == 0:
            state.del_temp('circles')
        self.detect_traps(state)
        #for l in [self.trapsU, self.trapsD, self.trapsL, self.trapsR]: print('\n'.join([''.join([str(int(n)) for n in row]) for row in l])+'\n')
        return state
    def get_next_states(self, state):
        states = {}
        move = state.get_var('move')
        symmetry = {}
        if not state.get_temp('click'):
            for p in self.open_tiles:
                val = state.get(p[0], p[1])
                if val[0] in ' #' or move == p:#or state.get_temp('sym') == p:
                    continue
                if self.corrupt:
                    for dirx, diry in DIRECTIONS.values():
                        if state.get(p[0]+dirx, p[1]+diry) != '#':
                            break
                    else:
                        for p2 in self.open_tiles:
                            if state.get(p2[0], p2[1])[0] == 'Y':
                                break
                        else: return {}
                        count = 0
                        for dirx, diry in DIRECTIONSDIAG:
                            if state.get(p[0]+dirx, p[1]+diry) != '#':
                                count += 1
                                if count == 2: break
                        else:
                            if count == 0 or count == 1 and val[0] != 'Y': return {}
                if val[0] == 'X': continue
                new_state = state.copy()
                new_state.set_var('move', p)
                new_state.set_score(0)
                new_state.set_temp('click', 1)
                states[p] = new_state
                if val[-1] == 's':
                    val = val[0]
                    if val in 'v<>': val = '^'
                    if val in symmetry:
                        states[symmetry[val]].set_temp('sym', p)
                        new_state.set_temp('sym', symmetry[val])
                    else:
                        symmetry[val] = p
                        new_state.del_temp('sym')
                else:
                    new_state.del_temp('sym')
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
            sym = state.get(x, y)[-1] == 's'
            states['^'] = self.copy_and_push(state, x, y+1, 0, -1, True, sym)
            states['<'] = self.copy_and_push(state, x+1, y, -1, 0, True, sym)
            states['>'] = self.copy_and_push(state, x-1, y, 1, 0, True, sym)
            states['v'] = self.copy_and_push(state, x, y-1, 0, 1, True, sym)
        return {k:v for k,v in states.items() if v is not None}
    def check_finish(self, state):
        return state.get_temp('tiles') == 0
    def lower_bound(self, state):
        return state.get_temp('tiles')
    def lower_bound_sym(self, state):
        return state.get_temp('tiles') // 2
    def approximate(self, state):
        return state.get_temp('tiles')# + 0 if state.get_temp('circles') else 3
    def can_move(self, state, pos, dest, dir, pval, dval):
        if dval == '#' or state.get_temp('circles') is None and self.is_trapped(dest[0], dest[1], pval):
            return False
        if pval[-1] == 's' and state.get_var('move') == pos:
            sym = state.get_temp('sym')
            if sym is not None:
                sym_dir = dir if state.get(sym[0], sym[1])[0] == pval[0] else (-dir[0], -dir[1])
                if pval[0] == 'O' and state.get(sym[0] - sym_dir[0], sym[1] - sym_dir[1]) not in '#* ':
                    if not state.move((sym[0] - sym_dir[0], sym[1] - sym_dir[1]), sym_dir):
                        return False
                if not state.move(sym, sym_dir):
                    return False
                state.set_temp('sym', (sym[0] + sym_dir[0], sym[1] + sym_dir[1]))
        if dval in ' *': return True
        return state.move(dest, dir)
    def do_move(self, state, pos, dest, dir, pval, dval):
        if dval == '*':
            if pos == state.previous.get_var('move'):
                state.del_var('move')
                state.del_temp('sym')
            if pos == state.previous.get_temp('sym'):
                state.del_temp('sym')
            state.dec_temp('tiles', 1)
            if pval[0] == 'O':
                state.dec_temp('circles', 1)
                if state.get_temp('circles') == 0:
                    state.set_temp('circles', -1)
        else:
            state.set(dest[0], dest[1], pval)
        if (pval[-1] == 'c' or len(pval) == 3) and state.get(pos[0], pos[1]) == ' ':
            moving = state.previous.get_var('move')
            if state.previous.get(moving[0], moving[1])[0] != 'O':
                state.set(pos[0], pos[1], '#')
    def copy_and_push(self, state, x, y, dx, dy, circle=False, symcircle=False):
        pos = (x, y)
        dir = (dx, dy)
        new_state = state.copy()
        new_state.del_temp('click')
        if circle and new_state.get(x, y) in '#* ':
            pos = (x + dx, y + dy)
        result = new_state.move(pos, dir)
        if result is False: return None
        if circle:
            new_state.set_var('move', (x + dx + dx, y + dy + dy))
        else:
            new_state.set_var('move', (x + dx, y + dy))
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
    def check_valid(self, state):
        if state.get_temp('circles') == -1:
            for x, y in self.open_tiles:
                if self.is_trapped(x, y, state.get(x, y)):
                    return False
            state.del_temp('circles')
        return True #Below code is for Doubles puzzle only
        if state.get(3, 5) in '^<' and state.get(1, 5) == ' ' and state.get(2, 5) == ' ': return False
        if state.get(2, 5) == 'v' and state.get(1, 5) == ' ': return False
        if state.get(10, 2) in '^>' and state.get(11, 2) == ' ' and state.get(12, 2) == ' ' and state.get(13, 2) == ' ':
            if state.get(10, 3) == 'v' and state.get(11, 3) == 'v': return False
        if state.get(11, 2) in '^>' and state.get(12, 2) == ' ' and state.get(13, 2) == ' ': return False
        if state.get(12, 2) == 'v' and state.get(13, 2) == ' ': return False
        if state.get(10, 4) in 'v>' and state.get(11, 3) == 'v' and state.get(11, 4) == ' ': return False
        if state.get(9, 4) in 'v>' and state.get(10, 3) == 'v' and state.get(11, 3) == 'v':
            if state.get(10, 4) == ' ' and state.get(11, 4) == ' ': return False
        if state.get(3, 3) in 'v<' and state.get(2, 3) == ' ' and state.get(1, 3) == ' ': return False
        return True

def from_strs(strs):
    map = {'+':'^c', '-':'vc', '}':'>c', '{':'<c', 'b':'Bc', 'y':'Yc',
           'U':'^s', 'D':'vs', 'R':'>s', 'L':'<s', 'W':'Bs', 'S':'Ys', 'F':'Os',
           'l':'<cs', 'r':'>cs', 'w':'Bcs', 's':'Ycs'}
    return [[map.get(c) or c for c in s] for s in strs]

#############################################################################

puzzle_misdirection = from_strs([ #Testing
'#########',
'#  #  # #',
'#># #   #',
'#  #  # #',
'# # *   #',
'#  #  # #',
'# #X#  <#',
'#  #Yb# #',
'#########',
])


puzzle_test = [
    ['#','#','#','#','#','#','#'],
    ['#',' ',' ','v',' ',' ','#'],
    ['#','>',' ',' ',' ',' ','#'],
    ['#','>',' ',' ',' ','<','#'],
    ['#',' ','^','*','^',' ','#'],
    ['#','#','#','#','#','#','#'],
]

puzzle = from_strs([
'#####',
'#> Y#',
'## ##',
'#OXv#',
'# XX#',
'#*^X#',
'#####',
])

AbridgeSolver().solve(puzzle_misdirection, debug=0, refine=0, use_score=1, optimize_score=1, write_to_file=0,
                      approximate=0, approx_factor=4, max_depth=400)

puzzle_blank = from_strs([
'#######',
'#     #',
])