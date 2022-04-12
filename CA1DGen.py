from copy import copy, deepcopy
import random
from scipy import spatial
from deap import base
from deap import creator
from deap import tools
#1100000000011
#-1 is padding
#Here is where we'll put test cases
#Tests are of the form, init, desired, time
individualSize = 16 #2-d Case
#individualSize = 99

Tests = []
Tests.append(([-1,0,0,0,0,0,0,0,0,0,-1],[-1,0,0,0,0,0,0,0,0,0,-1],3))
Tests.append(([-1,1,1,1,1,0,0,0,0,-1],[-1,1,1,1,1,0,0,0,0,-1], 3))
Tests.append(([-1,1,1,1,1,1,1,1,1,1,-1],[-1,1,1,1,1,1,1,1,1,1,-1],3))
Tests.append(([-1,0,1,1,0,0,1,0,1,-1],[-1,1,1,1,1,0,0,0,0,-1], 100))
Tests.append(([-1,0,1,1,0,0,1,1,0,-1],[-1,1,1,1,1,0,0,0,0,-1], 100))
Tests.append(([-1,0,1,1,1,0,0,0,0,-1],[-1,1,1,1,0,0,0,0,0,-1], 100))
Tests.append(([-1,0,1,0,1,0,1,0,1,-1],[-1,1,1,1,1,0,0,0,0,-1], 200))
Tests.append(([-1,0,0,0,0,1,1,1,1,-1],[-1,1,1,1,1,0,0,0,0,-1], 300))
# Tests.append(([-1,2,2,2,2,1,1,1,1,-1],[-1,1,1,1,1,2,2,2,2,-1], 300))
# Tests.append(([-1,0,1,2,1,0,1,0,1,-1],[-1,1,1,1,1,2,0,0,0,-1], 200))
# Tests.append(([-1,0,2,0,1,0,2,2,1,-1],[-1,1,1,2,2,2,0,0,0,-1], 200))
# Tests.append(([-1,2,2,2,2,0,0,0,0,-1],[-1,2,2,2,2,0,0,0,0,-1], 3))
# Tests.append(([-1,1,1,1,1,2,2,2,2,-1],[-1,1,1,1,1,2,2,2,2,-1], 3))
# Tests.append(([-1,0,0,0,0,2,2,2,2,-1],[-1,2,2,2,2,0,0,0,0,-1], 300))

def RunOneDCA(Init,DesiredResults,Rule,time, shouldPrint,printEnd):
    Current = Init
    Next = deepcopy(Current)
    for i in range(0,time):
        for j in range(1,len(Current)-1): #We'll need some gap to make it easier
            Next[j] = RunRule(Current[j-1],Current[j],Current[j+1],Rule)
        if shouldPrint:
            print(Next)
        if Next == Current:
            break
        else:
            Current = deepcopy(Next)
    
    if printEnd:
        print(Next)
    return -(spatial.distance.hamming(DesiredResults,Next))

BestGuess = [0   ,   1,   1,    1,   0,   1,     0,    0,    0,    1,   1,    1,    0,    0,    0  ,  1] #Matts Rule
#           00       01    10   11   000  001    010   011   100  101  110    111   00    01    10    11
def RunRule(c1,c2,c3,Rule):
    #print(c1,c2,c3)
    if c1 == -1:
        return Rule[(2*c2 + c3)]
    elif c3 == -1:
        return Rule[(len(Rule) - 4 + 2*c1 + c2)]
    else:
        return Rule[(4 + c1*4 + c2*2 + c3)]

def RunRule3(c1,c2,c3,Rule):
    #print(c1,c2,c3)
    if c1 == -1:
        return Rule[(3*c2 + c3)]
    elif c3 == -1:
        return Rule[(len(Rule) - 9 + 3*c1 + c2)]
    else:
        return Rule[(9 + c1*9 + c2*3 + c3)]

def mut3(ca,indp):
    if random.random() < indp:
        ca = random.randint(0,2)


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator 
#                      define 'attr_bool' to be an attribute ('gene')
#                      which corresponds to integers sampled uniformly
#                      from the range [0,1] (i.e. 0 or 1 with equal
#                      probability)
toolbox.register("attr_bool", random.randint, 0, 1)

toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_bool, individualSize) #264 is our rule size, 256 for 3, 8 for the edges.

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# the goal ('fitness') function to be maximized
def evalOneMax(individual):
    testTotal = 0
    for i in Tests:
        testTotal += RunOneDCA(i[0],i[1],individual,i[2],False,False)
    
    return testTotal,

def endingProof(individual):
    testTotal = 0
    for i in Tests:
        testTotal += RunOneDCA(i[0],i[1],individual,i[2],False,True)
    
    return testTotal,


#----------
# Operator registration
#----------
# register the goal / fitness function
toolbox.register("evaluate", evalOneMax)

# register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)

# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
toolbox.register("mutate", tools.mutUniformInt,low=0,up=1, indpb=0.05)

# operator for selecting individuals for breeding the next
# generation: each individual of the current generation
# is replaced by the 'fittest' (best) of three individuals
# drawn randomly from the current generation.
toolbox.register("select", tools.selTournament, tournsize=3)

#----------

def main():
    random.seed(64)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=300)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of 
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while max(fits) < 0 and g < 1000:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    evalOneMax(best_ind)
    endingProof(best_ind)
if __name__ == "__main__":
    endingProof(BestGuess)
    main()
    

