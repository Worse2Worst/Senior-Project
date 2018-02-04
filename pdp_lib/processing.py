import math
import numpy as np
import copy

# Loading a file
def load_file(filename):
    file = open(filename, 'rt')
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

    data = [locations,demands,timeWindows,ServiceTimes,pickupSiblings,deliverySiblings,requestType]
    return numVehicles, loadCapacities, speed,data

# Generate pairs of requests (pickup-> delivery)
def generate_request(pickupSiblings,deliverySiblings,requestType):
    requests = []
    for i in range(len(requestType)):
        if(requestType[i]=='pickup'):
            requests.append((i,deliverySiblings[i]))
    return requests


# calculate Euclidean distances between nodes
def distance(location1,location2):
    x1 = location1[0]
    y1 = location1[1]
    x2 = location2[0]
    y2 = location2[1]
    return math.sqrt(((x1-x2)**2) +((y1-y2)**2))

# Create a table that memo all distances bewtween any 2 nodes in the map
def createDistanceTable(locations):
    n = len(locations)
    distances = np.zeros((n, n))
    # create nxn matrix to memo the distances between nodes
    for i in range(n):
        for j in range(n):
            distances[i][j] = distance(locations[i], locations[j])
    return distances

# calculate duration of traveling between a pair of nodes
def duration(v1,v2,distances,serviceTimes,speed):
    return distance(v1,v2)/speed


# Create a table that memo all durations of traveling bewtween any 2 nodes in the map
def createDurationTable(locations,distances,serviceTimes,speed=1.0):
    # n = len(locations)
    # durations = np.zeros((n, n))
    # # create nxn matrix to memo the distances between nodes
    # for i in range(n):
    #     for j in range(n):
    #         durations[i][j] = distances[i][j]/speed
    durations = np.asarray(distances)
    durations = durations/float(speed)
    durations = np.ndarray.tolist(durations)
    return durations






