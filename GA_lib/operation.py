import copy
import random
from random import randrange
import collections

def remove_request(route,requests,index):
    pickup = requests[index][0]
    delivery = requests[index][1]
    route.remove(pickup)
    route.remove(delivery)

# A Chromosome(parents) is an array of genes(vehicles)
# A Gene is an array of indices of requests(pickup-delivery)
def crossover(requests, parent1, parent2, prob = 0.8):
    ##### Probability that will not crossover ####################
    if (random.random() > prob):
        return parent1,parent2
    ##### Else, crossover #########################

    # All couples indices to visit
    all_copules = set([i for i in range(len(requests))])
    set1 = all_copules
    set2 = all_copules
    child1,child2 = copy.deepcopy(parent1) ,copy.deepcopy(parent2)

    # Trim out the empty vehicles
    sub1 = [gene for gene in child1 if (len(gene[1]) > 0)]
    sub2 = [gene for gene in child2 if (len(gene[1]) > 0)]

    # # Shuffle(not necessary)
    # random.shuffle(child1)
    # random.shuffle(child2)

    # Generate random range for crossover
    range1 = random.randint(1,len(sub1))
    range2 = random.randint(1,len(sub2))
    # Subpart 1,2 for crossover
    sub1 = random.sample(sub1,range1)
    sub2 = random.sample(sub2, range2)

    # Remove subparts from children
    child1 = [x for x in child1 if x not in sub1]
    child2 = [x for x in child2 if x not in sub2]

    # from1 is a set contains all requests in sub1, from2 contains all requests in sub2
    from1 = [reqs for [vehicle,reqs,route] in sub1]
    from1 = set.union(*from1)
    from2 = [reqs for [vehicle,reqs,route] in sub2]
    from2 = set.union(*from2)

    # Remove requests we cut out from the 'subs'
    set1 = set1 - from1
    set2 = set2 - from2

    # Remove the duplicate requests in children
    child1 = [[vehicleNum,reqs-from2,route] for [vehicleNum,reqs,route] in parent1]
    set1 = set1 - from2

    set2 = set2 - from1

    ################################## Unfinished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ##### this is how to select a random element from a set
    # random.choice(tuple(my_set))
    return child1,child2




