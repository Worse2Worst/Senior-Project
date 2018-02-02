from random import randrange
import collections
from random import randrange,randint,sample,choice
import random

# CrossOver, using Single-Point, MUST BE list of INT!!!!
def cxOnePoint(in1, in2):
    if(set(in1)!=set(in2)):
        print('BUGG!!!!!!!!!!!!!!!')
        return False
    ind1, ind2 = in1[:], in2[:]
    size = min(len(ind1), len(ind2))
    cxpoint1 = cxpoint2 = int(len(ind1)/2)
    temp1 = ind2[0:cxpoint2+1] + ind1
    temp2 = ind1[0:cxpoint2+1] + ind2
    ind1 = ind1[0:cxpoint1]
    for x in temp1:
        if x not in ind1:
            ind1.append(x)

    ind2 =ind2[0:cxpoint2]
    for x in temp2:
        if x not in ind2:
            ind2.append(x)
    return ind1, ind2

# CrossOver, using Partialy Matched, MUST BE list of INT!!!!
def cxPartialyMatched(in1, in2):
    ind1,ind2 = in1[:],in2[:]
    size = min(len(ind1), len(ind2))
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    temp1 = ind1[cxpoint1:cxpoint2+1] + ind2
    temp2 = ind1[cxpoint1:cxpoint2+1] + ind1
    ind1 = []
    for x in temp1:
        if x not in ind1:
            ind1.append(x)
    ind2 = []
    for x in temp2:
        if x not in ind2:
            ind2.append(x)
    return ind1, ind2


def mutInverseIndexes(individual):
    start, stop = sorted(random.sample(range(len(individual)), 2))
    individual = individual[:start] + individual[stop:start-1:-1] + individual[stop+1:]
    return individual,

# Mutation
def mutate(chromosome):
    random1 = randrange(0, len(chromosome))
    random2=random1
    while (random2==random1):
        random2 = randrange(0, len(chromosome))
    swap(chromosome,random1,random2)

# flat out tours to a long chromosome
def pTours_to_chrommosome(tours):
    return [item for sublist in tours for item in sublist]

def pTours_to_pVehicles(p_tours):
    return [len(sublist) for sublist in p_tours]

# Swap
def swap(array, i, j):
    array[i], array[j]= array[j], array[i]

def make_child(p_tours,couples,nodes,distances,durations,generations = 100):
    chromosomes = []
    for tours in p_tours:
        chromosome = tours_to_chrommosome(p_tours)
        chromosomes.append(chromosome)



def precedence_correction(tour, couples):
    visited = []
    for i in range(len(tour)):
        v = tour[i]
        couple = [item for item in couples if v in item][0]
        pickup = couple[0] # pickup node
        delivery = couple[1] # delivery node
        if (v == delivery): # v is delivery
            if (not pickup in visited): # the pickup node is not visited
                pickup_index = tour.index(pickup)
                tour.pop(pickup_index)
                tour.insert(i, pickup)
                visited.append(pickup)
                visited.append(v)
            else: # the sibling is visited
                visited.append(v)
        else: # v is pickup
            visited.append(v)
    return tour



