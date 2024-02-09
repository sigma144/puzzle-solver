from solver import GridSolver, BinaryGridState

#Broken

class BinairoSolver(GridSolver):
    def solve(self, puzzle, width, height):
        state = BinaryGridState([[-1 for x in range(width)] for y in range(height)], 0, 0)
        self.decode_grid_digits(state, puzzle, width, height)
        for y, row in enumerate(state.grid):
            for x, num in enumerate(row):
                if num == -1:
                    state.set(x, y, 0)
                elif num == 0:
                    state.set(x, y, -1)
        self.solve_recursive(state)
    def get_next_states(self, state):
        states = []
        new_state = BinaryGridState(state.grid, state.x, state.y)
        new_state.set(state.x, state.y, 1)
        states.append(new_state)
        new_state = BinaryGridState(state.grid, state.x, state.y)
        new_state.set(state.x, state.y, -1)
        states.append(new_state)
        return states
    def check_state(self, state):
        row = self.get_row(state, state.y)
        if row.count(1) > len(row) // 2 or row.count(-1) > len(row) // 2:
            return False
        for i in range(len(row) - 2):
            if row[i] != 0 and row[i] == row[i + 1] and row[i] == row[i + 2]:
                return False
        if state.x == len(row) - 1:
            for y, row2 in enumerate(self.rows(state)):
                if y != state.y and row == row2:
                    return False
        column = self.get_column(state, state.x)
        if column.count(1) > len(column) // 2 or column.count(-1) > len(column) // 2:
            return False
        for i in range(len(column) - 2):
            if column[i] != 0 and column[i] == column[i + 1] and column[i] == column[i + 2]:
                return False
        if state.y == len(column) - 1:
            for row in enumerate(self.rows(state)):
                if column == row:
                    return False
            for x, column2 in enumerate(self.columns(state)):
                if x != state.x and column == column2:
                    return False
            
        return True

puzzle_easy = 'a1b0e1b0a1a0b0f0e10c1h0c00a0b00a1k0e0c0f0d11d'
#10x10 - ID: 6309627

puzzle_medium = 'e0h1a1c11c00c1e0c0a0l10f0a00f1i0a0j0d1a0a1c1d0a0a0h0g1a10j00d00a1a0f0a0h0a1a0e0b00c'
#14x14 - ID: 5097767

puzzle_hard = 'a00a00c1b0e0h1a1a1h0b0j11c01a1b0d1g00a0b0e1c11g10a1e0e10b0n11d00f1l0b1a1a1f0b0a0j00c1e0b11b0f1b01f0b11b0e1l0c0d11c00g0h1a0c11a1j00e0e1a01h01b11c1c0a0a0g1a0c0b1f1a0e1g0i'
#20x20 - ID: 5355369

BinairoSolver().solve(puzzle_easy, 10, 10)