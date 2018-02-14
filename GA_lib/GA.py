import math
import random
from GA_lib import evaluate


def initialize_EMPTY_chromosome(num_vehicles):
    chromosome =[[car_num,[],[]] for car_num in range(num_vehicles)]
    return chromosome

def initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,num_vehicles, DEMANDS, LoadCapacities,maxSpot = 1000):
    chromosome = [[0,[],[]]]
    reqsIndexToInsert = [i for i in range(len(REQUESTS))] # Every requests,HARD Code!!!
    chromosome = insert_requests_into_chromosome(chromosome, reqsIndexToInsert, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot)
    # Trim the empty gene
    # chromosome = [gene for gene in chromosome if (len(gene[1])>0)]
    return chromosome


# This function insert requests into a chromosome
def insert_requests_into_chromosome(chromosome, reqsIndexToInsert, DISTANCES, DURATIONS, timeWindows, REQUESTS,DEMANDS, LoadCapacities,maxSpot):
    reqsIndexToInsert = list(reqsIndexToInsert)
    ## Random things we want to insert.
    random.shuffle(reqsIndexToInsert)
    while(len(reqsIndexToInsert) > 0):
        # reqIndex = reqsIndexToInsert.pop(random.randrange(len(reqsIndexToInsert)))
        inf = 999999999
        minCost = inf
        minIndex = -999999999
        minRoute = []
        reqIndex = reqsIndexToInsert.pop()
        insertingReq = REQUESTS[reqIndex]
        countVehicle = 0
        for (i,gene) in enumerate(chromosome):
            route = gene[2]
            newRoute,newCost = evaluate.new_tour_after_insert_requests(insertingReq, route, DISTANCES, DURATIONS, timeWindows, DEMANDS, LoadCapacities,maxSpot)
            if(len(newRoute) > 0): # Can insert
                if(newCost < minCost):
                    minCost = newCost
                    minIndex = i
                    minRoute = newRoute
        # Can insert
        if(minIndex>=0):
            chromosome[minIndex][1].append(reqIndex)
            chromosome[minIndex][2] = minRoute
        else: # cannot insert, so we allocate a new vehicle
            chromosome.append([len(chromosome),[reqIndex],[REQUESTS[reqIndex][0],REQUESTS[reqIndex][1]]])
            countVehicle += 1
    return chromosome

# This function remove requests from a chromosome
def remove_requests(chromosome, tabooVehicles, reqsToRemove, REQUESTS):
    for [num, reqs, route] in chromosome:
        # Not removing the requests in the 'TABOO' Vehicles
        if (not num in tabooVehicles):
            for removingReq in reqsToRemove:
                if (removingReq in reqs):
                    reqs.remove(removingReq)
                    ## Also, remove the removing requests from the route
                    pickupNode = REQUESTS[removingReq][0]
                    deliveryNode = REQUESTS[removingReq][1]
                    route.remove(pickupNode)
                    route.remove(deliveryNode)