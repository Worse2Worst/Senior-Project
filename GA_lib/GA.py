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

# p_couples is the population of couples, N is the population size
def create_p_couples(couples, N=10):
    p_couples = [None] * N
    for i in range(N):
        p_couples[i] = np.random.permutation(couples).tolist()
        #p_couples[i] = [tuple(l) for l in p_couples[i]] # to tuple
    return p_couples


# p_vehicle  is the population of vehicles, N is the population size
def create_p_vehicles(couples, N=10, max_vehicles=100, restricted_requests = 1000):
    # actually we have unlimited vehicles, but let's be realistic here
    # no retricted_requests for now
    p_vehicle = [None]*N # the initial population (size=N)
    for i in range (N):
        p_vehicle[i] = [0]*max_vehicles
        remain = len(couples)
        vehicle_index = 0
        while (remain>0):
            # couples_visited is the numbers of couples visited by that vehicle
            couples_visited = randrange(1, remain+1)
            couples_visited = min(remain,couples_visited)
            p_vehicle[i][vehicle_index] = (couples_visited)
            #p_vehicle[i].append(couples_visited)
            vehicle_index +=1
            remain -= couples_visited
        p_vehicle[i].sort(reverse = True)

        #strip out all useless zeros!!!
        p_vehicle[i] = list(filter(lambda a: a != 0, p_vehicle[i]))
    return p_vehicle



# p_node is the population of nodes, N is the population size
def create_p_nodes(couples, N=5):
    nodes = couples_to_node_index(couples)
    p_node = [None] * N
    for i in range(N):
        p_node[i] = np.random.permutation(nodes).tolist()
        precedence_correction(p_node[i],couples)
    return p_node


# final population!!!
def create_p_jobs(p_couples_vehicles,N=10):
    # 'p_couples_vehicles' is an array of chromosome of couples
    p_jobs = [None]*len(p_couples_vehicles) * N
    i = 0
    for chromosome in p_couples_vehicles:
        num_vehicles = len(chromosome)
        for _ in range (N):
            p_jobs[i] = [None] * num_vehicles
            j = 0
            for couples in chromosome:
                nodes = couples_to_node_index(couples)
                job = np.random.permutation(nodes).tolist()
                job = precedence_correction(job, couples)
                # print('-----jobs -----------------')
                # print(job)
                # print('***************************')
                p_jobs[i][j] = job
                j += 1
            i += 1
    return p_jobs

# create p_couples_vehicles, representing vehicles visiting couples
# 'p_couples' has sex with 'p_vehicles'
def create_p_couples_vehicles(p_couples,p_vehicles):
    res = [None]*len(p_vehicles)*len(p_couples) # the result will be size N1*N2
    i = 0
    for couples in p_couples:
        for vehicles in p_vehicles:
            pos = 0
            res[i] = [None]*len(vehicles)
            j = 0
            for num in vehicles:
                res[i][j] = couples[pos:(pos+num)]
                pos += num
                j += 1
            i += 1
    return res

# random operator for GA
def mutate(chromosome):
    random1 = randrange(0, len(chromosome))
    random2=random1
    while (random2==random1):
        random2 = randrange(0, len(chromosome))
    swap(chromosome,random1,random2)




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
                node_index.pop(pickup_index)
                node_index.insert(i,pickup)
                visited.append(pickup)
                visited.append(v)
            else: # the sibling is visited
                visited.append(v)
        else: # v is pickup
            visited.append(v)
    return node_index


def pickup_sibling(index,couples):
    sib = [item[0] for item in couples if index in item]
    return sib[0]

def delivery_sibling(index,couples):
    sib = [item[1] for item in couples if index in item]
    return sib[0]

def swap(array, i, j):
    array[i], array[j]= array[j], array[i]


# eval distance of all p_jobs
def eval_distance (p_jobs,distances,depot,nodes):
    res = []
    for jobs in p_jobs:
        res.append(jobs_distance(jobs,distances,depot,nodes))
    return res

# distance of 'jobs' by all vehicles
def jobs_distance(jobs, distances, depot,nodes):
    dist = 0
    for job in jobs:
        dist += job_distance(job,distances,depot,nodes)
    return dist

# distance of just one 'job' by one vehicle
def job_distance(job,distances,depot,nodes):
    dist = 0
    for i in range(len(job)-1):
        dist += distances[job[i]][job[i+1]]
    dist += processing.distance(nodes[job[0]],depot)+processing.distance(nodes[job[-1]],depot)
    return dist


## below is junk !!!
'''
def set_files(fn):
    #print (fn)
    filename = fn
    nodes = tuple(preprocessing.load_node(filename))
    requests = preprocessing.generate_request(nodes)
    distances = processing.create_distance_table(nodes)


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

'''