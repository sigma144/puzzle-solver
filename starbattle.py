from solver import GridSolver, BinaryGridState, DIRECTIONS, DIRECTIONS8

class StarBattleSolver(GridSolver):
    def solve(self, puzzle, star_amount):
        self.decode_regions(puzzle)
        self.star_amount = star_amount
        self.solve_recursive(BinaryGridState([[0 for x in range(len(self._regions))] for y in range(len(self._regions))], 0, 0))

    def get_next_states(self, state):
        states = []
        #Place star
        new_state = BinaryGridState(state.grid, state.x, state.y)
        new_state.grid[state.y][state.x] = 1
        for dx, dy in DIRECTIONS8:
            if self.on_grid(new_state, state.x + dx, state.y + dy):
                new_state.grid[state.y + dy][state.x + dx] = -1
        #Update row
        if self.star_amount == 1 or self.get_row(new_state, state.y).count(1) == self.star_amount:
            for x in range(len(new_state.grid[state.y])):
                if new_state.grid[state.y][x] == 0:
                    new_state.grid[state.y][x] = -1
        #Update column
        if self.star_amount == 1 or self.get_column(new_state, state.x).count(1) == self.star_amount:
            for y in range(len(new_state.grid)):
                if new_state.grid[y][state.x] == 0:
                    new_state.grid[y][state.x] = -1
        #Update region
        if self.star_amount == 1 or self.get_region(state, state.x, state.y).count(1) == self.star_amount:
            region = self.get_region_points(state.x, state.y)
            for x, y in region:
                if new_state.grid[y][x] == 0:
                    new_state.grid[y][x] = -1
        states.append(new_state)
        #Don't place star
        new_state = BinaryGridState(state.grid, state.x, state.y)
        new_state.grid[state.y][state.x] = -1
        states.append(new_state)
        return states

    def check_state(self, state):
        for row in self.rows(state):
            if row.count(0) + row.count(1) < self.star_amount:
                return False
        for column in self.columns(state):
            if column.count(0) + column.count(1) < self.star_amount:
                return False
        for region in self.regions(state):
            if region.count(0) + region.count(1) < self.star_amount:
                return False
        return True

puzzle_easy = '1,1,2,2,2,1,1,1,2,2,3,1,1,2,4,3,3,3,5,4,3,3,3,5,5'
#1 star - ID: 8462991

puzzle_medium = '1,1,1,1,1,2,2,2,2,2,1,3,3,3,2,2,2,2,2,2,1,3,4,3,3,4,5,5,2,2,6,6,4,4,4,4,4,5,7,5,6,6,6,4,4,8,5,5,7,5,9,4,4,4,4,8,5,7,7,5,9,9,4,8,8,8,5,5,5,5,9,4,4,8,8,8,5,10,10,5,9,4,9,9,8,9,5,5,10,5,9,9,9,9,9,9,5,10,10,5'
#2 star - ID: 5933322

puzzle_hard = '1,1,1,1,1,2,2,2,2,2,2,3,3,3,1,4,4,4,1,1,1,5,5,5,5,6,6,3,7,7,4,1,1,1,1,5,5,5,5,6,6,3,7,4,4,5,5,5,5,5,6,6,5,6,3,3,7,7,4,5,5,5,4,4,4,6,6,6,3,3,7,4,4,4,4,4,4,8,8,8,8,8,3,3,7,7,7,4,4,9,9,9,9,9,9,8,3,3,7,10,7,10,4,11,11,11,9,12,12,8,3,3,7,10,10,10,10,11,9,9,9,12,12,8,3,3,7,10,10,13,13,11,9,14,9,12,8,8,3,3,7,10,10,13,11,11,9,14,9,12,8,8,8,3,7,10,13,13,11,11,13,14,14,12,12,8,12,12,7,13,13,13,13,13,13,14,12,12,12,12,12,12,7,7,13,13,13,14,14,14,14,14,14,14,14,14'
#3 star - ID: 7186464

StarBattleSolver().solve(puzzle_medium, 2)