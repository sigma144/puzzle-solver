import pickle
from solvernew import Solver, GridState, DIRECTIONS8, DIRECTIONS, DIRECTIONSDIAG

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
            if val[0] == 'O':
                state.inc_temp('circles')
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
                if val[0] in ' #X' or move == p:#or state.get_temp('sym') == p:
                    continue
                if val[-1] == 'c':
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
                        else: return {}
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
    def approximate(self, state):
        return state.get_temp('tiles')
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
                if state.get_temp('circles') == 0:
                    state.del_temp('circles')
            state.set(x, y, ' ')
            return True
        else:
            if not self.push(state, nextx, nexty, dx, dy):
                return False
            state.set(nextx, nexty, val)
            state.set(x, y, ' ')
            return True
    def copy_and_push(self, state, x, y, dx, dy, circle=False, symcircle=False):
        new_state = state.copy()
        new_state.del_temp('click')
        val = state.get(x, y)
        if symcircle and state.get_temp('sym') is not None:
            if not self.push(new_state, x, y, dx, dy):
                return None
            sx, sy = state.get_temp('sym')
            if x == sx and y == sy:
                self.push(new_state, x-dx, y-dy, dx, dy)
            elif (x+dx+dx != sx or y+dy+dy != sy) and state.get(sx, sy) == new_state.get(sx, sy):
                if state.get(sx-dx-dx, sy-dy-dy) == state.get(x+dx, y+dy):
                    if not self.push(new_state, sx, sy, dx, dy):
                        return None
                elif not self.push(new_state, sx-dx, sy-dy, dx, dy):
                    return None
            if state.get(sx+dx, sy+dy) == '*':
                new_state.del_temp('sym')
            else: new_state.set_temp('sym', (sx+dx, sy+dy))
        elif not circle and val[-1] == 's' and state.get_temp('sym') is not None:
            if not self.push(new_state, x, y, dx, dy):
                return None
            sx, sy = state.get_temp('sym')
            sdx = dx; sdy = dy
            if state.get(sx, sy)[0] != val[0]:
                sdx = -sdx; sdy = -sdy
            if (x+dx != sx or y+dy != sy) and state.get(sx, sy) == new_state.get(sx, sy) \
                and not self.push(new_state, sx, sy, sdx, sdy):
                return None
            if state.get(sx+sdx, sy+sdy) == '*':
                new_state.del_temp('sym')
            else: new_state.set_temp('sym', (sx+sdx, sy+sdy))
            if len(state.get(sx, sy)) == 3:
                new_state.set(sx, sy, '#')
        elif not self.push(new_state, x, y, dx, dy):
            return None
        if circle:
            new_state.set_var('move', (x+dx+dx, y+dy+dy))
        else:
            new_state.set_var('move', (x+dx, y+dy))
            if val[-1] == 'c' or len(val) == 3:
                new_state.set(x, y, '#')
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
'################',
'## ## #####   ##',
'#     ##### * ##',
'## ##    ##   X#',
'#  ##### ####  #',
'## ###   ## XX #',
'## ##  #### ####',
'#O ###      ####',
'#O B###v########',
'#XY### X #######',
'################',
])

AbridgeSolver().solve(puzzle, debug=0, use_score=0, optimize_score=1,
                      approximate=1, approx_factor=10, max_depth=186)

puzzle_blank = from_strs([
'#######',
'#     #',
])