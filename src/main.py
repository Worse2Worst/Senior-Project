import os
import time
from pdp_lib import preprocessing
from pdp_lib import save_pics
from pdp_lib import util
from pdp_lib import processing
from pdp_lib import GA


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

# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lrc107.txt'


nodes = preprocessing.load_node(filename)
print(len(nodes))
requests = preprocessing.generate_request(nodes)
max_vehicles = len(requests)
distances = processing.create_distance_matrix(nodes)
couples=GA.requests_to_couples(requests)

clusters = processing.clustering_requests_only_first(requests)
depots=processing.make_depots(nodes)
processing.assign_depot(clusters,depots,nodes)
added_nodes=processing.add_depots_to_nodes(nodes, depots)
util.draw_nodes_depots(nodes)

