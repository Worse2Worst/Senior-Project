import time
import os
import random
import csv
import numpy as np
import pandas as pd
from itertools import chain
from pdp_lib import processing as proc
from pdp_lib import util
from GA_lib import GA_multi_depot as GA
from GA_lib import operation_multi_depot as operation
from GA_lib import evaluate_multi_depot as evaluate
from statistics import mode,StatisticsError

start_time = time.time()
# use 'relative path' in filename
filename = 'pdp_instances/LiLim/pdp_100/lrc101.txt'

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
DISTANCES_FROM_DEPOTS = proc.distances_from_depots(DEPOTS, LOCATIONS)
DISTANCES_TO_DEPOTS = proc.distances_to_depots(DEPOTS, LOCATIONS)
# DEPOT_NUMBERS = proc.simple_assign_depots(REQUESTS, LOCATIONS, DEPOTS, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS)
# DEPOT_NUMBERS = proc.worse2worst_assign_depots(REQUESTS, timeWindows,DISTANCES,DURATIONS,DEPOTS,DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS)
DEPOT_NUMBERS = proc.vote_assign_depots(REQUESTS, timeWindows,DISTANCES,DURATIONS,DEPOTS,DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS)
REQ_BY_DEPOTS = proc.requests_by_depots(DEPOTS, REQUESTS, DEPOT_NUMBERS)


print(" processing time --- %s seconds ---" % (time.time() - start_time))

DEPOT_NUMBERS = proc.debug666(REQUESTS, timeWindows, DISTANCES, DURATIONS, DEPOTS, DISTANCES_FROM_DEPOTS,DISTANCES_TO_DEPOTS,k=3)
util.draw_simple_assigned_depots(REQUESTS,LOCATIONS,DEPOTS,DEPOT_NUMBERS)