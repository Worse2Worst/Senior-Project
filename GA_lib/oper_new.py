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


# A Chromosome(parents) is an array of genes(vehicles)
# A Gene is an array of indices of requests(pickup-delivery)
def crossover(parent1,parent2):
    child1,child2 = parent1,parent2
    rand_num1 = random.randint(1,len(child1))
    rand_num2 = random.randint(1,len(child2))
    # subpart 1
    sub1 = random.sample(child1,rand_num1)
     
    #subpart 2
    sub2 = random.sample(child2, rand_num2)

    #remove subpart1 from child 1
    child1 = [x for x in child1 if x not in sub1]
    # remove subpart2 from child 2
    child2 = [x for x in child2 if x not in sub2]
    return child1,child2
