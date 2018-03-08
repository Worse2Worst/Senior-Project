import time
import random
import numpy as np
from itertools import chain
from pdp_lib import processing as proc
from pdp_lib import util
from GA_lib import GA_multi_depot as GA
from GA_lib import operation_multi_depot as operation
from GA_lib import evaluate_multi_depot as evaluate




def solve_and_print(filename,rounds = 1,population_size = 100,generations=2000,crossoverRate=1.0,mutationRate=0.5):
    process_time = time.time()
    numVehicles, LoadCapacities, speed, data = proc.load_file(filename)
    LOCATIONS = data[0]
    DEMANDS = data[1]
    timeWindows = data[2]
    serviceTimes = data[3]
    pickupSiblings = data[4]
    deliverySiblings = data[5]
    requestType = data[6]
    REQS_TO_SOLVE = proc.generate_request(pickupSiblings, deliverySiblings, requestType)
    DISTANCES = proc.createDistanceTable(LOCATIONS)
    DURATIONS = proc.createDurationTable(LOCATIONS, DISTANCES, serviceTimes, speed)
    DEPOTS = proc.create_depots(LOCATIONS)
    DISTANCES_FROM_DEPOTS = proc.distances_from_depots(DEPOTS, LOCATIONS)
    DISTANCES_TO_DEPOTS = proc.distances_to_depots(DEPOTS, LOCATIONS)
    DEPOT_NUMBERS = proc.simple_assign_depots(REQUESTS, LOCATIONS, DEPOTS, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS)
    REQ_BY_DEPOTS = proc.requests_by_depots(DEPOTS, REQUESTS, DEPOT_NUMBERS)

    print('----------------Instance name: '+str(filename)+'-----------------------------------')
    print(" processing time --- %s seconds ---" % (time.time() - process_time))

    all_time = time.time()

    for round in range(rounds):
        solved_by_depots = []
        for id_depot in range(len(DEPOTS)):
            THIS_DEP_REQS = REQ_BY_DEPOTS[id_depot]
            NODES_OF_THIS_DEPOT = proc.locations_of_this_depot(id_depot, REQ_BY_DEPOTS, LOCATIONS)
            # ############### SOLVING THE PROBLEMS !!!!!!!! ######################################
            pops_create_time = time.time()
            start_time = time.time()
            print('#################### Round :' +str(round+1)+' ############################')
            ## Initialize the populations
            populations = []
            for _ in range(population_size):
                chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, id_depot, DURATIONS, timeWindows, THIS_DEP_REQS, DEMANDS, LoadCapacities)
                populations.append(chromosome)
            print("Populations creation time --- %s seconds ---" % (time.time() - pops_create_time))
            ## Crossovers and mutate
            GA_time = time.time()
            # bestFitGen = 0
            fitness = []

            best_fitness_so_far = -99999999
            for gen in range(generations):
                fitness_table = []
                for chromosome in populations:
                    fitness_table.append(
                        evaluate.chromosomeFitness(chromosome, DISTANCES, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS,
                                                   id_depot))
                populations = [x for _, x in sorted(zip(fitness_table, populations), reverse=True)]
                populations.pop()
                populations.pop()
                elite1 = populations.pop(0)
                elite2 = populations.pop(0)

                id1, id2 = random.randrange(0, len(populations)), random.randrange(0, len(populations))
                parent1, parent2 = populations[id1], populations[id2]
                # parent1,parent2 = elite1,elite2

                child1, child2 = operation.crossover(DISTANCES, DURATIONS, timeWindows, THIS_DEP_REQS, parent1, parent2,
                                                     DEMANDS, LoadCapacities, DISTANCES_FROM_DEPOTS,
                                                     DISTANCES_TO_DEPOTS, id_depot, crossoverRate)
                # if(not evaluate.haveEqualNodes(child1,child2,LOCATIONS)):
                #         print('note have Equal nodes, Crossover Bug!!!!!'+ str(gen))
                #         break
                #
                child1 = operation.mutate(child1, DISTANCES, DURATIONS, timeWindows, THIS_DEP_REQS, DEMANDS,
                                          LoadCapacities, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, id_depot, mutationRate)
                child2 = operation.mutate(child2, DISTANCES, DURATIONS, timeWindows, THIS_DEP_REQS, DEMANDS,
                                          LoadCapacities, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, id_depot, mutationRate)
                if (not evaluate.haveEqualNodes(child1, child2, NODES_OF_THIS_DEPOT)):
                    print('note have Equal nodes, Mutation Bug!!!!!' + str(gen))
                    break

                current_fitness = evaluate.chromosomeFitness(child1, DISTANCES, DISTANCES_FROM_DEPOTS,
                                                             DISTANCES_TO_DEPOTS, id_depot)
                current_fitness = max(current_fitness,
                                      evaluate.chromosomeFitness(child2, DISTANCES, DISTANCES_FROM_DEPOTS,
                                                                 DISTANCES_TO_DEPOTS, id_depot))
                current_fitness = max(current_fitness,
                                      evaluate.chromosomeFitness(elite1, DISTANCES, DISTANCES_FROM_DEPOTS,
                                                                 DISTANCES_TO_DEPOTS, id_depot))
                current_fitness = max(current_fitness,
                                      evaluate.chromosomeFitness(elite2, DISTANCES, DISTANCES_FROM_DEPOTS,
                                                                 DISTANCES_TO_DEPOTS, id_depot))
                populations.append(child1)
                populations.append(child2)
                populations.append(elite1)
                populations.append(elite2)
                if (current_fitness > best_fitness_so_far):
                    best_fitness_so_far = current_fitness
                    bestFitGen = gen
                    print('#### New Best Fitness !! , Best so far is :' + str(10000.0 / best_fitness_so_far) + '#####')
                    print('#### This Generation: ' + str(gen) + '#######')
                if (gen - bestFitGen >= 500):
                    print('#### Break Generation: ' + str(gen) + '#######')
                    break
                print('############# DEPOT-'+str(id_depot)+','+ 'Generation:' + str(gen + 1) + ' #########################')
                #### print('############# BestFitGen:' +str(bestFitGen)+' #########################')
                print('This Gen Distance :' + str(10000.0 / current_fitness))

            fitness_table = []
            for chromosome in populations:
                fitness_table.append(
                    evaluate.chromosomeFitness(chromosome, DISTANCES, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, id_depot))
            populations = [x for _, x in sorted(zip(fitness_table, populations), reverse=True)]
            print("GA time --- %s seconds ---" % (time.time() - GA_time))
            print("Total Calculation time --- %s seconds ---" % (time.time() - start_time))

            dist = evaluate.chromosomeRoutesDistance(populations[0],DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,id_depot)
            print('Distances of the best chromosome: ' + str(dist))
            print(populations[0])

    return solved_by_depots


######################### MAIN ########################################################
start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_400/LRC2_4_6.txt'
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
DISTANCES_FROM_DEPOTS = proc.distances_from_depots(DEPOTS,LOCATIONS)
DISTANCES_TO_DEPOTS = proc.distances_to_depots(DEPOTS, LOCATIONS)
DEPOT_NUMBERS = proc.simple_assign_depots(REQUESTS, LOCATIONS, DEPOTS,DISTANCES_FROM_DEPOTS ,DISTANCES_TO_DEPOTS)
REQ_BY_DEPOTS = proc.requests_by_depots(DEPOTS,REQUESTS,DEPOT_NUMBERS)


print(filename)
print(" processing time --- %s seconds ---" % (time.time() - start_time))
solved_by_depots = solve_and_print(filename)
print(solved_by_depots)
# solving the problems !!!!
start_time = time.time()

# util.draw_original_nodes(LOCATIONS,REQUESTS)
# util.draw_nodes_with_added_depots(LOCATIONS,REQUESTS,DEPOTS)
# util.draw_simple_assigned_depots(REQUESTS,LOCATIONS, DEPOTS, DEPOT_NUMBERS)


################# SOLVING THE PROBLEMS !!!!!!!! ######################################

## Initialize the populations
# population_size = 100
# populations = []
#
# dep = 4
# THIS_DEP_REQS = REQ_BY_DEPOTS[dep]
#
# LOCATIONS_OF_THIS_DEPOT = proc.locations_of_this_depot(dep, REQ_BY_DEPOTS, LOCATIONS)
#
#
# for i in range(population_size):
#     chromosome = GA.initialize_Feasible_chromosome(DISTANCES, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, dep, DURATIONS, timeWindows, THIS_DEP_REQS, DEMANDS, LoadCapacities)
#     populations.append(chromosome)
# print("Populations creation time --- %s seconds ---" % (time.time()-start_time))
# print(populations[0])
#
# parent1 = populations[0]
# parent2 = populations[1]
# child1,child2 = operation.crossover(DISTANCES, DURATIONS, timeWindows, THIS_DEP_REQS, parent1, parent2, DEMANDS, LoadCapacities, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, dep)
# child1 = operation.mutate(child1, DISTANCES, DURATIONS, timeWindows, THIS_DEP_REQS, DEMANDS, LoadCapacities, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, dep, 1.0)
# child2 = operation.mutate(child2, DISTANCES, DURATIONS, timeWindows, THIS_DEP_REQS, DEMANDS, LoadCapacities, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, dep, 1.0)
# print(THIS_DEP_REQS)
#
# if (not evaluate.haveEqualNodes(child1, child2, LOCATIONS_OF_THIS_DEPOT)):
#         print('note have Equal nodes, Mutation Bug!!!!!')
# else:
#     print('CX + MUTATE COMPLETE!!!')
# print(child1)
# print(child2)
# dist = evaluate.chromosomeRoutesDistance(child1,DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,dep)
# print(dist)
# print(evaluate.chromosomeFitness(child1, DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,dep))
#
# ## Crossovers and mutate
# GA_time = time.time()
# best_fitness_so_far = -999999
# bestFitGen = 0
# generations = 3000
# fitness_table = []
#
# for gen in range(generations):
#     fitness_table=[]
#     for chromosome in populations:
#         fitness_table.append(evaluate.chromosomeFitness(chromosome, DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,dep))
#     populations = [x for _,x in sorted(zip(fitness_table, populations), reverse=True)]
#     populations.pop()
#     populations.pop()
#     elite1 = populations.pop(0)
#     elite2 = populations.pop(0)
#
#     id1,id2 = random.randrange(0,len(populations)),random.randrange(0,len(populations))
#     parent1,parent2 = populations[id1],populations[id2]
#     # parent1,parent2 = elite1,elite2
#     if (not evaluate.haveEqualNodes(child1, child2, LOCATIONS_OF_THIS_DEPOT)):
#         print('note have Equal nodes, Elite Bug!!!!!' + str(gen))
#         break
#
#     child1,child2 = operation.crossover(DISTANCES, DURATIONS, timeWindows, THIS_DEP_REQS, parent1, parent2, DEMANDS, LoadCapacities, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, dep,1.0)
#     # if(not evaluate.haveEqualNodes(child1,child2,LOCATIONS)):
# #         print('note have Equal nodes, Crossover Bug!!!!!'+ str(gen))
# #         break
# #
#     child1 = operation.mutate(child1, DISTANCES, DURATIONS, timeWindows, THIS_DEP_REQS, DEMANDS, LoadCapacities, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, dep, 1.0)
#     child2 =operation.mutate(child2, DISTANCES, DURATIONS, timeWindows, THIS_DEP_REQS, DEMANDS, LoadCapacities, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, dep, 1.0)
#     if (not evaluate.haveEqualNodes(child1, child2, LOCATIONS_OF_THIS_DEPOT)):
#         print('note have Equal nodes, Mutation Bug!!!!!'+ str(gen))
#         break
#
#     current_fitness = evaluate.chromosomeFitness(child1, DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,dep)
#     current_fitness = max(current_fitness, evaluate.chromosomeFitness(child2, DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,dep))
#     current_fitness = max(current_fitness, evaluate.chromosomeFitness(elite1, DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,dep))
#     current_fitness = max(current_fitness, evaluate.chromosomeFitness(elite2, DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,dep))
#     populations.append(child1)
#     populations.append(child2)
#     populations.append(elite1)
#     populations.append(elite2)
#     if(current_fitness>best_fitness_so_far):
#         best_fitness_so_far = current_fitness
#         bestFitGen = gen
#         print('#### New Best Fitness !! , Best so far is :' + str(10000.0/best_fitness_so_far)+'#####')
#         print('#### This Generation: ' + str(gen) + '#######')
#     if(gen - bestFitGen >= 500):
#         print('#### Break Generation: ' + str(gen) + '#######')
#         break
#     print('############# Generation:' +str(gen+1)+' #########################')
#     #### print('############# BestFitGen:' +str(bestFitGen)+' #########################')
#     print('This Gen Distance :'+str(10000.0 / current_fitness))
#
# fitness_table=[]
# for chromosome in populations:
#     fitness_table.append(evaluate.chromosomeFitness(chromosome, DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,dep))
# populations = [x for _,x in sorted(zip(fitness_table, populations), reverse=True)]
# print("GA time --- %s seconds ---" % (time.time()- GA_time))
# print("Total Calculation time --- %s seconds ---" % (time.time()- start_time))
#
#
#
# dist = evaluate.chromosomeRoutesDistance(populations[0],DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,dep)
# print('Distances of the best chromosome: '+str(dist))
# print (populations[0])
# dist = evaluate.chromosomeRoutesDistance(populations[len(populations)-1],DISTANCES,DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,dep)
# print('Distances of the worst chromosome: '+str(dist))
# print(populations[len(populations)-1])


# #################################################################################################




