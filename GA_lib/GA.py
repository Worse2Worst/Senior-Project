import math
import random
from GA_lib import modify
from GA_lib import evaluate


def initialize_EMPTY_chromosome(num_vehicles):
    chromosome =[[car_num,[],[]] for car_num in range(num_vehicles)]
    return chromosome

def initialize_Feasible_chromosome(DISTANCES, DURATIONS, timeWindows,REQUESTS,num_vehicles = 25):
    chromosome = initialize_EMPTY_chromosome(num_vehicles)
    reqsIndexToInsert = [i for i in range(len(REQUESTS))] # Every requests,HARD Code!!!
    random.shuffle(reqsIndexToInsert)
    chromosome = modify.insert_requests_into_chromosome(chromosome, reqsIndexToInsert, DISTANCES, DURATIONS, timeWindows, REQUESTS)
    return chromosome
