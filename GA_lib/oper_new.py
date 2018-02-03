from random import randrange
import collections
import copy
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


# A Chromosome(parents) is an array of genes(vehicles)
# A Gene is an array of indices of requests(pickup-delivery)
def crossover(couples,parent1,parent2,prob = 0.8):
    ##### Probability that will not crossover
    if (random.random() > prob):
        return parent1,parent2
    ##### Else, crossover
    # All couples indices to visit
    all_copules = set([i for i in range(len(couples))])
    #
    child1,child2 = copy.deepcopy(parent1) ,copy.deepcopy(parent2)
    # Trim out the empty vehicles
    child1 = [gene for gene in child1 if (len(gene[1]) > 0)]
    child2 = [gene for gene in child2 if (len(gene[1]) > 0)]

    # # Shuffle(not necessary)
    # random.shuffle(child1)
    # random.shuffle(child2)

    # Generate random range for crossover
    range1 = random.randint(1,len(child1))
    range2 = random.randint(1,len(child2))
    # Subpart 1,2 for crossover
    sub1 = random.sample(child1,range1)
    sub2 = random.sample(child2, range2)

    # Remove subparts from children
    child1 = [x for x in child1 if x not in sub1]
    child2 = [x for x in child2 if x not in sub2]

    # set1 contains all requests in sub1
    set1 = [reqs for [vehicle, reqs] in sub1]
    set1 = set.union(*set1)
    set2 = [reqs for [vehicle, reqs] in sub2]
    set2 = set.union(*set2)


    # Unfinished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ##### this is how to select a random element from a set
    # random.choice(tuple(my_set))
    return child1,child2
