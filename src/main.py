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

numVehicles, LoadCapacities, speed, data = proc.load_file(filename)
locations = data[0]
DEMANDS = data[1]
timeWindows = data[2]
serviceTimes = data[3]
pickupSiblings = data[4]
deliverySiblings = data[5]
requestType = data[6]
REQUESTS = proc.generate_request(pickupSiblings,deliverySiblings,requestType)
DISTANCES = proc.createDistanceTable(locations)
DURATIONS = proc.createDurationTable(locations, DISTANCES, serviceTimes, speed)

print(requestType[96])

print(" processing time --- %s seconds ---" % (time.time() - start_time))


# solving the problems !!!!
start_time = time.time()

#
#
# maxSpot = 1000
#
#
# start_time = time.time()
# tour = [96,59,92,98,85,91,14,42,2,75,39,23,15,38,44,16,61,99,18,8,84,86,5,6,94,95,97,43,56,4,54,55,25,24,80,12,26,58]
# reqs = [(tour[i],deliverySiblings[tour[i]]) for i in range(len(tour)) if requestType[tour[i]]=='pickup']
# print('The Requests are :'+str(reqs))
# tour = []
# shuffle(reqs)
# for r in reqs:
#     tour = evaluate.new_tour_after_insert_requests(r, tour, DISTANCES, DURATIONS, timeWindows,DEMANDS, LoadCapacities,maxSpot)
# cal_time = time.time() - start_time
#
#
# print (tour)
# print('My Solution is :' + str(tour))
# print('my Solution:' + str(evaluate.tour_distance(tour, DISTANCES)))
# print('Violate time windows:' + str(evaluate.time_violated(tour, DURATIONS, timeWindows)))
# print('Violate time precedence:'+str(evaluate.precedence_violated(tour,requestType, pickupSiblings)))
# print('Violate load capacities:'+str(evaluate.load_capacities_violated(tour,DEMANDS, LoadCapacities)))
#
# best_tour = [96,59,92,98,85,91,14,42,2,75,39,23,15,38,44,16,61,99,18,8,84,86,5,6,94,95,97,43,56,4,54,55,25,24,80,12,26,58]
# print (best_tour)
#
# print('best solution : ' + str(evaluate.tour_distance(best_tour, DISTANCES)))
# print('Violate time windows:' + str(evaluate.time_violated(best_tour, DURATIONS, timeWindows)))
# print('Violate time precedence:'+str(evaluate.precedence_violated(best_tour,requestType, pickupSiblings)))
# print('Violate load capacities:'+str(evaluate.load_capacities_violated(best_tour,DEMANDS, LoadCapacities)))
# print(" cal time --- %s seconds ---" % (cal_time))
# print ('Have equal nodes:'+str(set(tour)==set(best_tour)))
#





#
# ############### SOLVING THE PROBLEMS !!!!!!!! ######################################

## Initialize the populations
population_size = 20
populations = []
for i in range(population_size):
    chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles, DEMANDS, LoadCapacities)
    populations.append(chromosome)
print("Populations creation time --- %s seconds ---" % (time.time()-start_time))

## Crossovers and mutate
start_time = time.time()
generations = 100
fitness = []
maxSpot = 1000
for gen in range(generations):
    fitness=[]
    for chromosome in populations:
        fitness.append(evaluate.chromosomeFitness(chromosome,DISTANCES))
    populations = [x for _,x in sorted(zip(fitness,populations),reverse=True)]
    populations.pop()
    populations.pop()
    elite1 = populations.pop(0)
    elite2 = populations.pop(0)
    # id1,id2 = random.randrange(0,len(populations)),random.randrange(0,len(populations))
    # parent1,parent2 = populations[id1],populations[id2]
    parent1,parent2 = elite1,elite2
    child1,child2 = operation.crossover(DISTANCES, DURATIONS, timeWindows,REQUESTS, parent1, parent2, DEMANDS, LoadCapacities,maxSpot)
    child1 = operation.mutate(child1, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot)
    child2 = operation.mutate(child2, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot)
    populations.append(child1)
    populations.append(child2)
    populations.append(elite1)
    populations.append(elite2)


fitness=[]
for chromosome in populations:
    fitness.append(evaluate.chromosomeFitness(chromosome,DISTANCES))
populations = [x for _,x in sorted(zip(fitness,populations),reverse=True)]
print("GA time --- %s seconds ---" % (time.time()-start_time))




dist = evaluate.chromosomeRoutesDistance(populations[0],DISTANCES)
print('Distances of the best chromosome: '+str(dist))
print (populations[0])
dist = evaluate.chromosomeRoutesDistance(populations[len(populations)-1],DISTANCES)
print('Distances of the worst chromosome: '+str(dist))
print(populations[len(populations)-1])
#
# #################################################################################################
