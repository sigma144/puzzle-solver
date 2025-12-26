from solvernew import Solver, GridState, DIRECTIONS
from innertaolevels import *

class InnerTaoSolver(Solver):
    def setup(self, puzzle):
        puzzle, parity = puzzle
        state = GridState(puzzle)
        state.set_temp('p1', state.find('P.'))
        state.set_temp('p2', state.find('P-'))
        state.set_var('p', parity)
        self.goals = []
        for x, y in state.all_points():
            val = state.get(x, y)
            if 'P' in val:
                if (val[-1] == '.') != ('X' in val): state.set_temp('p1', (x, y))
                else: state.set_temp('p2', (x, y))
            if 'O' in val:
                self.goals.append((x, y))
                state.set(x, y, val.replace('O', ''))
        return state
    def get_next_states(self, state):
        states = {}
        x, y = state.get_temp('p2' if state.get_var('p') else 'p1')
        for dn, (dx, dy) in DIRECTIONS.items():
            new_state = self.copy_and_push(state, x, y, dx, dy)
            if new_state is not None:
                states[dn] = new_state
        new_state = state.copy()
        new_state.set_var('p', 1 - state.get_var('p'))
        new_state.set_score(0)
        states['S'] = new_state
        return states
    def push(self, state, x, y, dx, dy):
        nextx, nexty = x+dx, y+dy
        val = state.get(x, y); nextval = state.get(nextx, nexty)
        nextnextval = state.get(nextx+dx, nexty+dy)
        if nextval == '' or nextval == ' ':
            return False
        if len(nextval) == 1:
            if nextval != '.-'[state.get_var('p')]: return False
            state.set(nextx, nexty, 'P'+nextval)
        elif nextval[0] == 'X':
            if nextval[-1] != '.-'[state.get_var('p')]:
                state.set(nextx, nexty, 'PX'+nextval[-1])
            else:
                if len(nextnextval) != 1 or nextnextval == ' ': return False
                state.set(nextx+dx, nexty+dy, 'X'+nextnextval[-1])
                state.set(nextx, nexty, 'P'+nextval[-1])
        elif nextval[0] == 'P':
            if len(nextval) != 3: return False
            if nextval[-1] != '.-'[state.get_var('p')] or nextnextval != '.-'[state.get_var('p')]: return False
            state.set(nextx+dx, nexty+dy, 'PX'+nextnextval[-1])
            state.set(nextx, nexty, 'P'+nextval[-1])
            state.set_temp('p1' if state.get_var('p') else 'p2', (nextx+dx, nexty+dy))
        state.set(x, y, val[1:])
        state.set_temp('p2' if state.get_var('p') else 'p1', (nextx, nexty))
        return True
    def copy_and_push(self, state, x, y, dx, dy):
        new_state = state.copy()
        if not self.push(new_state, x, y, dx, dy):
            return None
        return new_state
    def check_finish(self, state):
        for x, y in self.goals:
            if 'X' not in state.get(x, y):
                return False
        return True
    def check_valid(self, state):
        return True #Consider adding puzzle specific checks here

def from_strs(strs):
    map = {'P':'P-', 'p':'P.', 'X':'X-', 'x':'X.', 'O':'O-', 'o':'O.'}
    return [[map.get(c) or c for c in s] for s in strs]

#############################################################################

InnerTaoSolver().solve((puzzle35, 1), debug=0, use_score=1, optimize_score=1, max_depth=200)
