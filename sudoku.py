from solver import NumberGridState, GridSolver

class SudokuSolver(GridSolver):
    def solve(self, board):
        array = [[0 if c == '-' else int(c) for c in row] for row in board]
        starting_state = NumberGridState(array, 0, 0)
        print("Starting state: \n" + str(starting_state))
        self.solve_recursive(starting_state)
    def get_next_states(self, state):
        states = []
        for i in range(1, 10):
            if self.can_place(state, state.x, state.y, i):
                new_state = NumberGridState(state.grid, state.x, state.y)
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
    def iterate_state(self, state):
        return self.iterate_valid_placements(state)
    
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


        
    