import math
from pdp_lib import util
from operator import itemgetter

# calculate distances between nodes
def distance(v1,v2):
    return math.sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2)

# create distance matrix (a complete graph of distances between every nodes)
def create_distance_matrix(nodes):
    n = len(nodes)
    distances = []
    # create nxn matrix to memo the distances between nodes
    for i in range(n):
        distances.append([])
        for j in range(n):
            distances[i].append(int(distance(nodes[i],nodes[j])))
    return distances


#sort requests by LT of pickup nodes
def sort_requests(requests):
    requests.sort(key=lambda r: r[0].LT)


############# Clustering (merge all version) ##########################
def clustering_requests(requests) :
    clusters = []
    added = {}
    sort_requests(requests) # requests are sorted by LT of pickups
    iter=1
    for r in requests:
        added = False
        for c in clusters:
            for rc in c:
                if should_merge(r,rc) and (not added):
                    c.append(r)
                    added = True
        if (not added):
            clusters.append([r])
        iter+=1
    return clusters


############ Clustering (merge only first node version) ##########################
def clustering_requests_only_first(requests):
    clusters = []
    added = {}
    sort_requests(requests)  # requests are sorted by LT of pickups
    iter = 1
    for r in requests:
        added = False
        for c in clusters:
            rc = c[0]
            if should_merge(r, rc) and (not added):
                c.append(r)
                added = True
        if (not added):
            clusters.append([r])
        iter += 1
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
