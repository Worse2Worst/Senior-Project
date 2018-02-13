import random
import itertools

# To tell whether the precedence (pickup-delivery) is violated, True is violated, False is OK
def precedence_violated(tour,requestType, pickupSiblings):
    visited = []
    for i in range(len(tour)):
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
    for i in range(len(tour)):
        cur_node = tour[i]
        cur_load += DEMANDS[cur_node]
        if(cur_load > LoadCapacities):
            return True
    return False


def time_violated(tour,durations,timeWindows):
    cur_time = 0
    for i in range(len(tour)-1):
        cur_node = tour[i]
        next_node = tour[i+1]
        cur_ET = timeWindows[cur_node][0]
        next_LT = timeWindows[next_node][1]
        cur_time = max(cur_time,cur_ET)
        arrival_time = cur_time+durations[tour[i]][tour[i+1]]
        if(arrival_time > next_LT):
            return True
    return False



# distance of just one 'job' by one vehicle
def tour_distance(tour, DISTANCES, depot=0):
    if(len(tour) == 0):
        return 0
    dist = 0
    for i in range(len(tour)-1):
        dist += DISTANCES[tour[i]][tour[i + 1]]
    dist += DISTANCES[depot][tour[0]] + DISTANCES[tour[-1]][depot]
    return dist



# Calculate a new tour after inserting a request in to an existing tour
# Return empty if cannot insert
def new_tour_after_insert_requests(req, tour, DISTANCES, DURATIONS, timeWindows, DEMANDS, LoadCapacities,maxSpot):
    ## Restrict the maximum number of spots to be visited
    if (len(tour) + 2 > maxSpot):
        return []
    ## If the tour is empty, insert without thinking.
    if(len(tour)==0):
        return [req[0],req[1]]
    candidate = []
    min_dist = 99999999999999999
    min_index = -999999
    # generate all possibilities of insertions
    new_vehicle_dist = tour_distance(req, DISTANCES)
    old_tour_dist =  tour_distance(tour, DISTANCES)
    for i in range(len(tour)+1):
        # Inserting 1
        temp1 = tour[:i]+[req[0]]+tour[i:]
        if (load_capacities_violated(temp1, DEMANDS, LoadCapacities)):
            pass
        if(time_violated(temp1, DURATIONS, timeWindows)):
            pass
        for j in range(i+1,len(temp1)+1):
            # Inserting 2
            temp2 = temp1[:j] + [req[1]] + temp1[j:]
            # now remove the bad ones
            # Assume that precedence not violated
            # Check if temp2 violate the time-window constraints
            if (load_capacities_violated(temp2, DEMANDS, LoadCapacities)):
                pass
            if (not time_violated(temp2, DURATIONS, timeWindows)):
                # return temp2
                dist = tour_distance(temp2, DISTANCES)
                if(dist<min_dist):
                    min_dist = dist
                    candidate = temp2
    # if no feasible paths!!!, return empty
    if(len(candidate) == 0):
        return []
    # if inserting can reduce cost, then insert
    if(min_dist - old_tour_dist < new_vehicle_dist):
        return candidate
    # else, just don't insert and return empty
    return []

def chromosomeRoutesDistance(chromosome, DISTANCES, depot=0):
    total_distances = 0
    for [num, reqs, tour] in chromosome:
        total_distances += tour_distance(tour, DISTANCES)
    return total_distances

def waitingTime(tour,DURATIONS,timeWindows):
    if(len(tour)<=0):
        return 0
    cur_time = timeWindows[tour[0]][0] # first node ET
    waitTime = 0
    for i in range(len(tour) - 1):
        cur_node = tour[i]
        next_node = tour[i + 1]
        cur_ET = timeWindows[cur_node][0]
        next_ET = timeWindows[next_node][0]
        next_LT = timeWindows[next_node][1]
        cur_time = max(cur_time, cur_ET)
        arrival_time = cur_time + DURATIONS[tour[i]][tour[i + 1]]
        if (arrival_time > next_LT):
            print ('ERRORR - Time Violated!!')
        waitTime += (next_ET - arrival_time)
    return waitTime

def chromosomeWatingTime(chromosome,DURATIONS,timeWindows):
    totalWatingTime = 0
    for num,reqs,route in chromosome:
        totalWatingTime += waitingTime(route,DURATIONS,timeWindows)
    return totalWatingTime


def chromosomeFitness(chromosome,DISTANCES,depot=0):
    return 1.0/chromosomeRoutesDistance(chromosome,DISTANCES,depot)

