from solver import Solver

class AbridgeState:
    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.tiles_left = sum([sum([val not in ' #*' for val in row]) for row in board])
    def __hash__(self):
        return hash(str(self.board))
    def __eq__(self, state):
        return str(self) == str(state)
    def __repr__(self) -> str:
        return '\n'.join([''.join(row) for row in self.board])
    def copy(self):
        state = AbridgeState([])
        state.board = [row[:] for row in self.board]
        state.tiles_left = self.tiles_left
        return state
    def push(self, x, y, dx, dy):
        nextx, nexty = x+dx, y+dy
        if self.board[nexty][nextx] == '#':
            return False
        if self.board[y][x] == '#' or self.board[y][x] == '*':
            return self.push(nextx, nexty, dx, dy)
        elif self.board[nexty][nextx] == ' ':
            self.board[nexty][nextx] = self.board[y][x]
            self.board[y][x] = ' '
            return True
        elif self.board[nexty][nextx] == '*':
            self.board[y][x] = ' '
            self.tiles_left -= 1
            return True
        else:
            if not self.push(nextx, nexty, dx, dy):
                return False
            self.board[nexty][nextx] = self.board[y][x]
            self.board[y][x] = ' '
            return True
    def copy_and_push(self, x, y, dx, dy):
        new_state = self.copy()
        result = new_state.push(x, y, dx, dy)
        return new_state if result else None

class AbridgeSolver(Solver):
    def solve(self, board):
        starting_state = AbridgeState(board)
        self.solve_optimal(starting_state)
    def get_next_states(self, state):
        states = []
        for y, row in enumerate(state.board):
            for x, val in enumerate(row):
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
                
        return [s for s in states if s != None]

    def check_finish(self, state):
        return state.tiles_left <= 0

puzzle_blank = [
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
]

puzzle = [
    ['#','#','#','#','#',' ',' ',' ',' '],
    ['#',' ','#',' ','#','#',' ',' ',' '],
    ['#',' ',' ',' ','B','#','#','#','#'],
    ['#',' ','#',' ','#','v',' ',' ','#'],
    ['#',' ','#',' ',' ',' ','>','<','#'],
    ['#','*','#',' ','#','^','B',' ','#'],
    ['#','#','#','#','#','#','#','#','#'],
]

AbridgeSolver().solve(puzzle)

puzzle_recursion = [
    ['#','#','#','#','#','#','#'],
    ['#',' ',' ','v',' ',' ','#'],
    ['#','>',' ',' ',' ',' ','#'],
    ['#','>',' ',' ',' ','<','#'],
    ['#',' ','^','*','^',' ','#'],
    ['#','#','#','#','#','#','#'],
]

puzzle_hurdle = [
    ['#','#','#','#','#','#','#','#','#'],
    ['#',' ','#','#','#','#','#','#','#'],
    ['#',' ','#','#','#','#','#','#','#'],
    ['#',' ',' ',' ',' ',' ',' ','<','#'],
    ['#',' ',' ',' ',' ',' ','v','<','#'],
    ['#',' ','>',' ','#',' ',' ','<','#'],
    ['#',' ',' ',' ','#',' ','^',' ','#'],
    ['#','*',' ',' ','#','^',' ',' ','#'],
    ['#','#','#','#','#','#','#','#','#'],
]

puzzle_assist = [
    ['#','#','#','#','#'],
    ['#','#',' ','#','#'],
    ['#','#',' ','#','#'],
    ['#',' ',' ','*','#'],
    ['#','#',' ','#','#'],
    ['#','>','v','<','#'],
    ['#',' ','B',' ','#'],
    ['#','#','#','#','#'],
]

puzzle_return = [
    ['#','#','#','#','#','#','#','#','#'],
    ['#',' ',' ','#',' ',' ',' ','*','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ','#'],
    ['#','>',' ',' ','#','^',' ',' ','#'],
    ['#','#',' ','#','#','#','#','#','#'],
    ['#','#',' ','#',' ',' ',' ',' ','#'],
    ['#',' ',' ',' ','>','v',' ',' ','#'],
    ['#','#',' ','#','#','#',' ','B','#'],
    ['#','#','#','#','#','#','#','#','#'],
]

#AbridgeSolver().solve(puzzle_recursion)

        
    