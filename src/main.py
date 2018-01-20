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

# use 'relative path' in filename
#filename = 'pdp_instances/Worse2Worst/trivial01.txt'
filename = 'pdp_instances/LiLim/pdp_100/lrc208.txt'


nodes = preprocessing.load_node(filename)
requests = preprocessing.generate_request(nodes)
distances = processing.create_distance_table(nodes)
couples= GA.requests_to_couples(requests)

clusters = processing.clustering_requests_only_first(requests)
depots=processing.make_depots(nodes)
processing.assign_depot(clusters,depots,nodes)
added_nodes=processing.add_depots_to_nodes(nodes, depots)
#util.draw_requests(requests)
# solving the problems !!!!
couples = GA.requests_to_couples(requests)
p_vehicles = GA.initialize_p_vehicle(couples)
p_node = GA.initialize_p_node(couples, nodes)
p_couples = GA.initialize_p_couples(couples)
p_couples_vehicles = GA.create_p_couples_vehicles(p_couples,p_vehicles)



'''
for i in range(len(p_couples_vehicles)):
    print (p_couples_vehicles[i])
print (len(p_couples_vehicles))
'''