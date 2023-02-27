
from solver import Solver

class SokobanState:
    def __init__(self, board, x, y):
        self.x = x; self.y = y
        self.board = [row[:] for row in board]
    def __hash__(self):
        return hash(str(self.board))
    def __eq__(self, state):
        return self.x == state.x and self.y == state.y and str(self) == str(state)
    def __repr__(self) -> str:
        return '\n'.join([''.join(row) for row in self.board])

class SokobanSolver(Solver):
    def solve(self, board, target):
        self.target = SokobanState(board, 0, 0)
        start = SokobanState(target, 0, 0) #Solve in reverse 
        for y in range(len(target)):
            for x in range(len(target[y])):
                if target[y][x] == 'P':
                    start.x, start.y = x, y
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == 'P':
                    self.target.x, self.target.y = x, y
        print(start)
        print(self.target)
        move_list = self.solve_optimal(start)
        #move_list = self.solve_optimal_debug(start)
        for i in range(len(move_list)-1, -1, -1):
            print(move_list[i])
            input()
            print('\n\n\n\n')
        for i in range(-1, -len(move_list), -1):
            dx = move_list[i].x - move_list[i-1].x
            dy = move_list[i].y - move_list[i-1].y
            if dx == -1: print("R", end="")
            if dy == -1: print("D", end="")
            if dx == 1: print("L", end="")
            if dy == 1: print("U", end="")
            if i % 10 == 0: print()
    def get_next_states(self, state):
        next = []
        x = state.x; y = state.y
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x2 = x + dx; y2 = y + dy
            if state.board[y2][x2] == ' ':
                new_state = SokobanState(state.board, x2, y2)
                new_state.board[y2][x2] = 'P'
                new_state.board[y][x] = ' '
                next.append(new_state)
                if state.board[y - dy][x - dx] == 'O':
                    new_state = SokobanState(new_state.board, new_state.x, new_state.y)
                    new_state.board[y][x] = 'O'
                    new_state.board[y - dy][x - dx] = ' '
                    next.append(new_state)
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
    '# P #',
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


SokobanSolver().solve(puzzle, target)
