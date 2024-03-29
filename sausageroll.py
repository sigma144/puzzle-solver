from solver import Solver, BlockPushState, BlockPushStateD, Vec3, DIRECTIONS3D, DZERO, DLEFT, DRIGHT, DUP, DDOWN, DBELOW, DABOVE
from sausagerollpuzzles import *

chars = '><v^RLDUrldu****'*32
chars = '><v^'*32
nchars = ' .OS#FFFF'
SPACE = -1; FLOOR = -2; WALL = -3; PLAYER = -4; GRILL = -5; FORK = -6
FORKRIGHT = -6; FORKLEFT = -7; FORKDOWN = -8; FORKUP = -9
RIGHT = 0; LEFT = 1; DOWN = 2; UP = 3; COOKTOP = 4; COOKBOTTOM = 8
STABRIGHT = 16; STABLEFT = 32; STABDOWN = 48; STABUP = 64; 
GETDIR = 0b11; GETCOOK = 0b1100; GETSTAB = 0b110000

BlockPushState.define_params(chars, nchars, '><v^SF', {'<':'.<', '>':'.>', '^':'.^', 'v':'.v', 'S':'.S', 'F':'.F', 'u':' ^', 'd':' v', 'k':' <', 'r':' >', 'f':' F'})

class SSRState(BlockPushState):
    def __init__(self, state):
        super().__init__(state)
        self.pos = state.pos
        self.dir = state.dir
        self.remain = state.remain
        self.stab = False
        self.legal = True
        self.fallp = []
    @staticmethod
    def build_puzzle(puzzle, exceptions={'':[0]}, ):
        dims = (len(puzzle[0]), len(puzzle))
        puzzle = [' '*(len(puzzle[0])+2)] + [' '+row+' ' for row in puzzle] + [' '*(len(puzzle[0])+2)]
        state = BlockPushState.build_puzzle(puzzle, exceptions)
        state.pos = state.dir = DZERO
        state.remain = 0
        for p in state:
            if state.get(p) == PLAYER:
                state.pos = p
                if state.get(p + DLEFT) == FORK: state.dir = DLEFT
                if state.get(p + DRIGHT) == FORK: state.dir = DRIGHT
                if state.get(p + DUP) == FORK: state.dir = DUP
                if state.get(p + DDOWN) == FORK: state.dir = DDOWN
            if state.get(p) >= 0:
                state.remain += 2
        state.dims = dims
        return state
    def can_push(self, pos, dir, val): #Override
        if val == SPACE: return None
        if val == FLOOR or val == WALL or val == GRILL: return False
        return True
    def get_connected(self, pos, dir, val): #Override
        if val < 0: return []
        return [pos + DIRECTIONS3D[val & GETDIR]]
    def commit_push(self, pos, dir, val): #Override
        if val == PLAYER:
            if self.get(pos + DBELOW) == SPACE and pos.z <= 1:
                return False
            self.set(pos, val)
            return True
        if val < 0:
            self.set(pos, val)
            return True
        if not self.stab:
            if (val & GETDIR == LEFT or val & GETDIR == RIGHT) and dir.x == 0 or \
                (val & GETDIR == UP or val & GETDIR == DOWN) and dir.y == 0:
                if val & GETCOOK == COOKBOTTOM:
                    val = val - (val & GETCOOK) + COOKTOP
                elif val & GETCOOK == COOKTOP:
                    val = val - (val & GETCOOK) + COOKBOTTOM
        if self.get(pos + DBELOW) == GRILL:
            if val & COOKBOTTOM:
                self.legal = False
            else:
                val |= COOKBOTTOM
                self.remain -= 1
        if dir == DBELOW:
            if pos.z <= 1:
                self.legal = False
        if self.get(pos + DBELOW) == SPACE:
            self.fallp.append(pos)
            if pos - Vec3(1, 1, 0) not in SSRSolver.dims:
                if val & GETCOOK != COOKBOTTOM + COOKTOP:
                    self.legal = False
                    self.fallp.clear()
        self.set(pos, val)
    def fall(self):
        for p in self.fallp:
            self.push_connected(p, DBELOW)

class SSRSolver(Solver):
    dims = None
    def solve(self, puzzle, debug=0):
        self.targetpos = puzzle.pos
        self.targetdir = puzzle.dir
        SSRSolver.dims = Vec3(puzzle.dims[0], puzzle.dims[1], 10)
        self.solve_optimal(puzzle, debug=debug, showprogress=1, diff=0)
    def get_next_states(self, state):
        states = []
        for d in DIRECTIONS3D:
            newstate = SSRState(state)
            if d == state.dir:
                if newstate.push_connected(state.pos, d):
                    if newstate.get(state.pos + d + DBELOW) == GRILL:
                        newstate.push_connected(state.pos + d + d, -d)
                    else:
                        newstate.pos = newstate.pos + d
                    states.append(newstate)
            elif d == -state.dir:
                if newstate.push_connected(state.pos - d, d):
                    if newstate.get(state.pos + d + DBELOW) == GRILL:
                        newstate.push_connected(state.pos + d, -d)
                    else:
                        newstate.pos = newstate.pos + d
                    states.append(newstate)
            else:
                forkp = state.pos + state.dir
                if newstate.push_connected(forkp, d):
                    push2 = newstate.push_connected(forkp + d, -newstate.dir)
                    if push2:
                        newstate.dir = d
                        states.append(newstate)
                    #elif newstate.get(forkp + d) != SPACE:
                    #    newstate.set(forkp, newstate.get(forkp + d))
                    #    newstate.set(forkp + d, SPACE)
                    #    states.append(newstate)
        for s in states: s.fall()
        return states
    def check_state(self, state):
        return state.legal
    def check_finish(self, state):
        return state.remain <= 0 and state.legal and state.pos == self.targetpos and state.dir == self.targetdir

#ptest = SSRState.build_puzzle(
#    ['SF#..<>'])

#print(ptest)
#print(ptest._grid)
#print(ptest.pos, ptest.dir)

if __name__ == "__main__":
    SSRSolver().solve(pLachrymoseHead, debug=0)