import os
import time
from pdp_lib import preprocessing
from pdp_lib import save_pics
from pdp_lib import util
from pdp_lib import processing


global filename
global nodes
global requests
global distances

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

def sibling(v,nodes):
    if nodes[v].req_type == 'p':
        sib = int(nodes[v].d_sib)
    else:
        sib = int(nodes[v].p_sib)
    return sib



def swap(job,i,j):
    job[i],job[j]=job[j],job[i]

def set_files(fn):
    #print (fn)
    filename = fn
    nodes = tuple(preprocessing.load_node(filename))
    requests = preprocessing.generate_request(nodes)
    distances = processing.create_distance_matrix(nodes)


