import math
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


#sort requests by ET of pickup nodes
def sort_requests(requests):
    requests.sort(key=lambda r: r[0].ET)

def clustering_requests(requests) :
    clusters = []
    added = {}
    sort_requests(requests)
    clusters.append(requests[0]) # the first one
    added.add(requests[0])
    #for r in requests:


