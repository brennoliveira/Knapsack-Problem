# Required imports
import random
from deap import algorithms, base, creator, tools

# Defining MAX weight
MAX_WEIGHT = 50
print(f"Max weight is: {MAX_WEIGHT}\n")

# Items generation function
def generate_items(numberOfItems):
    items = []
    '''Ganerating random items (Weight & Value)
        and sotring them into the items' list '''
    for i in range(numberOfItems):
        items.append({"Weight": random.randint(1, 10), "Value": random.uniform(1, 100)})

    return items

items = generate_items(20)

# Showing the generated items
for item in items:
    print(item)

print("")

# Defining the Fitness
creator.create("Fitness", base.Fitness, weights=(1.0,))

# Defining individual according to the given Fitness
creator.create("Individual", list, fitness=creator.Fitness)

# Initializing Toolbox
toolbox = base.Toolbox()

# Registering random attribute
toolbox.register("attr_bool", random.random)

# Initializing individual and population
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=10)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Fitness function
# Returns a tuple with the individual evaluation
def evalOneMax(individual):
    value = 0
    weight = 0

    for index in range(len(individual)):
        if individual[index] > 0.5:
            value += items[index]['Value']
            weight += items[index]['Weight']

    # Checking if the bag isn't overweighted
    if weight > MAX_WEIGHT:
        return 100000000, 0
    return weight, value

# Get items function
def getItems(individual):
    _items = []
    for index in range(len(individual)):
        if individual[index] > 0.5:
            _items.append((index, items[index]))
    return _items
 
# Registering the Evaluation method, the Mutation and Selection into the toolbox
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.5)
toolbox.register("select", tools.selNSGA2)

# Defining the population size
population = toolbox.population(n=300)

# Defining number of generations
numberOfGen = 50

# Evolution process
for gen in range(numberOfGen):

    # The algorithms module implements many evolutionary algorithms
    # https://deap.readthedocs.io/en/master/api/algo.html
    # The function "varAnd" applies Mutation and Crossover operations
    # cxpb: Crossover probability
    # mutpb: Mutation probability
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)

    # Evaluating each individual
    fits = toolbox.map(toolbox.evaluate, offspring)

    # Associating each individual to its Fitness value
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = [fit[1]]

    # Applies the selection to generate a new population
    population = toolbox.select(offspring, k=len(population))

# Returns the best K individuals from the last population
topX = tools.selBest(population, k=10)

# Prints the best individual
print(topX[0])

# Printing every item
for item in getItems(topX[0]):
    print(item)

print("")

# Printing the total Value and Weight of the bag
print(f"Total Value: {sum(list(map(lambda x: x[1]['Value'], getItems(topX[0])))):.2f}")
print(f"Total Weight: {sum(list(map(lambda x: x[1]['Weight'], getItems(topX[0])))):.2f}")