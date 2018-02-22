import time
from random import shuffle
import random
from pdp_lib import processing as proc
from pdp_lib import util
from GA_lib import GA
from GA_lib import operation
from GA_lib import evaluate
import csv

def solve_and_print(filename,rounds = 30,population_size = 100,generations=2000,crossoverRate=1.0,mutationRate=0.7):
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

    print('----------------Instance name: '+str(filename)+'-----------------------------------')
    print(" processing time --- %s seconds ---" % (time.time() - start_time))

    results = []
    ## Loop and memo results

    for round in range(rounds):
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
            # f = min(f, evaluate.chromosomeFitness(child2, DISTANCES))
            # f = min(f, evaluate.chromosomeFitness(elite1, DISTANCES))
            # f = min(f, evaluate.chromosomeFitness(elite2, DISTANCES))
            # if(f<bestFitness):
            #     bestFitness = f
            #     bestFitGen = gen
            # if(bestFitGen-gen >= 3000):
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
        # dist = evaluate.chromosomeRoutesDistance(populations[len(populations) - 1], DISTANCES)
        # print('Distances of the worst chromosome: ' + str(dist))
        # print(populations[len(populations) - 1])
        #
        # #################################################################################################
        print('Chromosome waiting time :' + str(evaluate.chromosomeWatingTime(best_chromosome, DURATIONS, timeWindows)))
        results.append(best_result)
    return results

####################### Main Function Below #################################################################
filename = 'pdp_instances/LiLim/pdp_100/lc101.txt'
results = solve_and_print(filename,rounds=3)
fileWrite = filename.rsplit('/',1)[1].split('.txt')[0]
with open(filename+'.csv', "w") as f:
    writer = csv.writer(f)
    writer.writerows(results)