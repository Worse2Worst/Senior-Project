import time
from random import shuffle
from pdp_lib import processing as proc
from GA_lib import GA
from GA_lib import operation as op
from GA_lib import evaluate as eval






start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lr202.txt'

numVehicles, loadCapacities, speed, data = proc.load_file(filename)
locations = data[0]
demands = data[1]
timeWindows = data[2]
serviceTimes = data[3]
pickupSiblings = data[4]
deliverySiblings = data[5]
requestType = data[6]
requests = proc.generate_request(pickupSiblings,deliverySiblings,requestType)
distances = proc.createDistanceTable(locations)
durations = proc.createDurationTable(locations,distances,serviceTimes,speed)

print(requestType[96])

print(" processing time --- %s seconds ---" % (time.time() - start_time))


# solving the problems !!!!
start_time = time.time()




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


def new_tour_after_insert_requests(req,tour,distances,durations,timeWindows):
    if(len(tour)==0):
        return [req[0],req[1]]
    candidate = []
    min_dist = 99999999999999999
    min_index = -999
    # generate all possibilities of insertions
    new_vehicle_dist = eval.tour_distance(req, distances)
    old_tour_dist =  eval.tour_distance(tour,distances)
    for i in range(len(tour)+1):
        temp1 = tour[:] # copy tour
        temp1.insert(i,req[0])
        if(time_violated(temp1, durations,timeWindows)):
            pass
        for j in range(i+1,len(temp1)+1):
            temp2 = temp1[:]
            temp2.insert(j,req[1])
            # now remove the bad ones
            # Assume that precedence not violated
            # Check if temp2 violate the time-window constraints
            if (not time_violated(temp2,durations,timeWindows)):
                dist = eval.tour_distance(temp2,distances)
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



start_time = time.time()
tour = [96,59,92,98,85,91,14,42,2,75,39,23,15,38,44,16,61,99,18,8,84,86,5,6,94,95,97,43,56,4,54,55,25,24,80,12,26,58]
reqs = [(tour[i],deliverySiblings[tour[i]]) for i in range(len(tour)) if requestType[tour[i]]=='pickup']
print('The Requests are :'+str(reqs))
tour = []
shuffle(reqs)
for r in reqs:
    tour = new_tour_after_insert_requests(r,tour,distances,durations,timeWindows)
cal_time = time.time() - start_time


print (tour)

print('my Solution:'+str(eval.tour_distance(tour,distances)))
print('Violate time windows:'+str(time_violated(tour,durations,timeWindows)))
print('Violate time precedence:'+str(precedence_violated(tour,requestType, pickupSiblings)))

best_tour = [96,59,92,98,85,91,14,42,2,75,39,23,15,38,44,16,61,99,18,8,84,86,5,6,94,95,97,43,56,4,54,55,25,24,80,12,26,58]
print (best_tour)

print('best solution : '+str(eval.tour_distance(best_tour,distances)))
print('Violate time windows:'+str(time_violated(best_tour,durations,timeWindows)))
print('Violate time precedence:'+str(precedence_violated(tour,requestType, pickupSiblings)))
print(" cal time --- %s seconds ---" % (cal_time))
print ('Have equal nodes:'+str(set(tour)==set(best_tour)))
