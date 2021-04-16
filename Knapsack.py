# Required imports
import random
from deap import algorithms, base, creator, tools

# defining MAX weight
MAX_WEIGHT = 50
print(f"Max weight is: {MAX_WEIGHT}\n")
#numberOfItems = 5


# items generation function
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

def getItems(individual):
    _items = []
    for index in range(len(individual)):
        if individual[index] > 0.5:
            _items.append((index, items[index]))
    return _items


toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.5)

toolbox.register("select", tools.selNSGA2)

population = toolbox.population(n=300)

numberOfGen = 50
for gen in range(numberOfGen):

    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)

    # avalia cada indivíduo
    fits = toolbox.map(toolbox.evaluate, offspring)

    # associa cada indivíduo ao seu valor de fitness
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = [fit[1]]

    population = toolbox.select(offspring, k=len(population))

 #   best = tools.selBest(population, k=1)

top10 = tools.selBest(population, k=10)

# Imprime o melhor
print(top10[0])

for item in getItems(top10[0]):
    print(item)

print("")

print(f"{sum(list(map(lambda x: x[1]['Value'], getItems(top10[0]))))}")
print(f"{sum(list(map(lambda x: x[1]['Weight'], getItems(top10[0]))))}")