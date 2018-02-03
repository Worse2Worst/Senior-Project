import time
import numpy as np
from GA_lib import GA
from GA_lib import evaluate as eval
from GA_lib import oper as op
from pdp_lib import preprocessing
from pdp_lib import processing
from pdp_lib import util

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
#filename = 'pdp_instances/Worse2Worst/dummy01.txt'
filename = 'pdp_instances/LiLim/pdp_100/lc101.txt'
nodes = preprocessing.load_node(filename)
requests = preprocessing.generate_request(nodes)
distances = processing.create_distance_table(nodes)
durations = processing.create_duration_table(nodes,speed=1)
clusters = processing.clustering_requests_only_first(requests)
depots=processing.make_depots(nodes)
processing.assign_depot(clusters,depots,nodes)
added_nodes=processing.add_depots_to_nodes(nodes, depots)
#util.draw_requests(requests)

print(" processing time --- %s seconds ---" % (time.time() - start_time))
couples = GA.requests_to_couples(requests)

tour = [13,17,18,19,15,16,14,12]




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

print(precedence_violated(tour,couples))
print(time_violated(tour,nodes,durations))