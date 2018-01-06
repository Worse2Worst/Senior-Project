import math
import numpy
from pdp_lib import util
from pdp_lib import preprocessing
from operator import itemgetter

# calculate distances between nodes
def distance(v1,v2):
    return math.sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2)

# create distance matrix (a complete graph of distances between every nodes)
def create_distance_matrix(nodes):
    n = len(nodes)
    distances = numpy.zeros((n, n))
    # create nxn matrix to memo the distances between nodes
    for i in range(n):
        for j in range(n):
            distances[i][j] = distance(nodes[i],nodes[j])
    return distances

def request_distances(requests):
    dist = 0
    for r in requests:
        dist += distance(r[0],r[1])
    #multiple dist by 2 to get a round-trip distance
    return 2*dist

#sort requests by LT of pickup nodes
def sort_requests(requests):
    requests.sort(key=lambda r: r[0].LT)


############# Clustering (merge all version) ##########################
def clustering_requests(requests) :
    clusters = []
    sort_requests(requests) # requests are sorted by LT of pickups
    for r in requests:
        added = False
        merge_index = -1
        c_index = 0
        c_size = 99999999999999
        for c in clusters:
            for rc in c:
                if should_merge(r,rc) and (not added):
                    if (len(c) < c_size):
                        c_size = len(c)
                        merge_index = c_index
                    added = True
        if (not added):
            clusters.append([r])
        else:
            clusters[merge_index].append(r)
    return clusters


############ Clustering (merge only first node version) ##########################
def clustering_requests_only_first(requests):
    clusters = []
    sort_requests(requests)  # requests are sorted by LT of pickups
    for r in requests:
        added = False
        merge_index = -1
        c_index=0
        time_gap=99999999999999
        for cluster in clusters:
            rc = cluster[0]
            if should_merge(r, rc) and (not added):
                if (abs(r[1].LT - rc[1].LT) < time_gap):
                    time_gap=abs(r[1].LT-rc[1].LT)
                    merge_index = c_index
                added = True
            c_index+=1
        if (not added):
            clusters.append([r])
        else:
            clusters[merge_index].append(r)
    return clusters


# should merge only if the merged(new) ones produce the shorter distance
def should_merge(r1,r2):
    p1,d1 = r1[0],r1[1]
    p2,d2 = r2[0],r2[1]
    old_distance = 2 * (distance(p1,d1)+distance(p2,d2))
    new_distance=merged_distance(p1,p2,d1,d2)
    if(new_distance<old_distance):
        return True
    return False

# There are 6 permutations
def merged_distance(p1,p2,d1,d2):
    dist = circular_distance(p1,p2,d1,d2)
    dist = min(dist,circular_distance(p1,d1,p2,d2))
    dist = min(dist,circular_distance(p1,p2,d1,d2))
    dist = min(dist,circular_distance(p2,p1,d2,d1))
    dist = min(dist,circular_distance(p2,p1,d1,d2))
    dist = min(dist,circular_distance(p2,d2,p1,d1))
    return dist

# calculate distance of a route that visit all nodes
def circular_distance (v1,v2,v3,v4):
    if (not time_feasible(v1,v2)) or (not time_feasible(v2,v3)) or (not time_feasible(v3,v4)): return 99999999999999
    return distance(v1,v2)+distance(v2,v3)+distance(v3,v4)+distance(v4,v1)

def time_feasible(v1,v2,speed=1):
    # used time = distance/speed
    limit_time = v2.LT - v1.ET
    dist=distance(v1,v2)
    used_time=(dist/speed)
    if (used_time > limit_time):
        return False
    return True

def maximum_distance_in_requests(requests):
    max_r = -1
    for r in requests:
        d = distance(r[0], r[1])
        if d > max_r:
            max_r = d
    return max_r


def add_depots(nodes):
    depots=[]
    d0=nodes[0]

    index=len(nodes)
    size = -1
    if (len(nodes)>=1000): size=500
    elif (len(nodes)>=800):size=400
    elif (len(nodes)>=600):size=300
    elif (len(nodes)>=400):size=200
    elif (len(nodes)>=200):size=140
    else:size=100

    d1 = preprocessing.Node(d0.index, int(size/4),int(size/4),d0.demand,d0.ET,d0.LT,d0.service_time,d0.p_sib,d0.d_sib)
    d2 = preprocessing.Node(d0.index, int(size*3/4),int(size/4),d0.demand ,d0.ET,d0.LT,d0.service_time,d0.p_sib,d0.d_sib)
    d3 = preprocessing.Node(d0.index, int(size/4),int(size*3/4),d0.demand ,d0.ET,d0.LT,d0.service_time,d0.p_sib,d0.d_sib)
    d4 = preprocessing.Node(d0.index, int(size*3/4),int(size*3/4),d0.demand ,d0.ET,d0.LT,d0.service_time,d0.p_sib,d0.d_sib)
    d1.req_type=d0.req_type
    d2.req_type = d0.req_type
    d3.req_type = d0.req_type
    d4.req_type = d0.req_type
    nodes.append(d0)
    nodes.append(d1)
    nodes.append(d2)
    nodes.append(d3)
    nodes.append(d4)
    return nodes
