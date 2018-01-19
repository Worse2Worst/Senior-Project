import os
import time
import numpy as np
from random import randrange
from pdp_lib import preprocessing
from pdp_lib import save_pics
from pdp_lib import util
from pdp_lib import processing


global filename
global nodes
global requests
global distances

# A couple is the indices of all requests
def requests_to_couples(requests):
    couples=[]
    for req in requests:
        couples.append((int(req[0].index),int(req[1].index)))
    return couples

# node_index is the indices of all nodes
def couples_to_node_index(couples):
    node_index = []
    for x in couples:
        node_index.append(int(x[0]))
        node_index.append(int(x[1]))
    return node_index

# p_vehicle  is the population of vehicles, N is the population size
def initialize_p_vehicle(couples,N=100,max_vehicles=100,restricted_requests = 1000):
    # actually we have unlimited vehicles, but let's be realistic here
    # no retricted_requests for now
    p_vehicle = [None]*N # the initial population (size=N)
    for i in range (N):
        p_vehicle[i] = [0]*max_vehicles
        remain = len(couples)
        vehicle_index = 0
        while (remain>0):
            # nodes_visited is the numbers of node visited by that vehicle
            nodes_visited = randrange(1, remain+1)
            nodes_visited = min(remain,nodes_visited)
            p_vehicle[i][vehicle_index] = (nodes_visited*2)
            vehicle_index +=1
            remain -= nodes_visited
    return p_vehicle



# p_node is the population of nodes, N is the population size
def initialize_p_node(couples,nodes,N=100):
    node_index = couples_to_node_index(couples)
    p_node = [None] * N
    for i in range(N):
        p_node[i] = np.random.permutation(node_index).tolist()
        precedence_correction(p_node[i],couples)
    return p_node


# random operator for GA
def mutate(chromosome):
    random1 = randrange(0, len(chromosome))
    random2=random1
    while (random2==random1):
        random2 = randrange(0, len(chromosome))
    swap(chromosome,random1,random2)

def jobs_to_chromosome(jobs,nodes):
    max_vehicles = len(nodes)-1
    chromosome = [None] * max_vehicles
    for i in range(len(jobs)):
        chromosome[i]=jobs[i]
    return chromosome

def clusters_to_jobs(clusters):
    jobs = [] # array of integer!!!
    for cluster in clusters:
        jobs.append(cluster_to_job(cluster))
    return jobs

def cluster_to_job(cluster):
    job=[]
    for req in cluster:
        job.append(int(req[0].index))
        job.append(int(req[1].index))
    return job


def job_distance(job,distances):
    if len(job) <= 0: return 0
    d = 0
    last_node = int(job[-1])
    n = len(job)
    for i in range(n-1):
        d += distances[job[i]][job[i+1]]
    d += distances[job[0]][last_node] # complete the circle
    return d

def total_distances(jobs,distances):
    d = 0
    for job in jobs:
        d += job_distance(job,distances)
    return d

'''
def precedence_correction(job,nodes):
    wrong_list = []
    visited = []
    carrier = 0
    for i in job:
        if nodes[i].req_type == 'p':
            visited.append(i)
        else: # nodes[i] is delivery
            pickup_sibling = sibling(i,nodes)
            if (not pickup_sibling in visited):
                wrong_list.append((i,pickup_sibling))
            else:
                visited.append(i)
    i = 0
    for v in visited:
        for w in wrong_list:
            if (int(w[1]) == int(v)):
                visited.insert(i+1,w[0])
        i += 1

    job = visited
    return job
'''
def precedence_correction(node_index,couples):
    visited = []
    for i in range(len(node_index)):
        v = node_index[i]
        couple = [item for item in couples if v in item][0]
        pickup = couple[0] # pickup node
        delivery = couple[1] # delivery node
        if (v == delivery): # v is delivery
            if (not pickup in visited): # the pickup node is not visited
                pickup_index = node_index.index(pickup)
                pickup = node_index.pop(pickup_index) # still equals without assignment!!
                node_index.insert(i,pickup)
                visited.append(pickup)
                visited.append(v)
            else: # the sibling is visited
                visited.append(v)
        else: # v is pickup
            visited.append(v)
    return visited


def pickup_sibling(index,couples):
    sib = [item[0] for item in couples if index in item]
    return sib[0]

def delivery_sibling(index,couples):
    sib = [item[1] for item in couples if index in item]
    return sib[0]

def swap(array, i, j):
    array[i], array[j]= array[j], array[i]


## below is junk !!!
def set_files(fn):
    #print (fn)
    filename = fn
    nodes = tuple(preprocessing.load_node(filename))
    requests = preprocessing.generate_request(nodes)
    distances = processing.create_distance_table(nodes)


