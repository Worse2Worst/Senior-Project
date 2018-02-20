import time
from random import shuffle
from pdp_lib import processing as proc
from pdp_lib import util
from GA_lib import GA
from GA_lib import operation
from GA_lib import evaluate
import random






start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lc107.txt'
# filename = 'pdp_instances/Worse2Worst/dummy01.txt'


numVehicles, LoadCapacities, speed, data = proc.load_file(filename)
LOCATIONS = data[0]
DEMANDS = data[1]
timeWindows = data[2]
serviceTimes = data[3]
pickupSiblings = data[4]
deliverySiblings = data[5]
requestType = data[6]
REQUESTS = proc.generate_request(pickupSiblings,deliverySiblings,requestType)
DISTANCES = proc.createDistanceTable(LOCATIONS)
DURATIONS = proc.createDurationTable(LOCATIONS, DISTANCES, serviceTimes, speed)


print(" processing time --- %s seconds ---" % (time.time() - start_time))


# Solving the problems !!!!
start_time = time.time()


############################### INSERTION!!!!!!!! #######################################################
allReqs = [*REQUESTS]
random.shuffle(allReqs)

parent1 = [[0, [10, 0, 12, 3, 20, 7, 16, 14, 8, 6, 15, 17, 18, 19], [20, 24, 25, 13, 17, 18, 33, 32, 31, 27, 29, 35, 37, 38, 39, 101, 30, 28, 16, 14, 12, 36, 34, 6, 4, 1, 75, 21]], [1, [34, 21, 47, 24, 28, 22, 35, 29, 33, 27, 30, 32, 31, 26, 25, 37, 23], [43, 42, 67, 65, 63, 90, 83, 62, 41, 40, 54, 55, 57, 53, 56, 58, 44, 60, 72, 61, 103, 45, 46, 48, 50, 51, 59, 68, 69, 66, 47, 105, 49, 52]], [2, [48, 46, 41, 43, 13, 45, 49, 39, 11, 50, 40, 51, 44, 36, 42, 52], [98, 96, 95, 87, 86, 81, 104, 78, 76, 70, 71, 82, 94, 92, 93, 97, 85, 84, 73, 79, 77, 80, 88, 89, 99, 100, 106, 23, 102, 26, 22, 91]], [3, [5, 4, 2, 1, 9], [5, 3, 7, 8, 10, 19, 15, 11, 9, 2]], [4, [38], [74, 64]]]
parent2 = [[0, [19, 14, 25, 8, 20, 15, 10, 27, 26, 12, 16, 18, 23, 21, 17, 22, 24], [41, 42, 43, 20, 24, 25, 17, 18, 32, 33, 35, 31, 44, 40, 27, 29, 30, 28, 46, 45, 38, 37, 39, 101, 36, 34, 51, 48, 52, 50, 49, 47, 105, 21]], [1, [3, 41, 34, 36, 43, 37, 44, 28, 42, 30, 38, 29, 33, 35, 40, 39, 11], [67, 65, 63, 55, 57, 54, 81, 104, 78, 76, 71, 70, 53, 56, 62, 74, 72, 60, 77, 73, 84, 85, 89, 79, 80, 64, 23, 102, 6, 4, 91, 66, 68, 69]], [2, [2, 6, 1, 5, 9, 0, 4, 7], [5, 3, 7, 13, 10, 8, 19, 15, 16, 14, 11, 12, 9, 2, 1, 75]], [3, [46, 31, 48, 49, 50, 13, 47, 51, 32, 52, 45], [90, 87, 86, 98, 96, 95, 94, 92, 82, 83, 93, 61, 103, 58, 59, 88, 97, 100, 106, 99, 26, 22]]]

# GA.remove_requests(parent2, [], allReqs, REQUESTS)
# child1,child2 = operation.crossover(DISTANCES, DURATIONS, timeWindows,REQUESTS, parent1, parent2, DEMANDS, LoadCapacities,maxSpot=10000,prob=1.0)

child1 = operation.mutate(parent2, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot=1000,prob = 1.0)
# child1 = operation.mutate(parent1, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot=1000,prob = 1.0)
print(parent2)
print(child1)
print ('Parent1-Parent2 have equal nodes:'+str(evaluate.haveEqualNodes(parent1,parent2,LOCATIONS)))
print ('Child1-Parent1 have equal nodes:'+str(evaluate.haveEqualNodes(child1,parent1,LOCATIONS)))

#########################################################################################
# print("Chromosome crossover time --- %s seconds ---" % (time.time()-start_time))
# print (child1)
# dist = evaluate.chromosomeRoutesDistance(child1,DISTANCES)
# print('Child1 Distances of chromosome: '+str(dist))
# print (child2)
# dist = evaluate.chromosomeRoutesDistance(child2,DISTANCES)
# print('Child2 Distances of chromosome: '+str(dist))

# print ('Parent1-Parent2 have equal nodes:'+str(evaluate.haveEqualNodes(parent1,parent2,LOCATIONS)))
# print ('Child1-Child2 have equal nodes:'+str(evaluate.haveEqualNodes(child1,child2,LOCATIONS)))
# print ('Child1-Parent1 have equal nodes:'+str(evaluate.haveEqualNodes(child1,parent1,LOCATIONS)))
# print ('Child1-Parent2 have equal nodes:'+str(evaluate.haveEqualNodes(child1,parent2,LOCATIONS)))
# print ('Child2-Parent1 have equal nodes:'+str(evaluate.haveEqualNodes(child2,parent1,LOCATIONS)))
# print ('Child2-Parent2 have equal nodes:'+str(evaluate.haveEqualNodes(child2,parent2,LOCATIONS)))
# print('Child1:'+str(child1))
# print('child2:'+str(child2))


