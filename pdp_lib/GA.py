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
            pickup_pair = pair_node(job,node,nodes)
            if (not pickup_pair in visited):
                wrong_list.append((node,node.index,pickup_pair.index))
            else:
                visited.append(node)
    i = 0
    for v in visited:
        for w in wrong_list:
            if (int(w[2]) == int(v.index)):
                visited.insert(i+1,w[0])
        i += 1

    job = visited
    return job

def pair_node(job,v,nodes):
    if nodes[v].req_type == 'p':
        sib = int(nodes[v].d_sib)
    else:
        sib = int(nodes[v].p_sib)
    for i in job:
        if (sib == int(i)):
            return i



def swap(job,i,j):
    job[i],job[j]=job[j],job[i]

def set_files(fn):
    #print (fn)
    filename = fn
    nodes = tuple(preprocessing.load_node(filename))
    requests = preprocessing.generate_request(nodes)
    distances = processing.create_distance_matrix(nodes)


