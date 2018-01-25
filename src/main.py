import time
import numpy as np
from GA_lib import GA
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
filename = 'pdp_instances/Worse2Worst/trivial01.txt'
#filename = 'pdp_instances/LiLim/pdptw1000/LR2_10_6.txt'
nodes = preprocessing.load_node(filename)
requests = preprocessing.generate_request(nodes)
distances = processing.create_distance_table(nodes)
clusters = processing.clustering_requests_only_first(requests)
depots=processing.make_depots(nodes)
processing.assign_depot(clusters,depots,nodes)
added_nodes=processing.add_depots_to_nodes(nodes, depots)
#util.draw_requests(requests)

print(" processing time --- %s seconds ---" % (time.time() - start_time))


# solving the problems !!!!
start_time = time.time()

couples = GA.requests_to_couples(requests)

start_time = time.time()
p_vehicles = GA.create_p_vehicles(couples,N=10)
print(" p vehicle time --- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
p_couples = GA.create_p_couples(couples,N=10)
print(" p couple time --- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
p_couples_vehicles = GA.create_p_couples_vehicles(p_couples,p_vehicles)
print(" p couple-vehicle time --- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
p_tours = GA.create_p_tours(p_couples_vehicles, N=10)
print(" p tours time --- %s seconds ---" % (time.time() - start_time))


start_time = time.time()
d = GA.eval_distance(p_tours, distances, depots[0], nodes)
res = min(d)
index_min = np.argmin(d)
depots = [depots[0]]
print("eval time --- %s seconds ---" % (time.time() - start_time))

print (processing.unoptimized_distance(requests,depots))
print (res)
print (p_tours[index_min])
