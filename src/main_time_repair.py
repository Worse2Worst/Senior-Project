import time
import numpy as np
from GA_lib import GA_time_repair
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


# maximum distance that a vehicle can travel
MAX_DISTANCE = 1415

start_time = time.time()
# use 'relative path' in filename
#filename = 'pdp_instances/Worse2Worst/dummy01.txt'
filename = 'pdp_instances/LiLim/pdp_600/LC1_6_8.txt'
nodes = preprocessing.load_node(filename)
requests = preprocessing.generate_request(nodes)
distances = processing.create_distance_table(nodes)
durations = processing.create_duration_table(nodes)
clusters = processing.clustering_requests_only_first(requests)
depots=processing.make_depots(nodes)
processing.assign_depot(clusters,depots,nodes)
added_nodes=processing.add_depots_to_nodes(nodes, depots)
#util.draw_requests(requests)

print(" processing time --- %s seconds ---" % (time.time() - start_time))


# solving the problems !!!!
start_time = time.time()

couples = GA_time_repair.requests_to_couples(requests)

start_time = time.time()
p_vehicles = GA_time_repair.create_p_vehicles(couples, N=150)
print(" p vehicle time --- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
p_nodes = GA_time_repair.create_p_nodes(couples, N=150)
print(" p nodes time --- %s seconds ---" % (time.time() - start_time))
start_time = time.time()

# for x in p_vehicles:
#     print(x)

# p_nodes_vehicles = GA_time_repair.create_p_couples_vehicles(p_nodes, p_vehicles)
# print(" p couple-vehicle time --- %s seconds ---" % (time.time() - start_time))
# start_time = time.time()
# p_tours = GA_time_repair.create_p_tours(p_nodes_vehicles, nodes, durations, N=10)
# print(" p tours time --- %s seconds ---" % (time.time() - start_time))
#

# ############################################################################
#

# start_time = time.time()
# d = GA_time_repair.eval_distance(p_tours, distances, durations, depots[0], nodes)
# res = min(d)
# index_min = np.argmin(d)
# depots = [depots[0]]
# print("eval time --- %s seconds ---" % (time.time() - start_time))
#
#
#
# # tour = [5, 7, 8, 10, 9, 6, 2, 4]
# # dist = GA_penalty.tour_distance(tour,distances,durations,depots[0],nodes)
#
# print (processing.unoptimized_distance(requests,depots))
# print (res)
# print (p_tours[index_min])
# # util.draw_requests(requests)
# # util.draw_original_nodes(nodes)
#
# util.draw_tours(p_tours[index_min],nodes,depots[0])