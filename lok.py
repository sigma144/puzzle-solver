from solver import Solver, NumberGridState, DIRECTIONS
from lokpuzzles import *

class LokSolver(Solver):
    def get_next_states(self, state):
        next_states = []
        for y, row in enumerate(state.grid):
            for x, c in enumerate(row):
                if c == 0 and state.puzzle[y][x] != 'X':
                    for d in DIRECTIONS:
                        for s in self.match(state, 'LOK', x, y, d[0], d[1]):
                            next_states += self.mark(s)
                        for s in self.match(state, 'TLAK', x, y, d[0], d[1]):
                            next_states += self.mark2(s)
                        for s in self.match(state, 'TA', x, y, d[0], d[1]):
                            next_states += self.mark_all(s)
                        for s in self.match(state, 'TA', x, y, d[0], d[1]):
                            next_states += self.mark_all(s)
                        for s in self.match(state, 'BE', x, y, d[0], d[1]):
                            next_states += self.add_letter(s)
                        for s in self.match(state, 'LOLO', x, y, d[0], d[1]):
                            next_states += self.clear_diagonals(s)
                        if self.griva:
                            for s in self.match(state, 'GRIVA', x, y, d[0], d[1]):
                                s.y = 'GRIVA'
                                next_states.append(s)
        #states = []
        #for s in next_states:
        #    if (str(s.grid), str(s.puzzle)) not in self.visited:
        #        self.visited[(str(s.grid), str(s.puzzle))] = s
        #        states.append(s)
        #if states:
        #    print(len(states))
        #return states
        return next_states
    def get_next(self, state, x, y, dx, dy):
        if not state.on_grid(x, y):
            return None
        if state.grid[y][x] > 0 or state.puzzle[y][x] == ' ':
            return self.get_next(state, x+dx, y+dy, dx, dy)
        return (x, y)
    def match(self, state, word, x, y, dx, dy, depth=0):
        if not state.on_grid(x, y):
            return []
        if depth > 20:
            return []
        next_states = []
        if state.puzzle[y][x] == 'X' or state.puzzle[y][x] == '?':
            paths = []
            for dx2, dy2 in DIRECTIONS:
                if dx == -dx2 and dy == -dy2:
                    continue
                loc = self.get_next(state, x+dx2, y+dy2, dx2, dy2)
                if loc is None:
                    continue
                paths += self.match(state, word, loc[0], loc[1], dx2, dy2, depth+1)
            if state.puzzle[y][x] == 'X':
                return paths
            else:
                next_states += paths
        if state.puzzle[y][x] != word[0] and state.puzzle[y][x] != '?':
            return next_states
        if len(word) == 1:
            new_state = NumberGridState(state.grid, state.x, 0)
            new_state.puzzle = state.puzzle
            new_state.grid[y][x] = state.x
            return [new_state] + next_states
        loc = self.get_next(state, x+dx, y+dy, dx, dy)
        if loc is None:
            return next_states
        result = self.match(state, word[1:], loc[0], loc[1], dx, dy, depth+1)
        for p in result:
            p.grid[y][x] = state.x
        return result + next_states
    def mark(self, state, two=False):
        next_states = []
        for y, row in enumerate(state.grid):
            for x, c in enumerate(row):
                if c == 0:
                    new_state = NumberGridState(state.grid, state.x+1, 0)
                    new_state.puzzle = state.puzzle
                    new_state.grid[y][x] = state.x
                    next_states.append(new_state)
        return next_states
    def mark2(self, state):
        next_states = []
        for y, row in enumerate(state.grid):
            for x, c in enumerate(row):
                if c == 0:
                    for dx, dy in ((1, 0), (0, 1)):
                        next = self.get_next(state, x+dx, y+dy, dx, dy)
                        if next is not None:
                            new_state = NumberGridState(state.grid, state.x+1, 0)
                            new_state.puzzle = state.puzzle
                            new_state.grid[y][x] = state.x
                            new_state.grid[next[1]][next[0]] = state.x
                            next_states.append(new_state)
        return next_states
    def mark_all(self, state):
        next_states = []
        letters = set()
        for y, row in enumerate(state.grid):
            for x, c in enumerate(row):
                if c == 0: letters.add(state.puzzle[y][x])
        for l in letters:
            new_states = [NumberGridState(state.grid, state.x+1, 0)]
            new_states[0].puzzle = state.puzzle
            for y, row in enumerate(state.grid):
                for x, c in enumerate(row):
                    if c != 0:
                        continue
                    if state.puzzle[y][x] == l:
                        for s in new_states:
                            s.grid[y][x] = state.x
                    elif state.puzzle[y][x] == '?':
                        new2 = []
                        for s in new_states:
                            new2.append(NumberGridState(s.grid, s.x, 0))
                            new2[-1].puzzle = s.puzzle
                            new2[-1].grid[y][x] = state.x
                        new_states += new2
            next_states += new_states
        return next_states
    def add_letter(self, state):
        next_states = []
        if self.allow_wild:
            letters = {'?'}
        else:
            letters = {'L', 'O', 'K', 'T', 'A', 'B', 'E', 'X'}
            for y, row in enumerate(state.grid):
                for x, c in enumerate(row):
                    if c == 0 and state.puzzle[y][x] not in '-':
                        letters.add(state.puzzle[y][x])
        for l in letters:
            for y, row in enumerate(state.grid):
                for x, c in enumerate(row):
                    if c == 0 and state.puzzle[y][x] == '-':
                        new_state = NumberGridState(state.grid, state.x+1, 0)
                        new_state.puzzle = state.puzzle[:]
                        new_state.puzzle[y] = new_state.puzzle[y][:x] + l + new_state.puzzle[y][x+1:]
                        next_states.append(new_state)
        return next_states
    def clear_diagonals(self, state):
        next_states = []
        size = max(state.width, state.height)
        for y0 in range(state.width + state.height):
            new_state = NumberGridState(state.grid, state.x+1, 0)
            new_state.puzzle = state.puzzle
            found = False
            for y in range(y0):
                x = y0 - y - 1
                if x >= state.width or y >= state.height:
                    continue
                if state.grid[y][x] == 0 and state.puzzle[y][x] != ' ':
                    new_state.grid[y][x] = state.x
                    found = True
            if found:
                next_states.append(new_state)
        return next_states
    def check_finish(self, state):
        if self.griva:
            return state.y == 'GRIVA'
        for row in state.grid:
            if 0 in row:
                return False
        return True
    def solve(self, puzzle, allow_wild=True):
        self.visited = {}
        self.allow_wild = allow_wild
        self.griva = puzzle == p80
        puzzle = [row + ' '*max([len(r)-len(row) for r in puzzle]) for row in puzzle]
        state = NumberGridState([[-1 if c == ' ' else 0 for c in r] for r in puzzle], 1, 0)
        state.puzzle = puzzle
        result = self.solve_recursive(state)
        if result:
            for s in [''.join([c for c in row]) for row in result.puzzle]: print(s)
        return result

LokSolver().solve(p80)
