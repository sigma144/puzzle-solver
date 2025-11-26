
from solvernew import Solver, GridState, DIRECTIONS

class SokobanSolver(Solver):
    def setup(self, puzzle):
        board, target = puzzle
        self.target = GridState(board)
        state = GridState(target) #Solve in reverse
        state.x, state.y = state.find('P')
        return state
    def get_next_states(self, state):
        next = {}
        #x, y = state.find_and_track('P')
        x, y = state.x, state.y
        for dir, (dx, dy) in DIRECTIONS.items():
            x2 = x + dx; y2 = y + dy
            if state.get(x2, y2) == ' ':
                new_state = state.copy()
                #new_state.set_and_track(x2, y2, 'P')
                new_state.set(x2, y2, 'P')
                new_state.x, new_state.y = x2, y2
                new_state.set(x, y, ' ')
                next[dir] = new_state
                if state.get(x-dx, y-dy) == 'O':
                    new_state = new_state.copy()
                    new_state.x, new_state.y = x2, y2
                    new_state.set(x, y, 'O')
                    new_state.set(x-dx, y-dy, ' ')
                    new_state.set_score(2)
                    next[dir+'P'] = new_state
        return next
    def check_finish(self, state):
        return state == self.target
    
def convert(l):
    puzzle = []
    target = []
    for row in l:
        lp = []
        lt = []
        for c in row:
            if c == 'O':
                lp.append('O')
                lt.append(' ')
            elif c == 'X':
                lp.append(' ')
                lt.append('O')
            elif c == 'P':
                lp.append('P')
                lt.append(' ')
            elif c == 'E':
                lp.append(' ')
                lt.append('P')
            elif c == 'S':
                lp.append('O')
                lt.append('O')
            else:
                lp.append(c)
                lt.append(c)
        puzzle.append(lp)
        target.append(lt)
    return puzzle, target

testp, testt = convert([
    '#####',
    '# OX#',
    '# PE#',
    '#####'
])

puzzlex1 = [
    ['#','#','#','#','#','#','#','#','#'],
    ['#','#','#',' ',' ',' ','P','#','#'],
    ['#',' ','O','O','#','O','#','#','#'],
    ['#',' ',' ',' ',' ',' ',' ','#','#'],
    ['#','#','#',' ',' ',' ',' ','#','#'],
    ['#','#','#',' ',' ','#','#','#','#'],
    ['#','#','#','#','#','#','#','#','#']]
targetx1 = [
    ['#','#','#','#','#','#','#','#','#'],
    ['#','#','#',' ','P',' ',' ','#','#'],
    ['#',' ',' ',' ','#',' ','#','#','#'],
    ['#',' ',' ',' ','O',' ',' ','#','#'],
    ['#','#','#',' ','O','O',' ','#','#'],
    ['#','#','#',' ',' ','#','#','#','#'],
    ['#','#','#','#','#','#','#','#','#']]

puzzlex11 = [
    ['#','#','#','#','#','#','#','#','#'],
    ['#','#','#','#','#',' ',' ',' ','#'],
    ['#','#',' ',' ',' ',' ','#',' ','#'],
    ['#',' ','O','O','O','O',' ',' ','#'],
    ['#',' ','#',' ',' ','O',' ','#','#'],
    ['#',' ','#',' ','#','O',' ','#','#'],
    ['#',' ','#',' ',' ',' ',' ','#','#'],
    ['#',' ','#','#','#','O',' ',' ','#'],
    ['#',' ','P',' ',' ',' ',' ',' ','#'],
    ['#','#','#','#','#','#','#','#','#']]
targetx11 = [
    ['#','#','#','#','#','#','#','#','#'],
    ['#','#','#','#','#',' ','P',' ','#'],
    ['#','#',' ',' ',' ',' ','#',' ','#'],
    ['#',' ','O','O','O','O',' ',' ','#'],
    ['#',' ','#',' ',' ',' ',' ','#','#'],
    ['#',' ','#',' ','#','O',' ','#','#'],
    ['#',' ','#',' ',' ','O',' ','#','#'],
    ['#',' ','#','#','#','O',' ',' ','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#','#','#','#','#','#','#','#','#']]

puzzlex12 = [
    ['#','#','#','#','#','#','#','#','#','#','#'],
    ['#','#','#','#',' ',' ',' ','#','#','#','#'],
    ['#','#','#','#',' ','O',' ','O',' ','#','#'],
    ['#','#','#','#','#','O',' ','#',' ','#','#'],
    ['#',' ','O',' ','O',' ',' ','#',' ','#','#'],
    ['#',' ','#',' ',' ',' ','#','#',' ','#','#'],
    ['#',' ','#','#',' ',' ',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ','P',' ','#',' ',' ',' ','#'],
    ['#','#','#','#','#','#','#','#','#','#','#']]
targetx12 = [
    ['#','#','#','#','#','#','#','#','#','#','#'],
    ['#','#','#','#','P',' ',' ','#','#','#','#'],
    ['#','#','#','#',' ',' ',' ',' ',' ','#','#'],
    ['#','#','#','#','#',' ',' ','#','O','#','#'],
    ['#',' ',' ',' ',' ',' ',' ','#','O','#','#'],
    ['#',' ','#',' ',' ',' ','#','#','O','#','#'],
    ['#',' ','#','#',' ',' ',' ','O','O',' ','#'],
    ['#',' ',' ',' ',' ',' ','#',' ',' ',' ','#'],
    ['#','#','#','#','#','#','#','#','#','#','#']]



puzzle, target = convert([
    '#############',
    '####E########',
    '##   ########',
    '##    X O   #',
    '## X###  O  #',
    '##O######O ##',
    '#  X## X#  ##',
    '# S###  #O ##',
    '#   PX  #  ##',
    '######  #####',
    '#############',
])
'''
puzzle, target = convert([
    '#######',
    '###P ##',
    '#     #',
    '# #S#E#',
    '# # OX#',
    '#  S  #',
    '##   ##',
    '#######',
])
'''

#SokobanSolver().solve_optimal([testp, testt], use_score=1, optimize_score=0)
#SokobanSolver().solve_optimal([puzzlex11, targetx11], use_score=1, optimize_score=1)
SokobanSolver().solve_optimal([puzzle, target], optimize_score=0)