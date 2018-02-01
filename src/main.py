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
filename = 'pdp_instances/LiLim/pdp_100/lc102.txt'
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
p_tours = GA.create_p_tours(p_couples_vehicles,nodes,durations, N=10)
print(" p tours time --- %s seconds ---" % (time.time() - start_time))


# tour = [5, 7, 9, 4, 6, 2, 8, 10]
# violated = GA.time_violated_nodes(tour,durations,couples,nodes)
# print ('violated  ='+str(violated))
# print('new tour' +str(tour))
############################################################################




best = eval.select_best_populations(p_tours,distances,depots[0],nodes)
depots = [depots[0]]
dist = eval.tours_distance(best[0],distances,depots[0],nodes)
print("eval time --- %s seconds ---" % (time.time() - start_time))

best_lc102 = [[ 20 ,22 ,24 ,25 ,27 ,29 ,28 ,103 ,26 ,23 ,21 ,43 ,41 ,40 ,42 ,44 ,48 ,51 ,50 ,106 ,47 ,46 ,45 ,55 ,57 ,60 ,54 ,53 ,56 ,58 ,59 ,68 ,102 ,90 ,87 ,86 ,83 ,82 ,84 ,85 ,88 ,89 ,91 ,98 ,95 ,100 ,97 ,101 ,96 ,94 ,92 ,93 ,99 ,1 ,75 ,5 ,8 ,9 ,6 ,2 ,4 ,3 ,7 ,10 ,11 ,13 ,12 ,16 ,14 ,17 ,18 ,19 ,15 ,30 ,32 ,33 ,31 ,35 ,37 ,39 ,104 ,38 ,36 ,34 ,52 ,49 ,67 ,65 ,62 ,66 ,61 ,72 ,81 ,78 ,105 ,76 ,71 ,70 ,73 ,77 ,79 ,80 ,74 ,64 ,63 ,69  ]]

print (processing.unoptimized_distance(requests,depots))
couples.sort(key=lambda x: x[0])
print(dist)
util.draw_tours(best[0],nodes,depots[0])
util.draw_tours(best_lc102,nodes,depots[0])







util.draw_requests(requests)
# util.draw_original_nodes(nodes)
#
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
print(eval.tours_distance(best_lc102,distances,depots[0],nodes))
print(precedence_violated(best_lc102[0],couples))