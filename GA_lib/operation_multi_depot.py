import copy
import random
from GA_lib import GA_multi_depot as GA
from GA_lib import evaluate_multi_depot as evaluate
import collections




# A Chromosome(parents) is an array of genes(vehicles)
# A Gene is an array of indices of requests(pickup-delivery)
def crossover(DISTANCES, DURATIONS, timeWindows,REQUESTS, parent1, parent2, DEMANDS, LoadCapacities,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,DEPOT,prob = 1.0):
    ##### Probability that they will not crossover ####################
    if (random.random() > prob):
        return parent1,parent2
    ##### Else, crossover #########################

    ## All indices of REQUESTS to visit
    totalReqs = set([*REQUESTS])
    rep1,rep2 = copy.deepcopy(parent1) ,copy.deepcopy(parent2)

    ## Trim out the empty vehicles
    rep1 = [gene for gene in rep1 if (len(gene[1]) > 0)]
    rep2 = [gene for gene in rep2 if (len(gene[1]) > 0)]

    ## Generate random range for crossover
    range1 = random.randint(1,len(rep1))
    range2 = random.randint(1,len(rep2))
    ## Subpart 1,2 for crossover
    partFrom1 = random.sample(rep1,range1)
    partFrom2 = random.sample(rep2,range2)

    ## reqsFrom1 is a set contains all requests in partFrom1, reqsFrom2 contains all requests in partFrom2
    reqsIndexFrom1 = [reqs for [vehicle,reqs,route] in partFrom1]
    reqsIndexFrom1 = [item for sublist in reqsIndexFrom1 for item in sublist]
    reqsIndexFrom2 = [reqs for [vehicle, reqs, route] in partFrom2]
    reqsIndexFrom2 = [item for sublist in reqsIndexFrom2 for item in sublist]


    ############## Crossing!!! #################
    vehiclesFrom1 = set([vehicle for [vehicle,reqs,route] in partFrom1])
    vehiclesFrom2 = set([vehicle for [vehicle,reqs,route] in partFrom2])

    ## Remove the vehicles known to be replaced
    child1 = [[vehicle,reqs,route] for [vehicle,reqs,route] in rep1 if vehicle not in vehiclesFrom2]
    child2 = [[vehicle,reqs,route] for [vehicle,reqs,route] in rep2 if vehicle not in vehiclesFrom1]
    ## Concat the part of chromosome
    child2 += partFrom1
    child1 += partFrom2

    # DEBUG
    # reqsIn1 = [reqs for [vehicle,reqs,route] in child1]
    # reqsIn1 = [item for sublist in reqsIn1 for item in sublist]
    # reqsIn2 = [reqs for [vehicle,reqs,route] in child2]
    # reqsIn2 = [item for sublist in reqsIn2 for item in sublist]
    # print('Dups in child1:'+str([item for item, count in collections.Counter(reqsIn1).items() if count > 1]))
    # print('ReqsIn1:'+str(reqsIn1))
    # print('Dups in child2:'+str([item for item, count in collections.Counter(reqsIn2).items() if count > 1]))
    # print('ReqsIn2:' + str(reqsIn2))

    ## Remove the duplicate requests in children,
    GA.remove_requests(child1, vehiclesFrom2, reqsIndexFrom2, REQUESTS)
    GA.remove_requests(child2, vehiclesFrom1, reqsIndexFrom1, REQUESTS)

    ## Calculate remaining requests to insert
    usedReqs1 = [reqs for [vehicle, reqs, route] in child1]
    usedReqs1 = [item for sublist in usedReqs1 for item in sublist]
    # if(len([item for item, count in collections.Counter(usedReqs1).items() if count > 1])>0):
    #     print('operation -usedReqs1-bug')
    usedReqs1 = set(usedReqs1)
    reqsToInsert1 = list(totalReqs - usedReqs1)
    # print('operation -ReqsToInsert1:'+str(reqsToInsert1))

    usedReqs2 = [reqs for [vehicle, reqs, route] in child2]
    usedReqs2 = [item for sublist in usedReqs2 for item in sublist]
    # if (len([item for item, count in collections.Counter(usedReqs2).items() if count > 1]) > 0):
    #     print('operation -usedReqs2-bug')
    usedReqs2 = set(usedReqs2)
    reqsToInsert2 = list(totalReqs - usedReqs2)
    # print('operation -ReqsToInsert2:' + str(reqsToInsert2))
    child2 = copy.deepcopy(child2)
    # print('RITI1'+str(reqsToInsert1))
    # print('RITI2-before'+str(reqsToInsert2))
    # print('Child2-before'+str(child2))
    # child2 = copy.deepcopy(child2)
    ### Insert the remaining requests into the children ########
    GA.insert_requests_into_chromosome(child1, reqsToInsert1, DISTANCES, DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS, DEPOT, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities)
    # if(a=='BUG'):
    #     print('Bug is child1111 :'+str(child1))
    # print('RITI2-after' + str(reqsToInsert2))
    # print('Child2-after' + str(child2))
    GA.insert_requests_into_chromosome(child2, reqsToInsert2,DISTANCES, DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS, DEPOT, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities)
    # if (a == 'BUG'):
    #     print('Bug is child2222:' + str(child2))
    # DEBUG
    # usedReqs2 = [reqs for [vehicle, reqs, route] in child2]
    # usedReqs2 = [item for sublist in usedReqs2 for item in sublist]
    # reqsToInsert2 = list(totalReqs - set(usedReqs2))
    # print('operation -Final-ReqsToInsert2:' + str(reqsToInsert2))

    return child1,child2


def mutate(chromosome,DISTANCES, DURATIONS, timeWindows,REQUESTS, DEMANDS, LoadCapacities,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,DEPOT,prob = 0.4):
    if (random.random() > prob):
        return chromosome
    res = copy.deepcopy(chromosome)
    index = random.randrange(len(res))
    vehicleNum = res[index][0]
    reqs = res[index][1]
    res[index] = [vehicleNum,[],[]]
    # GA_lib.GA.remove_requests(res, [], reqs, REQUESTS)
    # print(res)
    GA.insert_requests_into_chromosome(res,reqs, DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS, DEPOT, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities)
    return res

def tournament_selection(candidate1,candidate2,f1,f2):
    return candidate1 if(f1 > f2) else candidate2