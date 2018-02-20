import math
import random
import numpy as np
from GA_lib import evaluate



def initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,num_vehicles, DEMANDS, LoadCapacities,maxSpot = 1000):
    chromosome = [[0,[],[]]]
    reqsIndexToInsert = [*REQUESTS] # Every requests!!!
    chromosome = insert_requests_into_chromosome(chromosome, reqsIndexToInsert, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot)
    # Trim the empty gene
    # chromosome = [gene for gene in chromosome if (len(gene[1])>0)]
    return chromosome

def initialize_WorstCase_Chromosome(REQUESTS):
    chromosome = []
    i = 0
    for req, val in REQUESTS.items():
        # tour = [req[0],req[1]]
        tour = [val[0],val[1]]
        chromosome.append([i,[req],tour])
        i+=1
    return chromosome

# This function insert requests into a chromosome
def insert_requests_into_chromosome(chromosome, reqsIndexToInsert, DISTANCES, DURATIONS, timeWindows, REQUESTS,DEMANDS, LoadCapacities,maxSpot):
    if(not reqsIndexToInsert):
        # print('inserting -RouteEmpty - BuggED')
        return chromosome

    # Debugging,
    # oldReqsIndex = [reqs for [_,reqs,_] in chromosome]
    # oldReqsIndex = set([item for sublist in oldReqsIndex for item in sublist])
    # reqsSetToInsert = set(reqsIndexToInsert)
    # if((oldReqsIndex & reqsSetToInsert) != set()):
    #     print ('GA-Debug Inserting:Dups-Bug!!')
    #     print('Intersect:'+str(oldReqsIndex & reqsSetToInsert))
    #     print('Chromosome:'+str(chromosome))
    #     return 'BUG'

    # reqsIndexToInsert = list(reqsSetToInsert - (oldReqsIndex & reqsSetToInsert))

    ## Random things we want to insert.
    random.shuffle(reqsIndexToInsert)
    carNumsSet = set()
    while(reqsIndexToInsert): # while 'reqsIndexToInsert' is not empty
        # reqIndex = reqsIndexToInsert.pop(random.randrange(len(reqsIndexToInsert)))
        inf = 999999999
        minCost = inf
        minIndex = -99999
        minRoute = []
        reqIndex = reqsIndexToInsert.pop()
        insertingReq = REQUESTS[reqIndex]
        for (i,gene) in enumerate(chromosome):
            route = gene[2]
            carNumsSet.add(gene[0])
            newRoute,newCost = evaluate.new_tour_after_insert_requests(insertingReq, route, DISTANCES, DURATIONS, timeWindows, DEMANDS, LoadCapacities,maxSpot)
            if(newRoute and (newCost <minCost)): # Should insert
                minCost = newCost
                minIndex = i
                minRoute = newRoute
        # Can insert
        if(minIndex>=0):
            chromosome[minIndex][1].append(reqIndex)
            chromosome[minIndex][2] = minRoute
        else: # cannot insert, so we allocate a new vehicle
            nonNegNum = set([i for i in range(300)])
            s = nonNegNum - carNumsSet
            carNum = next(iter(s))
            # print('Debug at GA;Chromosome L is:'+str(len(chromosome))+',Carnum is:'+str(carNum))
            chromosome.append([carNum,[reqIndex],[REQUESTS[reqIndex][0],REQUESTS[reqIndex][1]]])
    return chromosome

# This function remove requests from a chromosome
def remove_requests(chromosome, tabooVehicles, reqsIndexToRemove, REQUESTS):
    for i,[num, reqs, route] in enumerate(chromosome):
        # Not removing the requests in the 'TABOO' Vehicles
        if (not num in tabooVehicles):
            for removingReq in reqsIndexToRemove:
                if (removingReq in reqs):
                    chromosome[i][1].remove(removingReq)
                    ## Also, remove the removing requests from the route
                    pickupNode = REQUESTS[removingReq][0]
                    deliveryNode = REQUESTS[removingReq][1]
                    chromosome[i][2].remove(pickupNode)
                    chromosome[i][2].remove(deliveryNode)









######################## JUNK###########################################
'''
def initialize_EMPTY_chromosome(num_vehicles):
    chromosome =[[car_num,[],[]] for car_num in range(num_vehicles)]
    return chromosome


'''