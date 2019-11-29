# Unbounded knapsack solver (allowing for repetition of items)
# Instead of using the solver superclass, this algorithm uses a greedy approach to get an initial solution and then iteratively improves it using an upper bound.
# This solver will not correctly handle negative values or weights.
# Designed to run well on large knapsacks

class KnapsackItem:
    def __init__(self, value, size):
        self.value = value
        self.size = size
        self.value_ratio = value / size

class KnapsackSolver:
    def solve(self, values, sizes, knapsack_size):
        items = [KnapsackItem(value, size) for value, size in zip(values, sizes)]
        items.sort(key=lambda item: item.value_ratio, reverse=True)
        knapsack = [ 0 for item in items ]
        #Greedy initialization: fill with best value item
        add_amount = knapsack_size // items[0].size
        knapsack[0] = add_amount
        total_value = add_amount * items[0].value
        total_space = knapsack_size % items[0].size
        best_value = total_value
        best_knapsack = knapsack[:]
        current_item = 1
        while True:
            #Check upper bound
            if current_item >= len(items) or total_value + total_space * items[current_item].value_ratio < best_value:
                current_item -= 1
                if knapsack[current_item] > 0:
                    #Remove all of previous item
                    total_value -= knapsack[current_item] * items[current_item].value
                    total_space += knapsack[current_item] * items[current_item].size
                    knapsack[current_item] = 0
                #Remove one item
                while knapsack[current_item] == 0:
                    if current_item == 0:
                        #Finished
                        print("Best knapsack (W" + str(knapsack_size) + "): " + str(sorted([("$" + str(items[i].value) + "-W" + str(items[i].size), amount) for i, amount in enumerate(best_knapsack)], key=lambda point: point[0])))
                        print("Total Value: $" + str(best_value))
                        return
                    current_item -= 1
                total_value -= items[current_item].value
                total_space += items[current_item].size
                knapsack[current_item] -= 1
                current_item += 1
                continue
            #Fill with the item
            add_amount = total_space // items[current_item].size
            if add_amount == 0:
                current_item += 1
                continue
            knapsack[current_item] += add_amount
            total_value += add_amount * items[current_item].value
            total_space %= items[current_item].size
            #Check value
            if total_value > best_value:
                best_value = total_value
                best_knapsack = knapsack[:]
            
KnapsackSolver().solve([1, 30], [1, 50], 100)
KnapsackSolver().solve([1, 60], [1, 55], 100)
KnapsackSolver().solve([10, 40, 50, 70], [1, 3, 4, 5], 8123)
KnapsackSolver().solve([7, 5, 2], [6, 5, 3], 155554)