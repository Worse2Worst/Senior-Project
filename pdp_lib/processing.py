import math
from itertools import chain
import numpy as np
import copy

# Loading a file
def load_file(filepath):
    file = open(filepath, 'rt')
    line = file.readline()

    numVehicles, loadCapacities, speed = [int(num) for num in line.split()]

    # Initialized necessary variables
    locations = []
    demands = []
    timeWindows = []
    ServiceTimes = []
    pickupSiblings = []
    deliverySiblings = []
    requestType = []

    ######  Read the file ################
    line = file.readline()
    while line:
        index, x, y, demand, earliestTime, latestTime, service_time, p_sibling, d_sibling = [int(num) for num in line.split()]
        locations.append([x,y])
        demands.append(demand)
        timeWindows.append([earliestTime,latestTime])
        ServiceTimes.append(service_time)
        pickupSiblings.append(p_sibling)
        deliverySiblings.append(d_sibling)
        if (p_sibling == 0):
            requestType.append('pickup')
        else :
            requestType.append('delivery')
        # Read the next line
        line = file.readline()
    # close the file
    file.close()

    # the depot have unlimit time windows
    timeWindows[0] = [0,9999999999999999]
    requestType[0] = 'DEPOT'

    locations = dict(enumerate(locations))

    data = [locations,demands,timeWindows,ServiceTimes,pickupSiblings,deliverySiblings,requestType]
    return numVehicles, loadCapacities, speed,data

# Generate pairs of requests (pickup-> delivery)
def generate_request(pickupSiblings,deliverySiblings,requestType):
    requests = []
    for i in range(len(requestType)):
        if(requestType[i]=='pickup'):
            requests.append((i,deliverySiblings[i]))
    return dict(enumerate(requests))


# calculate Euclidean distances between nodes
def distance(location1,location2):
    x1 = location1[0]
    y1 = location1[1]
    x2 = location2[0]
    y2 = location2[1]
    return math.sqrt(((x1-x2)**2) +((y1-y2)**2))

# Create a table that memo all distances bewtween any 2 nodes in the map
def createDistanceTable(LOCATIONS):
    n = len(LOCATIONS)
    distances = np.zeros((n, n))
    # create nxn matrix to memo the distances between nodes
    for i in range(n):
        for j in range(n):
            distances[i][j] = distance(LOCATIONS[i], LOCATIONS[j])
    return distances

# calculate duration of traveling between a pair of nodes
def duration(v1,v2,DISTANCES,serviceTimes,speed):
    return (DISTANCES[v1][v2]/speed + serviceTimes[v1])


# Create a table that memo all durations of traveling bewtween any 2 nodes in the map
def createDurationTable(locations, DISTANCES, serviceTimes, speed=1.0):
    # Sometimes, the speed from instances are 'Zeros', so we will make it 'one'
    if(speed<=0):
        speed = 1.0

    n = len(locations)
    durations = np.zeros((n, n))
    # create nxn matrix to memo the distances between nodes
    for i in range(n):
        for j in range(n):
            durations[i][j] = DISTANCES[i][j]/speed + serviceTimes[i]
    durations = np.ndarray.tolist(durations)
    return durations



def create_depots(LOCATIONS):
    DEPOTS = []
    width = -1
    if (len(LOCATIONS) >= 1000):
        width = 500
    elif (len(LOCATIONS) >= 800):
        width = 400
    elif (len(LOCATIONS) >= 600):
        width = 300
    elif (len(LOCATIONS) >= 400):
        width = 200
    elif (len(LOCATIONS) >= 200):
        width = 140
    else:
        width = 100
    # Depot-0 , at center
    dep0 = copy.deepcopy(LOCATIONS[0])

    # Depot-1 , at upper left
    dep1 = [int(width/4),int(3*width/4)]

    # Depot-2 , at upper right
    dep2 = [int(3*width / 4), int(3*width / 4)]

    # Depot-3 , at lower left
    dep3 = [int(width / 4), int(width / 4)]

    # Depot-4 , at lower right
    dep4 = [int(3*width / 4), int(width / 4)]

    # # Special case for small size map (apporx. 100 nodes) ##
    # if(len(LOCATIONS)<150):
    #     dep1[0]-=10
    #     dep2[0]-=10
    #     dep3[0]-=10
    #     dep4[0]-=10

    ## Put every depots into the array ##
    DEPOTS.append(dep0)
    DEPOTS.append(dep1)
    DEPOTS.append(dep2)
    DEPOTS.append(dep3)
    DEPOTS.append(dep4)
    DEPOTS = dict(enumerate(DEPOTS))
    return DEPOTS

def locations_of_this_depot(dep,REQ_BY_DEPOTS,LOCATIONS):
    THIS_DEP_REQS = REQ_BY_DEPOTS[dep]
    THIS_LOCATIONS_INDEX = THIS_DEP_REQS.values()
    THIS_LOCATIONS_INDEX = list(chain(*THIS_LOCATIONS_INDEX))
    THIS_DEP_LOCATIONS = {idx: LOCATIONS[idx] for idx in THIS_LOCATIONS_INDEX}
    return THIS_DEP_LOCATIONS


def distances_to_depots(DEPOTS, LOCATIONS):
    # distances_to_depots[i][j] = location_i to depot_j
    n = len(LOCATIONS)
    m = len(DEPOTS)
    distances_to_depots = np.zeros(shape=(n,m))
    for i in range(n):
        for j in range(m):
            distances_to_depots[i][j] = distance(LOCATIONS[i],DEPOTS[j])
    return distances_to_depots

def distances_from_depots(DEPOTS, LOCATIONS):
    # distances_from_depots[i][j] = depots_i to location_j
    n = len(DEPOTS)
    m = len(LOCATIONS)
    distances_from_depots = np.zeros(shape=(n,m))
    for i in range(n):
        for j in range(m):
            distances_from_depots[i][j] = distance(DEPOTS[i],LOCATIONS[j])
    return distances_from_depots

def requests_by_depots(DEPOTS,REQUESTS,DEPOT_NUMBERS):
    REQ_BY_DEPOTS = []
    for i in range(len(DEPOTS)):
        temp = {}
        for id, req in REQUESTS.items():
            if (DEPOT_NUMBERS[id] == i):
                temp[id] = req
        REQ_BY_DEPOTS.append(temp)
    return REQ_BY_DEPOTS

def simple_assign_depots(REQUESTS, LOCATIONS, DEPOTS,DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS):
    dep_nums = np.zeros(shape=(len(REQUESTS)))
    n = len(REQUESTS)
    m = len(DEPOTS)
    for i in range(n): # loop in requests
        minDist = 9999999999
        minDep = 99
        for j in range(m): # loop in depots
            distPickup = DISTANCES_FROM_DEPOTS[j][REQUESTS[i][0]]
            distDelivery = DISTANCES_TO_DEPOTS[REQUESTS[i][1]][j]
            dist = distPickup + distDelivery
            if(dist < minDist):
                minDist = dist
                minDep = j
        dep_nums[i] = minDep
    return dep_nums


# def KNN_assign_depots():


