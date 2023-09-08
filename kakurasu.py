from solver import GridSolver, BinaryGridState

class KakurasuSolver(GridSolver):
    def solve(self, puzzle):
        totals = [int(num) for num in puzzle.split("/")]
        width = height = len(totals) // 2
        self.column_totals, self.row_totals = totals[:width], totals[width:]
        self.solve_recursive(BinaryGridState([[0 for x in range(width)] for y in range(height)], width - 1, height - 1))

    def get_next_states(self, state):
        states = []
        #Place block
        new_state = BinaryGridState(state.grid, state.x, state.y)
        new_state.set2(1)
        states.append(new_state)
        #Don't place block
        new_state = BinaryGridState(state.grid, state.x, state.y)
        new_state.set2(-1)
        states.append(new_state)
        return states

    def check_state(self, state):
        row = self.get_row(state, state.y)
        total_fill = 0
        total_empty = 0
        for i, num in enumerate(row):
            if num == 1:
                total_fill += i + 1
            if num == 0:
                total_empty += i + 1
        if total_fill > self.row_totals[state.y] or total_fill + total_empty < self.row_totals[state.y]:
            return False
        column = self.get_column(state, state.x)
        total_fill = 0
        total_empty = 0
        for i, num in enumerate(column):
            if num == 1:
                total_fill += i + 1
            if num == 0:
                total_empty += i + 1
        if total_fill > self.column_totals[state.x] or total_fill + total_empty < self.column_totals[state.x]:
            return False
        return True

puzzle_easy = '4/7/9/8/14/4/9/7/11/12'

puzzle_medium = '6/2/12/5/14/12/14/10/8/21/12/10/14/5'

puzzle_hard = '13/9/34/9/26/23/29/25/29/37/25/11/43/32/12/13/27/30'

puzzle_ultra = '38/17/21/42/2/12/45/45/7/45/59/30/40/5/54/57/38/35/18/42/58/35/36/1'

KakurasuSolver().solve(puzzle_hard)