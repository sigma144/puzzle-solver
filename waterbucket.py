from solver import Solver

class WaterBucketState:
    def __init__(self, level1, level2):
        self.level1 = level1
        self.level2 = level2
    def __hash__(self):
        return hash((self.level1, self.level2))
    def __eq__(self, other):
        if (other == None):
            return False
        return self.level1 == other.level1 and self.level2 == other.level2
    def __repr__(self):
        return "[" + str(self.level1) + ", " + str(self.level2) + "]"

class WaterBucketSolver(Solver):
    def solve(self, bucket_size_1, bucket_size_2, target_level):
        self.bucket_size_1 = bucket_size_1
        self.bucket_size_2 = bucket_size_2
        self.target_level = target_level
        return self.solve_optimal(WaterBucketState(0, 0))
    def get_next_states(self, state):
        states = []
        #Fill bucket 1
        states.append(WaterBucketState(self.bucket_size_1, state.level2))
        #Fill bucket 2
        states.append(WaterBucketState(state.level1, self.bucket_size_2))
        #Empty bucket 1
        states.append(WaterBucketState(0, state.level2))
        #Empty bucket 2
        states.append(WaterBucketState(state.level1, 0))
        #Bucket 1 into bucket 2
        amount_1_2 = min(state.level1, self.bucket_size_2 - state.level2)
        states.append(WaterBucketState(state.level1 - amount_1_2, state.level2 + amount_1_2))
        #Bucket 2 into bucket 1
        amount_2_1 = min(state.level2, self.bucket_size_1 - state.level1)
        states.append(WaterBucketState(state.level1 + amount_2_1, state.level2 - amount_2_1))
        return states
    def check_finish(self, state):
        return state.level1 == self.target_level or state.level2 == self.target_level
        
while True:
    size1 = input("Size of 1st jug: ")
    size2 = input("Size of 2nd jug: ")
    level = input("Amount of liquid to measure: ")
    WaterBucketSolver().solve(int(size1), int(size2), int(level))
    print()


        
    