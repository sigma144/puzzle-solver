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
        self.place_star(new_state, state.x, state.y)
        states.append(new_state)
        #Don't place star
        new_state = BinaryGridState(state.grid, state.x, state.y)
        new_state.grid[state.y][state.x] = -1
        states.append(new_state)
        return states

    def place_star(self, state, x, y):
        state.grid[y][x] = 1
        for dx, dy in DIRECTIONS8:
            if self.on_grid(state, x + dx, y + dy):
                state.grid[y + dy][x + dx] = -1
        #Update row
        if self.get_row(state, y).count(1) == self.star_amount:
            for X in range(len(state.grid[y])):
                if state.grid[y][X] == 0:
                    state.grid[y][X] = -1
        #Update column
        if self.get_column(state, x).count(1) == self.star_amount:
            for Y in range(len(state.grid)):
                if state.grid[Y][x] == 0:
                    state.grid[Y][x] = -1
        #Update region
        if self.get_region(state, x, y).count(1) == self.star_amount:
            for X, Y in self.get_region_points(x, y):
                if state.grid[Y][X] == 0:
                    state.grid[Y][X] = -1

    def iterate_state(self, state):
        updated = False
        for y,row in enumerate(self.rows(state)):
            count = 0
            for x,num in enumerate(row):
                if num == 1:
                    count += 1
                if num == 0:
                    count += 1
                    if x < len(row)-1 and row[x+1] == 0:
                        row[x+1] = 2
            
            if count < self.star_amount:
                return None
            if count == self.star_amount:
                for x,num in enumerate(row):
                    if num == 0 and not (x < len(row)-1 and row[x+1] == 2):
                        self.place_star(state, x, y)
                        updated = True

        for x,col in enumerate(self.columns(state)):
            count = 0
            for y,num in enumerate(col):
                if num == 1:
                    count += 1
                if num == 0:
                    count += 1
                    if y < len(col)-1 and col[y+1] == 0:
                        col[y+1] = 2
            
            if count < self.star_amount:
                return None
            if count == self.star_amount:
                for y,num in enumerate(col):
                    if num == 0 and not (y < len(col)-1 and col[y+1] == 2):
                        self.place_star(state, x, y)
                        updated = True

        for r,region in enumerate(self.regions(state)):
            count = region.count(0) + region.count(1)
            if count < self.star_amount:
                return None
            if count == self.star_amount:
                for x,y in self.get_all_region_points()[r]:
                    if state.grid[y][x] == 0:
                        self.place_star(state, x, y)
                        updated = True

        return updated

puzzle_easy = '1,1,2,2,2,1,1,1,2,2,3,1,1,2,4,3,3,3,5,4,3,3,3,5,5'
#1 star - ID: 8462991

puzzle_medium = '1,1,1,1,1,2,2,2,2,2,1,3,3,3,2,2,2,2,2,2,1,3,4,3,3,4,5,5,2,2,6,6,4,4,4,4,4,5,7,5,6,6,6,4,4,8,5,5,7,5,9,4,4,4,4,8,5,7,7,5,9,9,4,8,8,8,5,5,5,5,9,4,4,8,8,8,5,10,10,5,9,4,9,9,8,9,5,5,10,5,9,9,9,9,9,9,5,10,10,5'
#2 star - ID: 5933322

puzzle_hard = '1,1,1,1,1,2,2,2,2,2,2,3,3,3,1,4,4,4,1,1,1,5,5,5,5,6,6,3,7,7,4,1,1,1,1,5,5,5,5,6,6,3,7,4,4,5,5,5,5,5,6,6,5,6,3,3,7,7,4,5,5,5,4,4,4,6,6,6,3,3,7,4,4,4,4,4,4,8,8,8,8,8,3,3,7,7,7,4,4,9,9,9,9,9,9,8,3,3,7,10,7,10,4,11,11,11,9,12,12,8,3,3,7,10,10,10,10,11,9,9,9,12,12,8,3,3,7,10,10,13,13,11,9,14,9,12,8,8,3,3,7,10,10,13,11,11,9,14,9,12,8,8,8,3,7,10,13,13,11,11,13,14,14,12,12,8,12,12,7,13,13,13,13,13,13,14,12,12,12,12,12,12,7,7,13,13,13,14,14,14,14,14,14,14,14,14'
#3 star - ID: 7186464

puzzle_ultra = '1,1,1,1,1,1,1,1,1,1,1,2,2,2,3,3,3,3,4,5,5,5,5,5,5,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,4,4,4,5,5,5,5,5,5,1,1,1,1,1,1,1,1,1,1,1,2,2,2,3,3,4,4,4,5,5,5,5,5,5,6,1,6,1,6,1,1,1,1,1,1,2,2,3,3,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,1,1,1,1,1,2,2,3,3,3,4,4,4,4,4,7,7,7,7,7,8,9,9,6,6,6,1,10,1,1,1,1,1,3,4,4,4,4,4,4,4,4,4,7,7,8,8,9,6,1,1,1,10,1,11,11,11,1,3,4,11,4,4,4,7,7,7,7,7,7,8,8,9,6,1,9,1,10,10,12,12,11,11,11,11,11,4,4,4,4,4,7,7,7,7,8,8,9,9,9,9,9,9,10,10,12,11,13,13,13,11,4,4,14,14,7,7,7,7,7,8,8,8,9,15,9,10,9,10,12,12,12,13,11,11,11,4,4,14,7,7,7,7,14,7,8,8,8,15,15,9,10,10,10,10,12,13,13,13,11,11,13,13,14,14,7,7,14,14,7,8,8,8,15,10,9,9,10,12,12,12,12,12,13,13,13,13,14,14,14,14,14,14,16,16,8,8,15,15,10,10,10,10,10,12,12,12,12,12,13,12,13,14,14,17,14,16,16,16,16,8,15,15,15,15,12,12,12,12,12,12,12,12,12,12,12,14,14,17,17,14,16,16,16,16,8,8,15,15,15,12,12,12,12,12,12,12,12,12,18,14,14,19,19,17,14,17,16,16,16,8,8,15,15,15,12,15,15,15,12,12,12,12,12,18,14,19,19,17,17,17,17,16,16,16,20,8,20,15,15,15,15,15,21,21,18,12,18,18,18,19,19,19,19,19,17,17,16,16,16,20,20,20,20,20,15,15,15,15,21,18,12,18,18,19,19,19,22,19,17,17,17,17,16,16,20,20,20,20,20,20,15,21,21,21,18,18,18,19,19,22,19,22,19,17,17,17,17,16,16,20,20,20,20,20,20,20,21,23,21,21,21,21,21,21,22,19,22,22,17,17,17,16,16,16,20,20,20,20,20,20,20,21,23,23,23,21,21,22,22,22,22,22,22,17,17,17,17,16,16,20,24,24,24,20,24,20,23,23,23,23,21,23,22,25,25,25,22,22,22,17,17,17,17,17,24,24,24,24,24,24,24,23,23,23,23,21,23,23,25,22,22,22,22,22,22,22,22,22,22,24,24,24,24,24,23,23,23,23,23,23,23,23,25,25,25,22,22,22,22,22,22,22,22,22,24,24,24,24,23,23,23,23,23,23,23,23,23,23,23,25,25,25,25,25,25,22,22,22,22'
#6 star - 12/2020 Monthly Puzzle

StarBattleSolver().solve(puzzle_hard, 3)