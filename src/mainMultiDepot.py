import time
import random
from pdp_lib import processing as proc
from pdp_lib import util
from GA_lib import GA
from GA_lib import operation
from GA_lib import evaluate_multi_depot as evaluate




def solve_and_print(filename,population_size = 100,generations=2000,crossoverRate=1.0,mutationRate=0.5):
    start_time = time.time()

    numVehicles, LoadCapacities, speed, data = proc.load_file(filename)
    LOCATIONS = data[0]
    DEMANDS = data[1]
    timeWindows = data[2]
    serviceTimes = data[3]
    pickupSiblings = data[4]
    deliverySiblings = data[5]
    requestType = data[6]
    REQUESTS = proc.generate_request(pickupSiblings, deliverySiblings, requestType)
    DISTANCES = proc.createDistanceTable(LOCATIONS)
    DURATIONS = proc.createDurationTable(LOCATIONS, DISTANCES, serviceTimes, speed)
    DEPOTS = proc.create_depots(LOCATIONS)
    DEPOT_DISTANCES = proc.distances_from_depots(DEPOTS, LOCATIONS)
    DEPOT_NUMBERS = proc.simple_assign_depots(LOCATIONS, DEPOTS, DEPOT_DISTANCES)


    print('----------------Instance name: '+str(filename)+'-----------------------------------')
    print(" processing time --- %s seconds ---" % (time.time() - start_time))

    results = []
    ## Loop and memo results

    # ############### SOLVING THE PROBLEMS !!!!!!!! ######################################
    pops_create_time = time.time()
    start_time = time.time()
    print('#################### Round :' +str(round+1)+' ############################')
    ## Initialize the populations
    populations = []
    for i in range(population_size):
        chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows, REQUESTS, numVehicles,
                                                       DEMANDS, LoadCapacities)
        populations.append(chromosome)
    print("Populations creation time --- %s seconds ---" % (time.time() - pops_create_time))
    ## Crossovers and mutate
    GA_time = time.time()
    # bestFitness =9999999999999999999
    # bestFitGen = 0
    fitness = []
    maxSpot = 1000
    for gen in range(generations):
        fitness = []
        for chromosome in populations:
            fitness.append(evaluate.chromosomeFitness(chromosome, DISTANCES))
        populations = [x for _, x in sorted(zip(fitness, populations), reverse=True)]
        ## Remove the 2 worst populations
        populations.pop()
        populations.pop()

        ## Get the 2 best populations
        elite1 = populations.pop(0)
        elite2 = populations.pop(0)

        id1,id2 = random.randrange(0,len(populations)),random.randrange(0,len(populations))
        parent1,parent2 = populations[id1],populations[id2]
        # parent1, parent2 = elite1, elite2
        if (not evaluate.haveEqualNodes(parent1, parent2, LOCATIONS)):
            print('note have Equal nodes, Elite Bug!!!!!' + str(gen))
            break

        child1, child2 = operation.crossover(DISTANCES, DURATIONS, timeWindows, REQUESTS, parent1, parent2, DEMANDS,
                                             LoadCapacities, maxSpot, crossoverRate)
        if (not evaluate.haveEqualNodes(child1, child2, LOCATIONS)):
            print('note have Equal nodes, Crossover Bug!!!!!' + str(gen))
            break

        child1 = operation.mutate(child1, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot,
                                  mutationRate)
        child2 = operation.mutate(child2, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot,
                                  mutationRate)
        if (not evaluate.haveEqualNodes(child1, child2, LOCATIONS)):
            print('note have Equal nodes, Mutation Bug!!!!!' + str(gen))
            break


        populations.append(child1)
        populations.append(child2)
        populations.append(elite1)
        populations.append(elite2)


        # f = evaluate.chromosomeFitness(child1, DISTANCES)
        # f = max(f, evaluate.chromosomeFitness(child2, DISTANCES))
        # f = max(f, evaluate.chromosomeFitness(elite1, DISTANCES))
        # f = max(f, evaluate.chromosomeFitness(elite2, DISTANCES))
        # if(f>bestFitness):
        #     bestFitness = f
        #     bestFitGen = gen
        # if(bestFitGen-gen >= 500):
        #     break
    fitness = []
    for chromosome in populations:
        fitness.append(evaluate.chromosomeFitness(chromosome, DISTANCES))
    populations = [x for _, x in sorted(zip(fitness, populations), reverse=True)]
    print("GA time --- %s seconds ---" % (time.time() - GA_time))
    computationalTime = time.time() - start_time
    print("Computational time --- %s seconds ---" % (time.time() - start_time))

    best_chromosome = populations[0]
    dist = evaluate.chromosomeRoutesDistance(best_chromosome, DISTANCES)
    best_result = [dist,computationalTime,str(best_chromosome)]
    print('Distances of the best chromosome: ' + str(dist))
    print(best_chromosome)
    results.append(best_result)
    return results


######################### MAIN ########################################################
start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lc101.txt'
# filename = 'pdp_instances/LiLim/pdp_200/LR1_2_9.txt'
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
DEPOTS = proc.create_depots(LOCATIONS)
DEPOT_DISTANCES = proc.distances_from_depots(DEPOTS,LOCATIONS)
DEPOT_NUMBERS = proc.simple_assign_depots(REQUESTS,LOCATIONS,DEPOTS,DEPOT_DISTANCES)
print(filename)
print(" processing time --- %s seconds ---" % (time.time() - start_time))
print(DEPOT_NUMBERS)
util.draw_simple_assigned_depots(REQUESTS,LOCATIONS, DEPOTS, DEPOT_NUMBERS)



# solving the problems !!!!
start_time = time.time()

# util.draw_original_nodes(LOCATIONS,REQUESTS)
# util.draw_nodes_with_added_depots(LOCATIONS,REQUESTS,DEPOTS)

'''
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
GA_time = time.time()
best_fitness_so_far = -999999
bestFitGen = 0
generations = 3000
fitness_table = []
maxSpot = 1000
for gen in range(generations):
    fitness_table=[]
    for chromosome in populations:
        fitness_table.append(evaluate.chromosomeFitness(chromosome, DISTANCES))
    populations = [x for _,x in sorted(zip(fitness_table, populations), reverse=True)]
    populations.pop()
    populations.pop()
    elite1 = populations.pop(0)
    elite2 = populations.pop(0)

    id1,id2 = random.randrange(0,len(populations)),random.randrange(0,len(populations))
    parent1,parent2 = populations[id1],populations[id2]
    # parent1,parent2 = elite1,elite2
    if (not evaluate.haveEqualNodes(parent1, parent2, LOCATIONS)):
        print('note have Equal nodes, Elite Bug!!!!!' + str(gen))
        break

    child1,child2 = operation.crossover(DISTANCES, DURATIONS, timeWindows,REQUESTS, parent1, parent2, DEMANDS, LoadCapacities,maxSpot,prob = 1.0)
    if(not evaluate.haveEqualNodes(child1,child2,LOCATIONS)):
        print('note have Equal nodes, Crossover Bug!!!!!'+ str(gen))
        break

    child1 = operation.mutate(child1, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot,prob = 0.5)
    child2 = operation.mutate(child2, DISTANCES, DURATIONS, timeWindows, REQUESTS, DEMANDS, LoadCapacities, maxSpot,prob = 0.5)
    if (not evaluate.haveEqualNodes(child1, child2, LOCATIONS)):
        print('note have Equal nodes, Mutation Bug!!!!!'+ str(gen))
        break

    current_fitness = evaluate.chromosomeFitness(child1, DISTANCES)
    current_fitness = max(current_fitness, evaluate.chromosomeFitness(child2, DISTANCES))
    current_fitness = max(current_fitness, evaluate.chromosomeFitness(elite1, DISTANCES))
    current_fitness = max(current_fitness, evaluate.chromosomeFitness(elite2, DISTANCES))
    populations.append(child1)
    populations.append(child2)
    populations.append(elite1)
    populations.append(elite2)
    if(current_fitness>best_fitness_so_far):
        best_fitness_so_far = current_fitness
        bestFitGen = gen
        print('#### New Best Fitness !! , Best so far is :' + str(10000.0/best_fitness_so_far)+'#####')
        print('#### This Generation: ' + str(gen) + '#######')
    if(gen - bestFitGen >= 500):
        print('#### Break Generation: ' + str(gen) + '#######')
        break
    # print('############# Generation:' +str(gen+1)+' #########################')
    # print('############# BestFitGen:' +str(bestFitGen)+' #########################')
    # print('This Gen Fitness :'+str(10000.0 / current_fitness))

fitness_table=[]
for chromosome in populations:
    fitness_table.append(evaluate.chromosomeFitness(chromosome, DISTANCES))
populations = [x for _,x in sorted(zip(fitness_table, populations), reverse=True)]
print("GA time --- %s seconds ---" % (time.time()- GA_time))
print("Total Calculation time --- %s seconds ---" % (time.time()- start_time))




dist = evaluate.chromosomeRoutesDistance(populations[0],DISTANCES)
print('Distances of the best chromosome: '+str(dist))
print (populations[0])
dist = evaluate.chromosomeRoutesDistance(populations[len(populations)-1],DISTANCES)
print('Distances of the worst chromosome: '+str(dist))
print(populations[len(populations)-1])
#
# #################################################################################################


print(filename)
'''

