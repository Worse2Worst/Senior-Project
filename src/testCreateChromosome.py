import time
from random import shuffle
from pdp_lib import processing as proc
from pdp_lib import util
from GA_lib import GA
from GA_lib import operation
from GA_lib import evaluate







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

print ('Newly created chromosome below')
chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles, DEMANDS, LoadCapacities)
print (chromosome)

cal_time = time.time() - start_time
print("Chromosome initializing time --- %s seconds ---" % (cal_time))
start_time = time.time()
dist = evaluate.chromosomeRoutesDistance(chromosome,DISTANCES)
print('Tour Distances of chromosome: '+str(dist))

parent1 = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles, DEMANDS, LoadCapacities)
parent2 = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles, DEMANDS, LoadCapacities)


print ('Parents have equal nodes:'+str(evaluate.haveEqualNodes(parent1,parent2,LOCATIONS)))
print('Parent1:'+str(parent1))
print('Parent2:'+str(parent2))




start_time = time.time()
maxSpot = 1000

for i in range(100):
    print('------------------CROSSOVER-----------------')

    child1,child2 = operation.crossover(DISTANCES, DURATIONS, timeWindows,REQUESTS, parent1, parent2, DEMANDS, LoadCapacities,maxSpot,prob=1.0)
    if (not evaluate.haveEqualNodes(child1, child2, LOCATIONS)):
        print('BUGG:' + str(i))
        break
    print('------------------MUTATE-----------------')
    child1 = operation.mutate(child1, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot,prob = 1.0)
    child2 = operation.mutate(child2, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot,prob = 1.0)
    child1 = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles, DEMANDS, LoadCapacities)
    child2 = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles, DEMANDS, LoadCapacities)
    if(not evaluate.haveEqualNodes(child1,child2,LOCATIONS)):
        print('BUGG:' + str(i))
        break

#########################################################################################
# print("Chromosome crossover time --- %s seconds ---" % (time.time()-start_time))
# print (child1)
# dist = evaluate.chromosomeRoutesDistance(child1,DISTANCES)
# print('Child1 Distances of chromosome: '+str(dist))
# print (child2)
# dist = evaluate.chromosomeRoutesDistance(child2,DISTANCES)
# print('Child2 Distances of chromosome: '+str(dist))

print ('Parent1-Parent2 have equal nodes:'+str(evaluate.haveEqualNodes(parent1,parent2,LOCATIONS)))
print ('Child1-Child2 have equal nodes:'+str(evaluate.haveEqualNodes(child1,child2,LOCATIONS)))
print ('Child1-Parent1 have equal nodes:'+str(evaluate.haveEqualNodes(child1,parent1,LOCATIONS)))
print ('Child1-Parent2 have equal nodes:'+str(evaluate.haveEqualNodes(child1,parent2,LOCATIONS)))
print ('Child2-Parent1 have equal nodes:'+str(evaluate.haveEqualNodes(child2,parent1,LOCATIONS)))
print ('Child2-Parent2 have equal nodes:'+str(evaluate.haveEqualNodes(child2,parent2,LOCATIONS)))
print('Child1:'+str(child1))
print('child2:'+str(child2))


