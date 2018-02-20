import random
import itertools
import numpy as np

# To tell whether the precedence (pickup-delivery) is violated, True is violated, False is OK
def precedence_violated(tour,requestType, pickupSiblings):
    visited = []
    for i,_ in enumerate(tour):
        v = tour[i]
        req_type = requestType[v]
        if (req_type == 'delivery'): # v is delivery
            pSibling = pickupSiblings[v]
            if (not pSibling in visited): # the pickupSibling node is not visited
                return True
            else: # the sibling is visited
                visited.append(v)
        else: # v is pickup
            visited.append(v)
    return False

def load_capacities_violated(tour, DEMANDS, LoadCapacities):
    cur_load = 0
    for i,cur_node in enumerate(tour):
        cur_load += DEMANDS[cur_node]
        if(cur_load > LoadCapacities):
            return True
    return False
    # for cur_node in np.nditer(tour):
    #     cur_load += DEMANDS[cur_node]
    #     if (cur_load > LoadCapacities):
    #         return True
    # return False


def time_violated(tour,durations,timeWindows):
    cur_time = 0
    for cur_node, next_node in zip(tour, tour[1:]):
        cur_ET = timeWindows[cur_node][0]
        next_LT = timeWindows[next_node][1]
        cur_time = max(cur_time,cur_ET)
        arrival_time = cur_time+durations[cur_node][next_node]
        if(arrival_time > next_LT):
            return True
    return False



# distance of just one 'job' by one vehicle
def tour_distance(tour, DISTANCES, depot=0):
    if(not tour):
        return 0
    dist = 0
    for cur_node, next_node in zip(tour, tour[1:]):
        dist += DISTANCES[cur_node][next_node]
    dist += DISTANCES[depot][tour[0]] + DISTANCES[tour[-1]][depot]
    return dist



# Calculate a new tour after inserting a request in to an existing tour
# Return empty if cannot insert
def new_tour_after_insert_requests(req, tour, DISTANCES, DURATIONS, timeWindows, DEMANDS, LoadCapacities,maxSpot):
    inf = 9999999999999
    ## Restrict the maximum number of spots to be visited
    # if (len(tour) + 2 > maxSpot):
    #     return ([],inf)

    ## If the tour is empty, insert without thinking.
    if(not tour):
        tour = [req[0],req[1]]
        cost = tour_distance(tour, DISTANCES)
        return ([req[0],req[1]],cost)
    candidate = []
    min_dist = inf
    min_index = -999999
    min_waitTime = inf
    min_cost = inf

    ## Generate all possibilities of insertions
    new_vehicle_dist = tour_distance(req, DISTANCES)
    new_vehicle_waitTime = waitingTime(req, DURATIONS, timeWindows)
    # new_vehicle_cost = new_vehicle_waitTime + 1*new_vehicle_dist
    new_vehicle_cost = new_vehicle_dist
    old_tour_dist =  tour_distance(tour, DISTANCES)
    old_tour_waitTime =  waitingTime(tour, DURATIONS, timeWindows)
    # old_tour_cost = old_tour_waitTime + 1*old_tour_dist
    old_tour_cost = old_tour_dist
    for i in range(len(tour)+1):
        ### Inserting 1
        # temp1 = tour[:i]+[req[0]]+tour[i:]
        temp1 = tour[:]
        temp1[i:i] = [req[0]]

        if (not (load_capacities_violated(temp1, DEMANDS, LoadCapacities)) and not(time_violated(temp1, DURATIONS, timeWindows))):
            for j in range(i+1,len(temp1)+1):
                ### Inserting 2
                # temp2 = temp1[:j] + [req[1]] + temp1[j:]
                temp2 = temp1[:]
                temp2[j:j] = [req[1]]

                # now remove the bad ones
                # Assume that precedence not violated
                # Check if temp2 violate the constraints
                if (not load_capacities_violated(temp2, DEMANDS, LoadCapacities) and not time_violated(temp2, DURATIONS, timeWindows)):
                # if (load_capacities_violated(temp2NP, DEMANDS, LoadCapacities) or time_violated(temp2NP, DURATIONS, timeWindows)):
                    dist = tour_distance(temp2, DISTANCES)
                    waitTime =  waitingTime(temp2, DURATIONS, timeWindows)
                    # cost = waitTime + 1.0*dist
                    cost = dist
                    if(cost < min_cost):
                        min_cost = cost
                        candidate = temp2
    # if no feasible paths!!!, return empty
    if(not candidate):
        return ([],inf)
    # if inserting can reduce cost, then insert
    new_cost = min_cost - old_tour_cost
    if(new_cost < new_vehicle_cost):
        return (candidate,new_cost)
    # else, just don't insert and return empty
    return ([],inf)

def chromosomeRoutesDistance(chromosome, DISTANCES, depot=0):
    total_distances = 0
    for [num, reqs, tour] in chromosome:
        total_distances += tour_distance(tour, DISTANCES)
    return total_distances

def waitingTime(tour,DURATIONS,timeWindows):
    if(not tour):
        return 0
    waitTime = 0
    cur_time = 0
    for cur_node, next_node in zip(tour, tour[1:]):
        cur_ET = timeWindows[cur_node][0]
        next_ET =  timeWindows[next_node][0]
        next_LT = timeWindows[next_node][1]
        cur_time = max(cur_time,cur_ET)
        arrival_time = cur_time+DURATIONS[cur_node][next_node]
        if(arrival_time > next_LT):
            print('Evaluate-Waaiting time - ERRORR - Time Violated!!')
        if (arrival_time < next_ET):
            waitTime += (next_ET - arrival_time)
    # cur_time = timeWindows[tour[0]][0] # first node ET
    # waitTime = 0
    # for i in range(len(tour) - 1):
    #     cur_node = tour[i]
    #     next_node = tour[i + 1]
    #     cur_ET = timeWindows[cur_node][0]
    #     next_ET = timeWindows[next_node][0]
    #     next_LT = timeWindows[next_node][1]
    #     cur_time = max(cur_time, cur_ET)
    #     arrival_time = cur_time + DURATIONS[tour[i]][tour[i + 1]]
    #     if (arrival_time > next_LT):
    #         print ('Evaluate-Waaiting time - ERRORR - Time Violated!!')
    #     if(arrival_time < next_ET):
    #         waitTime += (next_ET - arrival_time)
    return waitTime

def chromosomeWatingTime(chromosome,DURATIONS,timeWindows):
    totalWatingTime = 0
    for num,reqs,route in chromosome:
        totalWatingTime += waitingTime(route,DURATIONS,timeWindows)
    return totalWatingTime


def chromosomeFitness(chromosome,DISTANCES,depot=0):
    return 1.0/chromosomeRoutesDistance(chromosome,DISTANCES,depot)

def haveEqualNodes(parent1,parent2,LOCATIONS):
    allNodes = set([x for x in range(len(LOCATIONS))])
    allNodes -= {0}
    tour1 = set()
    for [_, req, arr] in parent1:
        for x in arr:
            if (x in tour1):
                print('Duplicated-1!!!')
                print(x)
                return False
            tour1.add(x)

    tour2 = set()
    for [_, _, arr] in parent2:
        for x in arr:
            if (x in tour2):
                print('Duplicated-2!!!')
                print(x)
                return False
            tour2.add(x)
    return tour1 == tour2