import time
import numpy as np
from GA_lib import GA_new
from GA_lib import evaluate_new as eval
from GA_lib import oper as op
from pdp_lib import preprocessing
from pdp_lib import processing
from random import shuffle
from pdp_lib import util
from itertools import permutations
'''
filename='pdp_instances/LiLim/pdp_100/lrc207.txt'
nodes = preprocessing.load_node(filename)
util.draw_original_nodes(nodes)
util.print_nodes(nodes)
util.print_requests(requests)
util.draw_requests(requests)

util.print_distances(distances)

'''


start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lr202.txt'
#filename = 'pdp_instances/LiLim/pdp_100/lc102.txt'
nodes = preprocessing.load_node(filename)
requests = preprocessing.generate_request(nodes)
distances = processing.create_distance_table(nodes)
durations = processing.create_duration_table(nodes,speed=1)
# clusters = processing.clustering_requests_only_first(requests)
# depots=processing.make_depots(nodes)
# processing.assign_depot(clusters,depots,nodes)
# added_nodes=processing.add_depots_to_nodes(nodes, depots)
#util.draw_requests(requests)

print(" processing time --- %s seconds ---" % (time.time() - start_time))


# solving the problems !!!!
start_time = time.time()

couples = GA_new.requests_to_couples(requests)



# util.draw_requests(requests)
# util.draw_original_nodes(nodes)
#
def time_violated(tour,nodes,durations):
    cur_time = 0
    for i in range(len(tour)-1):
        cur_node = nodes[tour[i]]
        next_node = nodes[tour[i+1]]
        cur_ET = cur_node.ET
        next_LT = next_node.LT
        cur_time = max(cur_time,cur_ET)
        arrival_time = cur_time+durations[tour[i]][tour[i+1]]
        if(arrival_time > next_LT):
            return True
    return False
'''
def precedence_violated(tour, couples):
    visited = []
    for i in range(len(tour)):
        v = tour[i]
        couple = [item for item in couples if v in item][0]
        pickup = couple[0] # pickup node
        delivery = couple[1] # delivery node
        if (v == delivery): # v is delivery
            if (not pickup in visited): # the pickup node is not visited
                pickup_index = tour.index(pickup)
                tour.pop(pickup_index)
                tour.insert(i, pickup)
                visited.append(pickup)
                visited.append(v)
                return True
            else: # the sibling is visited
                visited.append(v)
        else: # v is pickup
            visited.append(v)
    return False
'''
'''
def insert_requests_into_tour(req,tour,couples,nodes):
    candidates = []
    # generate all possibilities of insertions
    for i in range(len(tour)+1):
        temp1 = tour[:]
        temp1.insert(i,req[0])
        for j in range(i+1,len(temp1)+1):
            temp2 = temp1[:]
            temp2.insert(j,req[1])
            # now remove the bad ones
            if (precedence_violated(temp2, couples)):
                print ('BUG!!!!!!!')
            if (not time_violated(temp2,nodes,durations)):
                candidates.append(temp2)

    # no feasible paths!!!, return empty
    if(len(candidates) ==0):
        return []
    # select the best candidates
    min_dist = 99999999999999999
    min_index = -999
    for i in range(len(candidates)):
        dist = eval.tour_distance(candidates[i],distances)
        if(dist<min_dist):
            min_dist = dist
            min_index = i
    return candidates[i]

start_time = time.time()
'''


# To tell whether the precedence (pickup-delivery) is violated, True is violated, False is OK
def precedence_violated(tour,nodes):
    visited = []
    for i in range(len(tour)):
        v = tour[i]
        req_type = nodes[v].req_type
        if (req_type == 'd'): # v is delivery
            pickup = nodes[v].p_sib
            if (not pickup in visited): # the pickup node is not visited
                return True
            else: # the sibling is visited
                visited.append(v)
        else: # v is pickup
            visited.append(v)
    return False


def new_tour_after_insert_requests(req,tour,nodes,distances,durations):
    candidates = []
    if(len(tour)==0):
        return [req[0],req[1]]
    # generate all possibilities of insertions
    new_vehicle_dist = eval.tour_distance(req, distances)
    old_tour_dist =  eval.tour_distance(tour,distances)
    for i in range(len(tour)+1):
        temp1 = tour[:]
        temp1.insert(i,req[0])
        for j in range(i+1,len(temp1)+1):
            temp2 = temp1[:]
            temp2.insert(j,req[1])
            # now remove the bad ones
            # Assume that precedence not violated
            if (not time_violated(temp2,nodes,durations)):
                candidates.append(temp2)
    # if no feasible paths!!!, return empty
    if(len(candidates) ==0):
        return []
    # select the best candidates
    min_dist = 99999999999999999
    min_index = -999
    for i in range(len(candidates)):
        dist = eval.tour_distance(candidates[i],distances)
        if(dist<min_dist):
            min_dist = dist
            min_index = i
    # if inserting can reduce cost, then insert
    if(min_dist - old_tour_dist < new_vehicle_dist):
        return candidates[min_index]
    # else, just don't insert and return empty
    return []

tour = [96,59,92,98,85,91,14,42,2,75,39,23,15,38,44,16,61,99,18,8,84,86,5,6,94,95,97,43,56,4,54,55,25,24,80,12,26,58]
pickup = []
for x in tour:
    if(nodes[x].req_type == 'p'):
        pickup.append(x)
req = [(p,nodes[p].d_sib)for p in pickup]
print(req)
tour = []
shuffle(req)
for r in req:
    tour = new_tour_after_insert_requests(r,tour,nodes,distances,durations)



print (tour)

print('my Solution:'+str(eval.tour_distance(tour,distances)))
print('Violate time windows:'+str(time_violated(tour,nodes,durations)))
print('Violate time precedence:'+str(precedence_violated(tour,nodes)))

best_tour = [96,59,92,98,85,91,14,42,2,75,39,23,15,38,44,16,61,99,18,8,84,86,5,6,94,95,97,43,56,4,54,55,25,24,80,12,26,58]
print (best_tour)

print('best solution : '+str(eval.tour_distance(best_tour,distances)))
print('Violate time windows:'+str(time_violated(best_tour,nodes,durations)))
print('Violate time precedence:'+str(precedence_violated(best_tour,nodes)))
print(" cal time --- %s seconds ---" % (time.time() - start_time))
print ('Have equal nodes:'+str(set(tour)==set(best_tour)))
