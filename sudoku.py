from solver import Solver, GridSolver

class SudokuState:
    def __init__(self, array, x, y):
        self.grid = []
        for row in array:
            self.grid.append(row[:])
        self.x = x; self.y = y
    def __repr__(self):
        string = ""
        for row in self.grid:
            for num in row:
                string += str(num) if num > 0 else "-"
            string += "\n"
        return string

class SudokuSolver(GridSolver):
    def solve(self, board):
        self.finished = False
        array = []
        for row in board:
            array.append([])
            for char in row:
                array[-1].append(0 if char == '-' else int(char))
        starting_state = SudokuState(array, 0, 0)
        print("Starting state: \n" + str(starting_state))
        self.solve_recursive(starting_state)
    def get_next_states(self, state):
        states = []
        for i in range(1, 10):
            if self.can_place(state, state.x, state.y, i):
                new_state = SudokuState(state.grid, state.x, state.y)
                new_state.grid[state.y][state.x] = i
                states.append(new_state)
        return states
    def can_place(self, state, x, y, num):
        #Check row
        if num in state.grid[y]:
            return False
        #Check column
        for Y in range(9):
            if state.grid[Y][x] == num:
                return False
        #Check square
        for X in range(3):
            for Y in range(3):   
                if state.grid[y // 3 * 3 + Y][x // 3 * 3 + X] == num:
                    return False
        return True

class SudokuSolverI(Solver): #Iterative version. It's about the same speed as the other one, maybe slightly slower. I mostly made it to demonstrate the iterative solving algorithm
    def solve(self, board):
        self.finished = False
        array = []
        for row in board:
            array.append([])
            for char in row:
                array[-1].append(0 if char == '-' else int(char))
        starting_state = SudokuState(array, 0, 0)
        self.starting_state = SudokuState(array, 0, 0)
        print("Starting state: \n" + str(starting_state))
        while starting_state.grid[starting_state.y][starting_state.x] != 0:
            starting_state = self.next_level(starting_state)
        self.solve_iterative(starting_state)
    def next_state(self, state):
        num = state.grid[state.y][state.x]
        if num == 9:
            return None
        if not self.can_place(state, state.x, state.y, num + 1):
            state.grid[state.y][state.x] += 1
            return self.next_state(state)
        state.grid[state.y][state.x] = num + 1
        return state
    def next_level(self, state):
        state.x += 1
        if state.x >= 9:
            state.x = 0
            state.y += 1
            if state.y >= 9:
                return None
        if self.starting_state.grid[state.y][state.x] == 0:
            return state
        else:
            return self.next_level(state)
    def prev_level(self, state):
        state.grid[state.y][state.x] = self.starting_state.grid[state.y][state.x]
        state.x -= 1
        if state.x < 0:
            state.x = 8
            state.y -= 1
            if state.y < 0:
                return None
        if self.starting_state.grid[state.y][state.x] == 0:
            return state
        else:
            return self.prev_level(state)
    def can_place(self, state, x, y, num):
        #Check row
        if num in state.grid[y]:
            return False
        #Check column
        for Y in range(9):
            if state.grid[Y][x] == num:
                return False
        #Check square
        for X in range(3):
            for Y in range(3):   
                if state.grid[y // 3 * 3 + Y][x // 3 * 3 + X] == num:
                    return False
        return True

board_easy = [
        "8769-----",
        "-1---6---",
        "-4-3-58--",
        "4-----21-",
        "-9-5-----",
        "-5--4-3-6",
        "-29-----8",
        "--469-173",
        "-----1--4"]

board_hard = [
        "8--------",
        "--36-----",
        "-7--9-2--",
        "-5---7---",
        "----457--",
        "---1---3-",
        "--1----68",
        "--85---1-",
        "-9----4--"]

SudokuSolver().solve(board_hard)


        
    