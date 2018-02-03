import math
import numpy as np
import copy

# Loading a file
def load_file(filename):
    file = open(filename, 'rt')
    line = file.readline()

    numVehicles, loadCapacities, speed = line.split()

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
        if(requestType[i]=='p'):
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


def request_distances(requests):
    dist = 0
    for r in requests:
        dist += distance(r[0],r[1])
    #multiple dist by 2 to get a round-trip distance
    return 2*dist

#sort requests by LT of pickup nodes
def sort_requests(requests):
    requests.sort(key=lambda r: r[0].LT)




def maximum_distance_in_requests(requests):
    max_r = -1
    for r in requests:
        d = distance(r[0], r[1])
        if d > max_r:
            max_r = d
    return max_r


def make_depots(nodes):
    depots=[]
    index=len(nodes)
    size = -1
    if (len(nodes)>=1000): size=500
    elif (len(nodes)>=800):size=400
    elif (len(nodes)>=600):size=300
    elif (len(nodes)>=400):size=200
    elif (len(nodes)>=200):size=140
    else:size=100
    d0 = nodes[0]
    d1 = preprocessing.Node(d0.index, int(size/4),int(size/4),d0.demand,d0.ET,d0.LT,d0.service_time,d0.p_sib,d0.d_sib)
    d2 = preprocessing.Node(d0.index, int(size*3/4),int(size/4),d0.demand ,d0.ET,d0.LT,d0.service_time,d0.p_sib,d0.d_sib)
    d3 = preprocessing.Node(d0.index, int(size/4),int(size*3/4),d0.demand ,d0.ET,d0.LT,d0.service_time,d0.p_sib,d0.d_sib)
    d4 = preprocessing.Node(d0.index, int(size*3/4),int(size*3/4),d0.demand ,d0.ET,d0.LT,d0.service_time,d0.p_sib,d0.d_sib)

    '''
    # special case for size = 100
    if (size==100):
        d0.x+=10
    '''

    d1.req_type=d0.req_type
    d2.req_type = d0.req_type
    d3.req_type = d0.req_type
    d4.req_type = d0.req_type
    d0.depot=0
    d1.depot=1
    d2.depot=2
    d3.depot=3
    d4.depot=4
    depots.append(d0)
    depots.append(d1)
    depots.append(d2)
    depots.append(d3)
    depots.append(d4)
    return depots

def add_depots_to_nodes(nodes, depots):
    added_nodes = copy.deepcopy(nodes)
    for d in depots:
        added_nodes.append(d)
    return added_nodes

def assign_depot(clusters,depots,nodes):
    for c in clusters:
        depot_num=closest_depot(c,depots)
        for v in c:
            nodes[int(v[0].index)].depot = depot_num
            nodes[int(v[1].index)].depot = depot_num

def closest_depot(cluster,depots):
    min_dist = 9999999999999999
    min_depot = 10000000000000
    i=0
    for d in depots:
        dist=0
        for req in cluster:
            dist=distance(req[0],req[1])+distance(d,req[0])+distance(d,req[1])
        if(dist < min_dist):
            min_dist=dist
            min_depot=i
        i+=1
    return int(min_depot)

def closest_depot_distance(req,depots):
    min_dist = 9999999999999999
    min_depot = 10000000000000
    i=0
    for dep in depots:
        dist=distance(req[0],req[1])+distance(dep,req[0])+distance(dep,req[1])
        if(dist < min_dist):
            min_dist=dist
            min_depot=i
        i+=1
    return min_dist

# calculate the total unoptimized distance
def unoptimized_distance(requests,depots):
    dist=0
    for req in requests:
        dist += closest_depot_distance(req,depots)
    return dist