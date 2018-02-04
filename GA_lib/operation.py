import copy
import random
from random import randrange
import collections


def removeRequests(chromosome, tabooVehicles, reqsToRemove, requests):
    for [num, reqs, route] in chromosome:
        if (not num in tabooVehicles):
            for removingReq in reqsToRemove:
                if (removingReq in reqs):
                    reqs.remove(removingReq)
                    ## Also, remove the removing requests from the route
                    pickupNode = requests[removingReq][0]
                    deliveryNode = requests[removingReq][1]
                    route.remove(pickupNode)
                    route.remove(deliveryNode)

# A Chromosome(parents) is an array of genes(vehicles)
# A Gene is an array of indices of requests(pickup-delivery)
def crossover(REQUESTS, parent1, parent2, prob = 0.8):
    ##### Probability that they will not crossover ####################
    if (random.random() > prob):
        return parent1,parent2
    ##### Else, crossover #########################

    # All couples indices to visit
    totalReqs = set([i for i in range(len(REQUESTS))])
    child1,child2 = copy.deepcopy(parent1) ,copy.deepcopy(parent2)

    # Trim out the empty vehicles
    parent1 = [gene for gene in parent1 if (len(gene[1]) > 0)]
    parent2 = [gene for gene in parent2 if (len(gene[1]) > 0)]

    # # Shuffle(not necessary)
    # random.shuffle(child1)
    # random.shuffle(child2)

    # Generate random range for crossover
    range1 = random.randint(1,len(parent1))
    range2 = random.randint(1,len(parent2))
    # Subpart 1,2 for crossover
    partFrom1 = random.sample(parent1,range1)
    partFrom2 = random.sample(parent2, range2)
    # partFrom1,partFrom2 = copy.deepcopy(partFrom1),copy.deepcopy(partFrom2)

    # # Remove subparts from original parents
    # child1 = [x for x in child1 if x not in partFrom1]
    # child2 = [x for x in child2 if x not in partFrom2]

    # reqsFrom1 is a set contains all requests in partFrom1, reqsFrom2 contains all requests in partFrom2
    reqsFrom1 = [reqs for [vehicle,reqs,route] in partFrom1]
    reqsFrom1 = [item for sublist in reqsFrom1 for item in sublist]
    reqsFrom2 = [reqs for [vehicle, reqs, route] in partFrom2]
    reqsFrom2 = [item for sublist in reqsFrom2 for item in sublist]


    # # Remove requests we cut out from the 'partFrom'
    # reqRemainingSet1 = reqRemainingSet1 - reqsFrom1
    # reqRemainingSet2 = reqRemainingSet2 - reqsFrom2

    ############## Crossing!!! #################
    vehiclesFrom1 = set([x[0] for x in partFrom1])
    vehiclesFrom2 = set([x[0] for x in partFrom2])
    # Remove the vehicles known to be replaced
    child1 = [x for x in child1 if x[0] not in vehiclesFrom2]
    child2 = [x for x in child2 if x[0] not in vehiclesFrom1]
    # Append the part of chromosome
    child1 += partFrom2
    child2 += partFrom1
    # Remove the duplicate requests in children,
    removeRequests(child1, vehiclesFrom2, reqsFrom2, REQUESTS)
    removeRequests(child2, vehiclesFrom1, reqsFrom1, REQUESTS)
    # Calculate remaining requests to insert
    usedReqs1 = [reqs for [vehicle, reqs, route] in child1]
    usedReqs1 = [item for sublist in usedReqs1 for item in sublist]
    usedReqs1 = set(usedReqs1)
    toInsertReqs1 = totalReqs - usedReqs1
    usedReqs2 = [reqs for [vehicle, reqs, route] in child2]
    usedReqs2 = [item for sublist in usedReqs2 for item in sublist]
    usedReqs2 = set(usedReqs2)
    toInsertReqs2 = totalReqs - usedReqs2
    ### Insert the remaining requests into the children ########

    ################################## Unfinished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ##### this is how to select a random element from a set
    # random.choice(tuple(my_set))
    return child1,child2




