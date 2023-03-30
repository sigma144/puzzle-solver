from solver import Solver
from sokochesslevels import *

class SokoChessState:
    def __init__(self, board):
        self.board = [row[:] for row in board]
    def __hash__(self):
        return hash(str(self.board))
    def __eq__(self, state):
        return self.board == state.board
    def __repr__(self) -> str:
        return '\n'.join([''.join([s.replace('*', '') if len(s) > 1 else s for s in row]) for row in self.board])+'\n'
    def get(self, x, y):
        if x < 0 or x >= len(self.board[0]):
            return ' '
        if y < 0 or y >= len(self.board):
            return ' '
        return self.board[y][x]
    def set(self, x, y, val):
        self.board[y] = self.board[y][:]
        self.board[y][x] = val
    def push(self, x, y, dx, dy):
        x2, y2 = x+dx, y+dy
        val = self.get(x, y)
        next = self.get(x2, y2)
        next2 = self.get(x2+dx, y2+dy)
        if next == ' ':
            return False
        elif next == '-':
            self.set(x2, y2, val)
        elif next == '*':
            self.set(x2, y2, val+'*')
        elif next == 'O':
            self.set(x2, y2, '-')
        elif next2 == '-':
            self.set(x2+dx, y2+dy, next.replace('*', ''))
            self.set(x2, y2, val)
        elif next2 == '*':
            self.set(x2+dx, y2+dy, next+'*')
            self.set(x2, y2, val)
        elif next2 == 'O':
            self.set(x2+dx, y2+dy, '-')
            self.set(x2, y2, val)
        else:
            return False
        self.set(x, y, ' ' if cracks[y][x] else '-')
        return True
    def copy_and_push(self, x, y, dx, dy):
        new_state = SokoChessState(self.board)
        result = new_state.push(x, y, dx, dy)
        if not result: return None
        new_state.last_move = (x+dx, y+dy)
        return new_state
    def copy_and_swap(self, x, y, dx, dy):
        x2, y2 = x+dx, y+dy
        val = self.get(x, y)
        next = self.get(x2, y2)
        if next == ' ': return None
        new_state = SokoChessState(self.board)
        if next == 'O':
            new_state.set(x, y, '-')
            new_state.set(x2, y2, '-')
        else:
            new_state.set(x, y, next)
            new_state.set(x2, y2, val)
        if cracks[y][x] and next == '-':
            new_state.set(x, y, ' ')
        new_state.last_move = (x2, y2)
        return new_state
    def copy_and_slide(self, x, y, dx, dy):
        next_states = []
        state = self
        val = state.get(x, y)
        next = state.get(x+dx, y+dy)
        while next != ' ':
            if next == '-':
                state = SokoChessState(state.board)
                state.set(x+dx, y+dy, val)
                state.set(x, y, ' ' if cracks[y][x] else '-')
                state.last_move = (x+dx, y+dy)
                next_states.append(state)
            else:
                result = state.copy_and_push(x, y, dx, dy)
                if result:
                    next_states.append(result)
                return next_states
            x += dx; y += dy
            val = state.get(x, y)
            next = state.get(x+dx, y+dy)
        return next_states
    def get_moves(self, x, y):
        states = []
        val = self.get(x, y)
        if val == 'p':
            if self.get(x, y-1) == '-':
                states.append(self.copy_and_push(x, y, 0, -1))
            if self.get(x+1, y-1) not in '- ':
                states.append(self.copy_and_push(x, y, 1, -1))
            if self.get(x-1, y-1) not in '- ':
                states.append(self.copy_and_push(x, y, -1, -1))
        elif val == 'k':
            for dx, dy in [(1, -2), (1, 2), (-1, 2), (-1, -2)]:
                states.append(self.copy_and_swap(x, y, dx, dy))
                states.append(self.copy_and_swap(x, y, dy, dx))
        if val == 'b' or val == 'q':
            states += self.copy_and_slide(x, y, 1, 1)
            states += self.copy_and_slide(x, y, -1, 1)
            states += self.copy_and_slide(x, y, 1, -1)
            states += self.copy_and_slide(x, y, -1, -1)
        if val == 'r' or val == 'q':
            states += self.copy_and_slide(x, y, 1, 0)
            states += self.copy_and_slide(x, y, -1, 0)
            states += self.copy_and_slide(x, y, 0, 1)
            states += self.copy_and_slide(x, y, 0, -1)
        return states

class SokoChessSolver(Solver):
    def solve(self, board, finish_state):
        board = [[c for c in row] for row in board]
        board = [row + [' ']*max([len(r)-len(row) for r in board]) for row in board]
        global cracks
        cracks = [[False for _ in row] for row in board]
        for y, row in enumerate(board):
            for x, s in enumerate(row):
                if s == '@' or x < len(finish_state[y]) and finish_state[y][x] == '@':
                    cracks[y][x] = True
                    if s == '@': board[y][x] = '-'
        starting_state = SokoChessState(board)
        self.finish_state = finish_state
        self.finish_points = []
        for y, row in enumerate(finish_state):
            for x, val in enumerate(row):
                if val in 'pkbrq':
                    self.finish_points.append((x, y))
        starting_state.last_move = (0, 0)
        self.solve_optimal(starting_state)
        #self.solve_optimal_debug(starting_state)
    def get_next_states(self, state):
        states = state.get_moves(*state.last_move)
        for y, row in enumerate(state.board):
            for x, val in enumerate(row):
                if (x, y) == state.last_move:
                    continue
                states += state.get_moves(x, y)
        return [s for s in states if s is not None]
    def check_finish(self, state):
        for x, y in self.finish_points:
            if self.finish_state[y][x] != state.get(x, y):
                return False
        return True

ptest, ftest = [
    'O*-',
    '*xp',
    'prp',
    'px*',
    '-*O',
],[
    'p-p',
    '---',
    '-r-',
    '---',
    'p-p',
]

SokoChessSolver().solve(p5, f5)