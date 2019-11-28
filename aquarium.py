from solver import GridSolver, BinaryGridState

class AquariumSolver(GridSolver):

    def solve(self, puzzle):
        totals, regions = puzzle.split(";")
        totals = [int(num) for num in totals.split("_")]
        width = height = len(totals) // 2
        self.column_totals, self.row_totals = totals[:width], totals[width:]
        self.decode_regions(regions, width, height)
        self.solve_recursive(BinaryGridState([[0 for x in range(width)] for y in range(height)], 0, 0))
        
    def get_next_states(self, state):
        states = []
        region = self.get_region_points(state.x, state.y)
        min_height = min([y for x, y in region])
        max_height = max([y for x, y in region])
        new_state = BinaryGridState(state.grid, state.x, state.y)
        for x, y in region:
            new_state.grid[y][x] = 1
        states.append(new_state)
        for height in range(min_height, max_height + 1):
            new_state = BinaryGridState(new_state.grid, state.x, state.y)
            for x, y in region:
                if height == y:
                    new_state.grid[y][x] = -1
            states.append(new_state)
        return states

    def check_state(self, state):
        for y, row in enumerate(self.rows(state)):
            total_water = row.count(1)
            total_space = row.count(-1)
            if total_water > self.row_totals[y] or total_space > len(row) - self.row_totals[y]:
                return False
        for x, column in enumerate(self.columns(state)):
            total_water = column.count(1)
            total_space = column.count(-1)
            if total_water > self.column_totals[x] or total_space > len(column) - self.column_totals[x]:
                return False
        return True

puzzle_easy = '2_4_1_1_3_3_1_1_2_2_3_5;1,2,3,4,5,5,1,2,3,4,6,7,8,8,9,10,10,7,11,11,9,9,12,12,13,13,14,15,16,17,18,18,14,15,16,17'
#ID: 2199505

puzzle_hard = '5_7_6_5_7_10_8_10_12_10_8_8_3_5_1_3_10_5_8_10_7_5_5_5_4_3_8_9_10_13;1,1,1,2,2,2,3,3,4,4,4,4,5,5,6,7,1,8,8,2,3,3,4,4,9,9,4,5,6,6,7,10,11,12,12,13,13,13,9,9,9,14,14,14,15,7,10,11,11,16,13,13,9,9,17,17,17,14,17,15,11,10,11,16,16,13,13,18,18,18,18,17,17,17,15,11,11,11,11,16,19,19,19,19,18,20,20,15,15,15,11,21,21,11,11,22,23,24,18,18,25,25,15,26,26,21,21,11,11,11,22,23,24,18,18,25,25,15,15,26,27,27,28,23,23,23,23,24,24,24,29,25,25,15,26,27,27,28,28,28,28,30,30,30,24,29,29,25,26,26,31,27,32,32,33,33,33,30,34,35,35,29,36,26,26,31,37,38,32,33,33,33,34,34,35,29,29,36,36,26,31,37,38,39,39,40,40,41,35,35,42,42,36,36,26,31,38,38,39,43,43,40,41,41,41,44,45,45,26,26,38,38,39,39,41,41,41,41,41,44,44,45,45,26,26'
#ID: 3002029

AquariumSolver().solve(puzzle_easy)


        
    