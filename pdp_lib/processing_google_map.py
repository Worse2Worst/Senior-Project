import math
from itertools import chain
import numpy as np
import pandas as pd
import copy
from statistics import mode,StatisticsError

# Loading a file
def load_file(filepath):
    df = pd.read_csv(filepath, header=None, delimiter=',',names =['Places','Lat','Long','Demands','ET','LT','serviceTime','pickup','delivery'] )

    numVehicles, loadCapacities, speed = 100,90,1

    # Initialized necessary variables
    locations = [[0,0]]
    demands = [0]
    timeWindows = [[0,9999999999999]]
    ServiceTimes = [0]
    pickupSiblings = [0]
    deliverySiblings = [0]
    requestType = ['Invalid']


    ######  loop the file ################
    for idx in range(1,len(df)):
        index, x, y = idx,float(df['Lat'][idx]), float(df['Long'][idx])
        demand = int(df['Demands'][idx])
        earliestTime, latestTime, service_time = int(df['ET'][idx]), int(df['LT'][idx]), int(df['serviceTime'][idx])
        p_sibling, d_sibling = int(df['pickup'][idx]), int(df['delivery'][idx])
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

    # # the depot have unlimit time windows
    # timeWindows[0] = [0,9999999999999999]
    # requestType[0] = 'DEPOT'

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



# Create a table that memo all distances bewtween any 2 nodes in the map
def createDistanceTable(filename):
    df = pd.read_csv(filename, header=None)
    n = len(df)
    distances = np.zeros((n, n))
    # create nxn matrix to memo the distances between nodes
    for i in range(n):
        for j in range(n):
            distances[i][j] = float(df[i][j])
    return distances



# Create a table that memo all durations of traveling bewtween any 2 nodes in the map
def createDurationTable(filename):
    df = pd.read_csv(filename, header=None)
    n = len(df)
    durations = np.zeros((n, n))
    # create nxn matrix to memo the durations between nodes
    for i in range(n):
        for j in range(n):
            durations[i][j] = float(df[i][j])
    return durations



def create_depots(filename):
    DEPOTS = []
    df = pd.read_csv(filename,names=['Places','Lat','Long'])
    n = len(df)
    for i in range(1,n):
        dep = df['Lat'][i],df['Long'][i]
        DEPOTS.append(dep)
    DEPOTS = dict(enumerate(DEPOTS))
    return DEPOTS

def locations_of_this_depot(dep,REQ_BY_DEPOTS,LOCATIONS):
    THIS_DEP_REQS = REQ_BY_DEPOTS[dep]
    THIS_LOCATIONS_INDEX = THIS_DEP_REQS.values()
    THIS_LOCATIONS_INDEX = list(chain(*THIS_LOCATIONS_INDEX))
    THIS_DEP_LOCATIONS = {idx: LOCATIONS[idx] for idx in THIS_LOCATIONS_INDEX}
    return THIS_DEP_LOCATIONS


def distances_to_depots(filename):
    # distances_to_depots[i][j] = location_i to depot_j
    arr = np.genfromtxt(filename,delimiter=',')
    return arr

def distances_from_depots(filename):
    # distances_from_depots[i][j] = depots_i to location_j
    arr = np.genfromtxt(filename, delimiter=',')
    return arr

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

def can_route(req1,req2,DISTANCES,DURATIONS,timeWindows):
    p1 = req1[0]
    d1 = req1[1]
    p2 = req2[0]
    d2 = req2[1]
    p1_tw = timeWindows[p1]
    d1_tw = timeWindows[d1]
    p2_tw = timeWindows[p2]
    d2_tw = timeWindows[d2]
    if(d1_tw[0] + DURATIONS[d1][p2] <= p2_tw[1]):
        return True
    if (p1_tw[0] + DURATIONS[p1][p2] <= p2_tw[1] and p2_tw[0] + DURATIONS[p2][d1] <= d1_tw[1] and d1_tw[0] + DURATIONS[d1][d2] <= d2_tw[1]):
        return True
    return  False

def can_merge_requests(REQUESTS,DISTANCES,timeWindows,DURATIONS,key1,key2):
    req1 = REQUESTS[key1]
    req2 = REQUESTS[key2]
    return can_route(req1,req2,DISTANCES,DURATIONS,timeWindows) or can_route(req2,req1,DISTANCES,DURATIONS,timeWindows)

def worse2worst_assign_depots(REQUESTS, timeWindows,DISTANCES,DURATIONS,DEPOTS,DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS):
    LOCATIONS = []
    dep_nums = np.zeros(shape=(len(REQUESTS)))
    old_dep_nums = simple_assign_depots(REQUESTS, LOCATIONS, DEPOTS,DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS)
    n = len(REQUESTS)
    m = len(DEPOTS)

    LT = []
    for key, value in REQUESTS.items():
        LT.append((key, timeWindows[value[0]][1]))
    LT = sorted(LT, key=lambda x: x[1])

    for key1,_ in LT:
        old_dep = int(old_dep_nums[key1])
        value = REQUESTS[key1]
        min_cost = DISTANCES_FROM_DEPOTS[old_dep][value[0]] + DISTANCES_TO_DEPOTS[value[1]][old_dep]
        # print('Min cost = '+str(min_cost))
        minDep = old_dep
        p1 = value[0]
        d1 = value[1]
        for key2,val2 in REQUESTS.items():
            p2 = val2[0]
            d2 = val2[1]
            if(key1 != key2 and can_merge_requests(REQUESTS,DISTANCES,timeWindows,DURATIONS,key1,key2)):
                cost = DISTANCES[p1][p2] + DISTANCES[d1][d2]
                if(cost < min_cost):
                    # print('found!!!!')
                    # print('Cost = ' + str(cost))
                    min_cost = cost
                    minDep = old_dep_nums[key2]
        dep_nums[key1] = minDep
        old_dep_nums[key1] = minDep
    return dep_nums

def vote_assign_depots(REQUESTS, timeWindows, DISTANCES, DURATIONS, DEPOTS, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, k=3):
    LOCATIONS = []
    dep_nums = np.zeros(shape=(len(REQUESTS)))
    old_dep_nums = simple_assign_depots(REQUESTS, LOCATIONS, DEPOTS, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS)
    n = len(REQUESTS)
    m = len(DEPOTS)

    LT = []
    for key, value in REQUESTS.items():
        LT.append((key, timeWindows[value[0]][1]))
    LT = sorted(LT, key=lambda x: x[1])
    for reqIndex1, _ in LT:
        voter = []
        old_dep = int(old_dep_nums[reqIndex1])
        value = REQUESTS[reqIndex1]
        cost = DISTANCES_FROM_DEPOTS[old_dep][value[0]] + DISTANCES_TO_DEPOTS[value[1]][old_dep]
        # print('Min cost = '+str(min_cost))
        minDep = old_dep
        p1 = value[0]
        d1 = value[1]
        for reqIndex2, val2 in REQUESTS.items():
            p2 = val2[0]
            d2 = val2[1]
            if (reqIndex1 != reqIndex2 and can_merge_requests(REQUESTS, DISTANCES, timeWindows, DURATIONS, reqIndex1, reqIndex2)):
                cost = DISTANCES[p1][p2] + DISTANCES[d1][d2]
            voter.append((reqIndex2,cost))
        voter.sort(key=lambda x: x[1])
        voter = voter[:k]
        voter = [int(old_dep_nums[reqIndex]) for (reqIndex,_)  in voter]
        # print((reqIndex1,voter))
        # if (len(set(voter)) == len(voter)):
        #     minDep = voter[0]
        # else:
        #     minDep = mode(voter)
        try:
            minDep = mode(voter)
        except StatisticsError:
            minDep = voter[0]
        dep_nums[reqIndex1] = minDep
        old_dep_nums[reqIndex1] = minDep
    return dep_nums


def closest_from_depot(node,DISTANCES_FROM_DEPOTS):
    # distances_from_depots[i][j] = depots_i to location_j
    dist = 999999999999999
    res = -999
    for dep in range(len(DISTANCES_FROM_DEPOTS)):
        if(DISTANCES_FROM_DEPOTS[dep][node] < dist):
            dist = DISTANCES_FROM_DEPOTS[dep][node]
            res = dep
    return res

def closest_to_depot(node, DISTANCES_TO_DEPOTS):
    dist = 999999999999999
    res = -999
    for dep in range(len(DISTANCES_TO_DEPOTS[0])):
        if(DISTANCES_TO_DEPOTS[node][dep] < dist):
            dist = DISTANCES_TO_DEPOTS[node][dep]
            res = dep
    return res




def final_assign_depots(REQUESTS, timeWindows, DISTANCES, DURATIONS, DEPOTS, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS, k=1):
    LOCATIONS = []
    dep_nums = np.zeros(shape=(len(REQUESTS)))
    simple_dep_nums = simple_assign_depots(REQUESTS, LOCATIONS, DEPOTS, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS)
    # vote_dep_nums = vote_assign_depots(REQUESTS, timeWindows, DISTANCES, DURATIONS, DEPOTS, DISTANCES_FROM_DEPOTS, DISTANCES_TO_DEPOTS,k)
    w2w = worse2worst_assign_depots(REQUESTS, timeWindows, DISTANCES, DURATIONS, DEPOTS, DISTANCES_FROM_DEPOTS,
                              DISTANCES_TO_DEPOTS)
    n = len(REQUESTS)
    m = len(DEPOTS)

    LT = []
    for key, value in REQUESTS.items():
        LT.append((key, timeWindows[value[0]][1]))
    LT = sorted(LT, key=lambda x: x[1])
    problematics = []
    for reqIndex1, _ in LT:
        voter = []
        old_dep = int(simple_dep_nums[reqIndex1])
        value = REQUESTS[reqIndex1]
        if(closest_from_depot(value[0],DISTANCES_FROM_DEPOTS) == closest_to_depot(value[1],DISTANCES_TO_DEPOTS)):
            dep_nums[reqIndex1] = closest_from_depot(value[0],DISTANCES_FROM_DEPOTS)
            simple_dep_nums[reqIndex1] = closest_from_depot(value[0],DISTANCES_FROM_DEPOTS)
        else:
            problematics.append(reqIndex1)
            # dep_nums[reqIndex1] = w2w[reqIndex1]


    for reqIndex1 in problematics:
        cost = DISTANCES_FROM_DEPOTS[old_dep][value[0]] + DISTANCES_TO_DEPOTS[value[1]][old_dep]
        p1 = value[0]
        d1 = value[1]
        voter = []
        for reqIndex2, val2 in REQUESTS.items():
            p2 = val2[0]
            d2 = val2[1]
            if (reqIndex1 != reqIndex2 and can_merge_requests(REQUESTS, DISTANCES, timeWindows, DURATIONS, reqIndex1, reqIndex2)):
                cost = DISTANCES[p1][p2] + DISTANCES[d1][d2]
                voter.append((reqIndex2,cost))
        voter.sort(key=lambda x: x[1])
        voter = voter[:k]
        voter = [int(simple_dep_nums[reqIndex]) for (reqIndex,_)  in voter]
        try:
            minDep = mode(voter)
        except StatisticsError:
            minDep = voter[0]
        dep_nums[reqIndex1] = minDep
        simple_dep_nums[reqIndex1] = minDep
    return dep_nums
