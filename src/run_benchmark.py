import os
import time
from pdp_lib import preprocessing
from pdp_lib import save_pics
from pdp_lib import util
from pdp_lib import processing
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

filename = 'pdp_instances/Worse2Worst/dummy01.txt'
#filename = 'pdp_instances/LiLim/pdptw1000/LR2_10_7.txt'
nodes = preprocessing.load_node(filename)
requests = preprocessing.generate_request(nodes)
distances = processing.create_distance_matrix(nodes)


processing.sort_requests(requests)
util.print_requests(requests)
#util.draw_requests(requests)






'''
max_d=-9999999999999
for i in range(len(distances)):
    for j in range(len(distances)):
        if (distances[i][j]>max_d):
            max_d=distances[i][j]

print (max_d)
'''