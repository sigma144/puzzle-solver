from solver import Solver, GridSolver

class ExampleState: #For basic solves
    def __init__(self):
        pass
    def __repr__(self):
        pass

class ExampleOState: #For optimal solves
    def __init__(self):
        pass
    def __repr__(self):
        pass
    def __hash__(self):
        pass
    def __eq__(self, other):
        pass

#For general puzzles
class ExampleSolver(Solver): 
    def solve(self, board):
        pass

    def get_next_states(self, state):
        return []

    def check_state(self, state):
        return True

    def check_finish(self, state):
        return True

#For grid-based puzzles
class ExampleGridSolver(GridSolver): 
    def solve(self, board):
        pass

    def get_next_states(self, state):
        return []

    def check_state(self, state):
        return True

    def check_finish(self, state):
        return True