# Required imports
import random
from deap import algorithms, base, creator, tools

# defining MAX weight
MAX_WEIGHT = 10
print(f"Max weight is: {MAX_WEIGHT}\n")
numberOfItems = 10


# items generation function
def generate_items(numberOfItems):
    items = []
    # Appending the item's pair of values (Weight & Value) into a list
    for i in range(numberOfItems):
        items.append({"Weight": random.randint(1, 10), "Value": random.uniform(0, 100)})

    return items


items = generate_items(10)
# Printing the generated items
for item in items:
    print(item)


# Defining the Fitness
creator.create("Fitness", base.Fitness, weights=(1.0,))
# Defining individual according to the given Fitness
creator.create("Individual", list, fitness=creator.Fitness)

# Initializing Toolbox
toolbox = base.Toolbox()

# Registering random attribute
toolbox.register("attr_bool", random.random, numberOfItems)

# Initializing individual and population
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=10)
toolbox.register("population", tools.initRepeat, list, toolbox.Individual)

# Fitness function
# Returns a tuple with the individual evaluation
def evalOneMax(individual):
    value = 0
    weight = 0

    for index in range(len(individual)):
        if individual[index] > 0.5:
            value += items[index]['value']
            weight += items[index]['weight']
    # Checking if the bag isn't overweighted
    if weight > MAX_WEIGHT:
        return 100000000, 0
    return weight, value