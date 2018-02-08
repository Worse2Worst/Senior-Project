import random
from GA_lib import evaluate

#############################################################
# This module is used to modify chromosomes.                #
#############################################################

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

# This function insert requests into a chromosome
def insert_requests_into_chromosome(chromosome, reqsIndexToInsert, DISTANCES, DURATIONS, timeWindows, REQUESTS,maxSpot):
    reqsIndexToInsert = list(reqsIndexToInsert)
    ## Random things we want to insert.
    random.shuffle(reqsIndexToInsert)
    maxVehicles = len(chromosome)
    while(len(reqsIndexToInsert) > 0):
        # reqIndex = reqsIndexToInsert.pop(random.randrange(len(reqsIndexToInsert)))
        reqIndex = reqsIndexToInsert.pop()
        insertingReq = REQUESTS[reqIndex]
        countVehicle = 0
        for (i,gene) in enumerate(chromosome):
            route = gene[2]
            newRoute = evaluate.new_tour_after_insert_requests(insertingReq, route, DISTANCES, DURATIONS, timeWindows,maxSpot)
            if(len(newRoute) > 0): # Can insert
                # Insert !!
                chromosome[i][1].append(reqIndex)
                chromosome[i][2] = newRoute
                break
            countVehicle += 1
    return chromosome

