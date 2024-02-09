from solver import GridSolver, NumberGridState

class SkyscrapersSolver(GridSolver):
    def solve(self, puzzle):
        if "," in puzzle:
            total_string, grid_numbers = puzzle.split(",")
        else:
            total_string, grid_numbers = puzzle, "0"
        totals = [int(num) if num else 0 for num in total_string.split("/")]
        width = height = len(totals) // 4
        self.totals_top = totals[:width]
        self.totals_bottom = totals[width:width*2]
        self.totals_left = totals[width*2:width*2+width]
        self.totals_right = totals[width*2+width:]
        state = NumberGridState([[0 for x in range(width)] for y in range(height)], 0, 0)
        state.grid = self.decode_grid_values(grid_numbers, width, height)
        self.solve_recursive(state)

    def get_next_states(self, state):
        states = []
        for i in range(len(self.totals_top)):
            if i + 1 not in self.get_row(state, state.y) and i + 1 not in self.get_column(state, state.x):
                new_state = NumberGridState(state.grid, state.x, state.y)
                new_state.set2(i + 1)
                states.append(new_state)
        return states

    def check_state(self, state):
        row = self.get_row(state, state.y)
        if not self.check_count(row, self.totals_left[state.y]) or not self.check_count(row[::-1], self.totals_right[state.y]):
            return False
        column = self.get_column(state, state.x)
        if not self.check_count(column, self.totals_top[state.x]) or not self.check_count(column[::-1], self.totals_bottom[state.x]):
            return False
        return True

    def check_count(self, array, count):
        if count == 0:
            return True
        min_height = 0
        min_total = 0
        max_height = 0
        max_total = 0
        for num in array:
            if num > min_height:
                min_total += 1
                min_height = num
            elif num == 0 and min_height < len(array):
                for i in range(len(array), min_height, -1):
                    if i not in array:
                        min_total += 1
                        min_height = i
                        break
            if num > max_height:
                max_total += 1
                max_height = num
            elif num == 0 and max_height < len(array):
                max_total += 1
                max_height += 1
        if min_total > count or max_total < count:
            return False
        return True
        
puzzle_test = '3/1/2/3/2/2/3/1/2/2/1/3/3/2/2/1'
#ID: 344330

puzzle_easy = '//2/2//2/////2/////,b2e2g'
#ID: 4260124

puzzle_medium = '/3//3////3//3////4/2//3/2//'
#ID: 5065052

puzzle_hard = '2//2//4///3/2///3/4/////2//3//4/3/,m1j1k'
#ID: 9640501

puzzle_ultra = '///6//6/2/2/5///5/3/3/3//4/////1//4/4//5//3//7/2/5/2/4/,e2c7zf6_2e3o3g3a5e'
#Monthly Puzzle 1-11-2019

SkyscrapersSolver().solve(puzzle_hard)