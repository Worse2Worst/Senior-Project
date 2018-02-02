import time
import numpy as np
from GA_lib import GA_new
from GA_lib import evaluate_new as eval
from GA_lib import oper as op
from pdp_lib import preprocessing
from pdp_lib import processing
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
filename = 'pdp_instances/LiLim/pdp_100/lc103.txt'
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
print(couples)


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

tour = [1,75]
tour = insert_requests_into_tour([7,9],tour,couples,nodes)
tour = insert_requests_into_tour([5,11],tour,couples,nodes)
tour = insert_requests_into_tour([3,8],tour,couples,nodes)
tour = insert_requests_into_tour([10,6],tour,couples,nodes)
tour = insert_requests_into_tour([4,2],tour,couples,nodes)


print (tour)
print('my Solution:'+str(eval.tour_distance(tour,distances)))
tour = [5,3,7,8,10,11,9,6,4,2,1,75]
print (tour)
print(time_violated(tour,nodes,durations))
print(precedence_violated(tour,couples))
print('best solution : '+str(eval.tour_distance(tour,distances)))
print(time_violated(tour,nodes,durations))
print(precedence_violated(tour,couples))
print(" cal time --- %s seconds ---" % (time.time() - start_time))