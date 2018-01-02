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
#save_pics.save_all_pics()

# maximum distance that a vehicle can travel
MAX_DISTANCE = 1415
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdptw1000/LRC2_10_10.txt'
#GA2.set_files(filename) # set filename to GA
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

jobs = GA.clusters_to_jobs(clusters)
print (GA.total_distances(jobs,distances))
# GA.swap(job, 2, 9)
# GA.swap(job, 5, 4)
# GA.swap(job, 8, 7)
# GA.swap(job, 2, 7)
# GA.swap(job, 3, 4)
# print (job)
# print(job)
# job[2]=job
# for job in jobs:
#     print (job)
# print('============================================')
# GA.total_distances(jobs,distances)
print(GA.jobs_to_chromosome(jobs,nodes))