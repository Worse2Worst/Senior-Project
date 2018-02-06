import random


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
def tour_distance(tour,distances,depot=0):
    dist = 0
    for i in range(len(tour)-1):
        dist += distances[tour[i]][tour[i+1]]
    dist += distances[depot][tour[0]]+distances[tour[-1]][depot]
    return dist



# Calculate a new tour after inserting a request in to an existing tour
# Return empty if cannot insert
def new_tour_after_insert_requests(req, tour, DISTANCES, DURATIONS, timeWindows):
    if(len(tour)==0):
        return [req[0],req[1]]
    candidate = []
    min_dist = 99999999999999999
    min_index = -999999
    # generate all possibilities of insertions
    new_vehicle_dist = tour_distance(req, DISTANCES)
    old_tour_dist =  tour_distance(tour, DISTANCES)
    for i in range(len(tour)+1):
        temp1 = tour[:] # copy tour
        temp1 = temp1[:i]+[req[0]]+temp1[i:] # Insert
        if(time_violated(temp1, DURATIONS, timeWindows)):
            pass
        for j in range(i+1,len(temp1)+1):
            temp2 = temp1[:]
            temp2 = temp2[:j] + [req[1]] + temp2[j:]
            # now remove the bad ones
            # Assume that precedence not violated
            # Check if temp2 violate the time-window constraints
            if (not time_violated(temp2, DURATIONS, timeWindows)):
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


