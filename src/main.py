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
filename = 'pdp_instances/LiLim/pdp_100/lc101.txt'
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

print(filename)
print(" processing time --- %s seconds ---" % (time.time() - start_time))


# solving the problems !!!!
start_time = time.time()


#
# ############### SOLVING THE PROBLEMS !!!!!!!! ######################################

## Initialize the populations
population_size = 100
populations = []
for i in range(population_size):
    chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,numVehicles, DEMANDS, LoadCapacities)
    populations.append(chromosome)
print("Populations creation time --- %s seconds ---" % (time.time()-start_time))
## Crossovers and mutate
start_time = time.time()
# bestFitness =9999999999999999999
# bestFitGen = 0
generations = 1000
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
    if (not evaluate.haveEqualNodes(parent1, parent2, LOCATIONS)):
        print('note have Equal nodes, Elite Bug!!!!!' + str(gen))
        break

    child1,child2 = operation.crossover(DISTANCES, DURATIONS, timeWindows,REQUESTS, parent1, parent2, DEMANDS, LoadCapacities,maxSpot,prob = 1.0)
    if(not evaluate.haveEqualNodes(child1,child2,LOCATIONS)):
        print('note have Equal nodes, Crossover Bug!!!!!'+ str(gen))
        break

    child1 = operation.mutate(child1, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot,prob = 0.7)
    child2 = operation.mutate(child2, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot,prob = 0.7)
    if (not evaluate.haveEqualNodes(child1, child2, LOCATIONS)):
        print('note have Equal nodes, Mutation Bug!!!!!'+ str(gen))
        break

    f = evaluate.chromosomeFitness(child1,DISTANCES)
    f = min(f,evaluate.chromosomeFitness(child2,DISTANCES))
    f = min(f,evaluate.chromosomeFitness(elite1,DISTANCES))
    f = min(f,evaluate.chromosomeFitness(elite2,DISTANCES))
    populations.append(child1)
    populations.append(child2)
    populations.append(elite1)
    populations.append(elite2)
    # if(f<bestFitness):
    #     bestFitness = f
    #     bestFitGen = gen
    # if(bestFitGen-gen >= 3000):
    #     break
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




print ('Chromosome waiting time :'+str(evaluate.chromosomeWatingTime(populations[0],DURATIONS,timeWindows)))