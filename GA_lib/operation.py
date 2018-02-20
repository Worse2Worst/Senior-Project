import copy
import random
import GA_lib.GA
import collections




# A Chromosome(parents) is an array of genes(vehicles)
# A Gene is an array of indices of requests(pickup-delivery)
def crossover(DISTANCES, DURATIONS, timeWindows,REQUESTS, parent1, parent2, DEMANDS, LoadCapacities,maxSpot=10000,prob = 1.0):
    ##### Probability that they will not crossover ####################
    if (random.random() > prob):
        return parent1,parent2
    ##### Else, crossover #########################

    # All couples indices to visit
    totalReqs = set([i for i in range(len(REQUESTS))])
    rep1,rep2 = copy.deepcopy(parent1) ,copy.deepcopy(parent2)

    # Trim out the empty vehicles
    rep1 = [gene for gene in rep1 if (len(gene[1]) > 0)]
    rep2 = [gene for gene in rep2 if (len(gene[1]) > 0)]


    # Generate random range for crossover
    range1 = random.randint(1,len(rep1))
    range2 = random.randint(1,len(rep2))
    # Subpart 1,2 for crossover
    partFrom1 = random.sample(rep1,range1)
    partFrom2 = random.sample(rep2, range2)
    # partFrom1,partFrom2 = copy.deepcopy(partFrom1),copy.deepcopy(partFrom2)

    # # Remove subparts from original parents
    # child1 = [x for x in child1 if x not in partFrom1]
    # child2 = [x for x in child2 if x not in partFrom2]

    # reqsFrom1 is a set contains all requests in partFrom1, reqsFrom2 contains all requests in partFrom2
    listOfList1 = [reqs for [vehicle,reqs,route] in partFrom1]
    reqsFrom1 = [item for sublist in listOfList1 for item in sublist]
    listOfList2 = [reqs for [vehicle, reqs, route] in partFrom2]
    reqsFrom2 = [item for sublist in listOfList2 for item in sublist]


    ############## Crossing!!! #################
    vehiclesFrom1 = set([vehicle for [vehicle,reqs,route] in partFrom1])
    vehiclesFrom2 = set([vehicle for [vehicle,reqs,route] in partFrom2])
    # print('VehicleFrom1:'+str(vehiclesFrom1))
    # print('VehicleFrom2:'+str(vehiclesFrom2))

    # Remove the vehicles known to be replaced
    child1 = [[vehicle,reqs,route] for [vehicle,reqs,route] in rep1 if vehicle not in vehiclesFrom2]
    child2 = [[vehicle,reqs,route] for [vehicle,reqs,route] in rep2 if vehicle not in vehiclesFrom1]
    # Concat the part of chromosome
    child1 += partFrom2
    child2 += partFrom1


    # debugReq1 = [reqs for [vehicle,reqs,route] in child1]
    # dupsReq1 = [item for sublist in debugReq1 for item in sublist]
    # debugReq2 = [reqs for [vehicle,reqs,route] in child2]
    # dupsReq2 = [item for sublist in debugReq2 for item in sublist]
    # print('Dups in debugReqs1:'+str([item for item, count in collections.Counter(dupsReq1).items() if count > 1]))
    # print('Dups in debugReqs2:'+str([item for item, count in collections.Counter(dupsReq2).items() if count > 1]))
    # print('debugReq1:' + str(debugReq1))
    # print('debugReq2:' + str(debugReq2))


    # Remove the duplicate requests in children,
    GA_lib.GA.remove_requests(child1, vehiclesFrom2, reqsFrom2, REQUESTS)
    # compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
    GA_lib.GA.remove_requests(child2, vehiclesFrom1, reqsFrom1, REQUESTS)

    # Calculate remaining requests to insert
    usedReqs1 = [reqs for [vehicle, reqs, route] in child1]
    usedReqs1 = [item for sublist in usedReqs1 for item in sublist]
    usedReqs1 = set(usedReqs1)
    reqsToInsert1 = list(totalReqs - usedReqs1)
    usedReqs2 = [reqs for [vehicle, reqs, route] in child2]
    usedReqs2 = [item for sublist in usedReqs2 for item in sublist]
    usedReqs2 = set(usedReqs2)
    reqsToInsert2 = list(totalReqs - usedReqs2)
    # print('reqsToInsert1:'+str(reqsToInsert1))
    # print('reqsToInsert2:'+str(reqsToInsert2))

    ### Insert the remaining requests into the children ########
    GA_lib.GA.insert_requests_into_chromosome(child1, reqsToInsert1, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot)
    GA_lib.GA.insert_requests_into_chromosome(child2, reqsToInsert2, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot)

    return child1,child2


def mutate(chromosome,DISTANCES, DURATIONS, timeWindows,REQUESTS, DEMANDS, LoadCapacities,maxSpot,prob = 0.2):
    if (random.random() > prob):
        return chromosome
    num = random.randrange(len(chromosome))
    vehicleNum = chromosome[num][0]
    reqs = chromosome[num][1]
    chromosome[num] = [vehicleNum,[],[]]
    GA_lib.GA.insert_requests_into_chromosome(chromosome, reqs, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS,
                                              LoadCapacities, maxSpot)
    return chromosome