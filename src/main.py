import os
import time
from pdp_lib import preprocessing
from pdp_lib import save_pics
from pdp_lib import util
from pdp_lib import processing
from pdp_lib import GA2
'''
filename='pdp_instances/LiLim/pdp_100/lrc207.txt'
nodes = preprocessing.load_node(filename)
util.draw_original_nodes(nodes)
util.print_nodes(nodes)
util.print_requests(requests)
util.draw_requests(requests)

util.print_distances(distances)

'''
#save_pics.save_all_pics()

# maximum distance that a vehicle can travel
MAX_DISTANCE = 1415
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lc101.txt'
#filename = 'pdp_instances/LiLim/pdptw1000/LR2_10_7.txt'
nodes = preprocessing.load_node(filename)
requests = preprocessing.generate_request(nodes)
max_vehicles = len(requests)
distances = processing.create_distance_matrix(nodes)
#util.draw_original_nodes(nodes)

processing.sort_requests(requests)
#util.print_requests(requests)
clusters = processing.clustering_requests_only_first(requests)
# clusters = processing.clustering_requests(requests)
# util.print_clusters(clusters)
# util.draw_requests(requests)
# util.draw_clusters(clusters)
# request_distances=processing.request_distances(requests)
# print (request_distances)
jobs = GA2.clusters_to_jobs(clusters)


