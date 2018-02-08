import time
from random import shuffle
from pdp_lib import processing as proc
from pdp_lib import util
from GA_lib import GA
from GA_lib import operation
from GA_lib import evaluate
from GA_lib import modify






start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lc107.txt'

numVehicles, loadCapacities, speed, data = proc.load_file(filename)
LOCATIONS = data[0]
demands = data[1]
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
# chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles)
chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles,maxSpot=10)
# chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles,maxSpot=2)

print (chromosome)
cal_time = time.time() - start_time
print("Chromosome initializing time --- %s seconds ---" % (cal_time))
start_time = time.time()
dist = evaluate.chromosomeRoutesDistance(chromosome,DISTANCES)
print('Tour Distances of chromosome(restricted maxSpot=10): '+str(dist))
print("Distance Calculation time --- %s seconds ---" % (time.time()-start_time))
fitness = evaluate.chromosomeFitness(chromosome,DISTANCES)
print('Tour Fitness of the chromosome: '+str(fitness))
print("Fitness Calculation time --- %s seconds ---" % (time.time()-start_time))

# util.draw_original_nodes(LOCATIONS, REQUESTS)
# util.draw_requests(LOCATIONS, REQUESTS)
# util.draw_tours(chromosome,LOCATIONS)

parent1 = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles,maxSpot=10000)
parent2 = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles,maxSpot=10000)
dist = evaluate.chromosomeRoutesDistance(parent1,DISTANCES)
print('Parent1 Distances of chromosome: '+str(dist))
dist = evaluate.chromosomeRoutesDistance(parent2,DISTANCES)
print('Parent2 Distances of chromosome: '+str(dist))
start_time = time.time()
maxSpot = 10000
child1,child2 = operation.crossover(DISTANCES, DURATIONS, timeWindows,REQUESTS, parent1, parent2,maxSpot)
print("Chromosome crossover time --- %s seconds ---" % (time.time()-start_time))
print (child1)
dist = evaluate.chromosomeRoutesDistance(child1,DISTANCES)
print('Child1 Distances of chromosome: '+str(dist))
print (child2)
dist = evaluate.chromosomeRoutesDistance(child2,DISTANCES)
print('Child2 Distances of chromosome: '+str(dist))
util.draw_tours(child2,DISTANCES)

################### Unoptimized  ############################
unlimitedVehicles=300
chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,unlimitedVehicles,maxSpot=2)
dist = evaluate.chromosomeRoutesDistance(chromosome,DISTANCES)
print('Unoptimized distances is: '+str(dist))
util.draw_tours(chromosome,LOCATIONS)
#######################################################

