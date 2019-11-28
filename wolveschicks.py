from solver import Solver

class WolvesChicksState:
    def __init__(self, chicks1, wolves1, chicks2, wolves2, last_move, raft_location):
        self.chicks1 = chicks1
        self.wolves1 = wolves1
        self.chicks2 = chicks2
        self.wolves2 = wolves2
        self.last_move = last_move
        self.raft_location = raft_location
    def __repr__(self):
        string = ""
        for animal in range(self.chicks1):
            string += "C"
        for animal in range(self.wolves1):
            string += "W"
        string += " " + self.last_move + " "
        for animal in range(self.chicks2):
            string += "C"
        for animal in range(self.wolves2):
            string += "W"
        string += "\n"
        return string
    def __hash__(self):
        return hash((self.chicks1, self.wolves1, self.chicks2, self.wolves2, self.raft_location))
    def __eq__(self, other):
        if other == None:
            return False
        return self.chicks1 == other.chicks1 and self.chicks2 == other.chicks2 \
            and self.wolves1 == other.wolves1 and self.wolves2 == other.wolves2 \
            and self.raft_location == other.raft_location

class WolvesChicksSolver(Solver):
    def solve(self, chicks, wolves):
        self.solve_optimal(WolvesChicksState(chicks, wolves, 0, 0, "", 0))
        
    def get_next_states(self, state):
        states = []
        if state.raft_location == 0:
            #Move one chick
            states.append(WolvesChicksState(state.chicks1 - 1, state.wolves1, state.chicks2 + 1, state.wolves2, "C->", 1))
            #Move two chicks
            states.append(WolvesChicksState(state.chicks1 - 2, state.wolves1, state.chicks2 + 2, state.wolves2, "CC->", 1))
            #Move one wolf
            states.append(WolvesChicksState(state.chicks1, state.wolves1 - 1, state.chicks2, state.wolves2 + 1, "W->", 1))
            #Move two wolves
            states.append(WolvesChicksState(state.chicks1, state.wolves1 - 2, state.chicks2, state.wolves2 + 2, "WW->", 1))
            #Move chick and wolf
            states.append(WolvesChicksState(state.chicks1 - 1, state.wolves1 - 1, state.chicks2 + 1, state.wolves2 + 1, "CW->", 1))
        else:
            #Move one chick
            states.append(WolvesChicksState(state.chicks1 + 1, state.wolves1, state.chicks2 - 1, state.wolves2, "<-C", 0))
            #Move two chicks
            states.append(WolvesChicksState(state.chicks1 + 2, state.wolves1, state.chicks2 - 2, state.wolves2, "<-CC", 0))
            #Move one wolf
            states.append(WolvesChicksState(state.chicks1, state.wolves1 + 1, state.chicks2, state.wolves2 - 1, "<-W", 0))
            #Move two wolves
            states.append(WolvesChicksState(state.chicks1, state.wolves1 + 2, state.chicks2, state.wolves2 - 2, "<-WW", 0))
            #Move chick and wolf
            states.append(WolvesChicksState(state.chicks1 + 1, state.wolves1 + 1, state.chicks2 - 1, state.wolves2 - 1, "<-CW", 0))
        return states
            
    def check_state(self, state):
        return state.chicks1 >= 0 and state.chicks2 >= 0 and state.wolves1 >= 0 and state.wolves2 >= 0 and (state.chicks1 >= state.wolves1 or state.chicks1 == 0) and (state.chicks2 >= state.wolves2 or state.chicks2 == 0)

    def check_finish(self, state):
        return state.chicks1 == 0 and state.wolves1 == 0

WolvesChicksSolver().solve(3, 3)


        
    